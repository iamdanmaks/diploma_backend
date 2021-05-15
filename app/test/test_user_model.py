import unittest
import datetime
import uuid

from app.main import db
from app.main.model.user import User
from app.main.service.token_service import encode_auth_token, decode_auth_token
from app.test.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            public_id=str(uuid.uuid4()),
            email='test@email.com',
            username='test',
            password='test',
            first_name='test',
            last_name='test',
            apply_reason='test',
            registration_date=datetime.datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()
        auth_token = encode_auth_token(days=1, seconds=5, user_id=user.public_id)
        
        self.assertTrue(user.public_id == decode_auth_token(auth_token)[0])


if __name__ == '__main__':
    unittest.main()