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

    def test_roles_permissions(self):
        Role.updata_roles()
        u=User(email='lensonzhu@163.com',password='zhulunchen111')
        self.assertTrue(u.can(Permission.WRITE_ARTCLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u=AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))


