import unittest
import jwt
from datetime import datetime, timedelta
from users.utils.jwt_utils import encode_jwt, decode_jwt


class TestJWTUtils(unittest.TestCase):
    def setUp(self):
        self.user_payload = {"user_id": 123, "email": "test@example.com"}
        self.secret_key = "testsecret"
        self.algorithm = "HS256"

    def test_encode_jwt_returns_string(self):
        token = encode_jwt(
            self.user_payload, secret=self.secret_key, algorithm=self.algorithm
        )
        self.assertIsInstance(token, str)

    def test_decode_jwt_returns_payload(self):
        token = jwt.encode(
            {**self.user_payload, "exp": datetime.utcnow() + timedelta(hours=1)},
            self.secret_key,
            algorithm=self.algorithm,
        )
        payload = decode_jwt(token, secret=self.secret_key, algorithms=[self.algorithm])
        self.assertIn("user_id", payload)
        self.assertEqual(payload["user_id"], self.user_payload["user_id"])

    def test_decode_jwt_expired_token_raises(self):
        token = jwt.encode(
            {**self.user_payload, "exp": datetime.utcnow() - timedelta(hours=1)},
            self.secret_key,
            algorithm=self.algorithm,
        )
        with self.assertRaises(jwt.ExpiredSignatureError):
            decode_jwt(token, secret=self.secret_key, algorithms=[self.algorithm])

    def test_decode_jwt_invalid_token_raises(self):
        invalid_token = "invalid.token.value"
        with self.assertRaises(jwt.DecodeError):
            decode_jwt(
                invalid_token, secret=self.secret_key, algorithms=[self.algorithm]
            )


if __name__ == "__main__":
    unittest.main()
