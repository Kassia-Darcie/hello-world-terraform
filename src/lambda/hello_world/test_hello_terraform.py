import unittest

from hello_terraform import lambda_handler


class TestLambdaFunction(unittest.TestCase):
    def test_hello_world(self):
        event = {}
        context = {}
        response = lambda_handler(event, context)
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(response["body"], '"Hellow Terraform!"')


if __name__ == "__main__":
    unittest.main()
