import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u=User(password='lenson')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u=User(password='lenson')
        with self.assertRaises(AttributeError):

    def test_password_verification(self):
        u=User(password='lenson')
        self.assertTrue(u.verify_password('lenson'))
        self.assertFalse(u.verify_password('ggsmd'))

    def test_paswword_salts_random(self):
        u=User(password='ggsmd')
        u2=User(password='ggsmd')
        self.assertTrue(u.password_hash!=u2.password_hash)

