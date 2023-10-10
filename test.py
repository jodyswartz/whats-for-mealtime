import unittest
from main import app


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.main = app.test_client()
        self.main.testing = True

    def test_index(self):
        response = self.main.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
