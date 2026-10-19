import json
import unittest
from http.client import HTTPConnection
from threading import Thread
from http.server import HTTPServer

from app import CalculatorHandler


class CalculatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), CalculatorHandler)
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()

    def test_calculates_dps(self):
        connection = HTTPConnection("127.0.0.1", self.server.server_port)
        connection.request("GET", "/?damage=250&attacks=2&crit=20")
        response = connection.getresponse()
        payload = json.loads(response.read())
        self.assertEqual(response.status, 200)
        self.assertEqual(payload["dps"], 600.0)


if __name__ == "__main__":
    unittest.main()
