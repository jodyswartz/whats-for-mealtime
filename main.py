import io
import os
from datetime import datetime
from functools import wraps

import pyotp
import qrcode
from qrcode.constants import ERROR_CORRECT_M
from flask import Flask, redirect, render_template, request, session, send_file, url_for

from crud import insert_feeding, list_feedings, ping_db
from utils import load_food_list

app = Flask(__name__)

# Used to sign the session cookie (required for login sessions)
app.secret_key = os.getenv("APP_SECRET_KEY", "dev-secret-change-me")

FOOD_LIST_PATH = os.getenv("FOOD_LIST_PATH", "foodlist.txt")


def _now_defaults():
    now = datetime.now()
    return now.strftime("%Y-%m-%d"), now.strftime("%H:%M")


def _totp() -> pyotp.TOTP:
    secret = os.getenv("TOTP_SECRET", "").strip()
    if not secret:
        raise RuntimeError("TOTP_SECRET is not set")
    return pyotp.TOTP(secret)


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("authed"):
            return redirect(url_for("login"))
        return fn(*args, **kwargs)

    return wrapper


@app.get("/login")
def login():
    # Add ?setup=1 the first time so you can scan the QR code.
    show_qr = request.args.get("setup") == "1"
    issuer = os.getenv("TOTP_ISSUER", "AstroJournal")
    account = os.getenv("TOTP_ACCOUNT", "me")
    secret = os.getenv("TOTP_SECRET", "")
    return render_template(
        "login.html",
        error=None,
        show_qr=show_qr,
        issuer=issuer,
        account=account,
        secret=secret,
    )


@app.post("/login")
def login_post():
    code = (request.form.get("code") or "").strip().replace(" ", "")
    try:
        # valid_window=1 allows a little clock drift (30s)
        if _totp().verify(code, valid_window=1):
            session["authed"] = True
            return redirect(url_for("index"))
    except Exception:
        pass
    return render_template("login.html", error="Invalid code.", show_qr=False), 401


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.get("/totp-qr")
def totp_qr():
    issuer = os.getenv("TOTP_ISSUER", "AstroJournal")
    account = os.getenv("TOTP_ACCOUNT", "me")
    uri = _totp().provisioning_uri(name=account, issuer_name=issuer)

    # Generate a high-contrast, large, easy-to-scan QR code
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_M,
        box_size=10,   # bigger modules
        border=4,
    )
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


@app.get("/")
@login_required
def index():
    default_date, default_time = _now_defaults()
    foods = load_food_list(FOOD_LIST_PATH)

    ok, db_status = ping_db() if os.getenv("MONGODB_URI") else (False, "Not configured (MONGODB_URI not set)")
    return render_template(
        "index.html",
        default_date=default_date,
        default_time=default_time,
        db_status=db_status,
        foods=foods,
    )


@app.post("/submit")
@login_required
def submit():
    foods = load_food_list(FOOD_LIST_PATH)
    allowed_foods = {f.strip().lower() for f in foods if f.strip()}
    allowed_foods.add("water")  # safety

    date = (request.form.get("date") or "").strip()
    time = (request.form.get("time") or "").strip()
    name = (request.form.get("name") or "").strip()
    amount_raw = (request.form.get("amount") or "").strip()

    errors = []

    # Required
    if not date:
        errors.append("Date is required.")
    if not time:
        errors.append("Time is required.")
    if not name:
        errors.append("Food name is required.")
    if not amount_raw:
        errors.append("Amount is required.")

    # Format checks
    if date:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            errors.append("Date must be in YYYY-MM-DD format.")

    if time:
        try:
            datetime.strptime(time, "%H:%M")
        except ValueError:
            errors.append("Time must be in HH:MM (24-hour) format.")

    # Name must be in list
    name_norm = name.strip().lower()
    if name and name_norm not in allowed_foods:
        errors.append("Food name must be one of the options in the dropdown.")

    # Amount must be integer
    amount_int = None
    if amount_raw:
        try:
            amount_int = int(amount_raw)
        except ValueError:
            errors.append("Amount must be a whole number.")

    # Range check
    if amount_int is not None:
        if amount_int < 1:
            errors.append("Amount must be at least 1.")
        if amount_int > 500:
            errors.append("Amount looks too large (max 500).")

    # Water rule (server enforced)
    if name_norm == "water":
        amount_int = 1

    if errors:
        default_date, default_time = _now_defaults()
        ok, db_status = ping_db() if os.getenv("MONGODB_URI") else (False, "Not configured (MONGODB_URI not set)")
        return render_template(
            "index.html",
            default_date=default_date,
            default_time=default_time,
            db_status=db_status,
            foods=foods,
            errors=errors,
            form={"date": date, "time": time, "name": name, "amount": amount_raw},
        ), 400

    doc = {
        "date": date,
        "time": time,
        "name": name,
        "amount": amount_int,  # store as number
    }

    inserted_id = None
    if os.getenv("MONGODB_URI"):
        ok, _ = ping_db()
        if ok:
            inserted_id = insert_feeding(doc)

    return redirect(url_for("logs", inserted_id=inserted_id or ""))


@app.get("/logs")
@login_required
def logs():
    ok, db_status = ping_db() if os.getenv("MONGODB_URI") else (False, "Not configured (MONGODB_URI not set)")
    inserted_id = request.args.get("inserted_id") or ""
    feedings = list_feedings(limit=80) if os.getenv("MONGODB_URI") else []
    return render_template("receipt.html", feedings=feedings, db_status=db_status, inserted_id=inserted_id)


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=debug)