"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from models import db, User, Message, Follow, Like

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app
from sqlalchemy.exc import IntegrityError
from app import app



DEFAULT_IMAGE_URL = (
    "https://icon-library.com/images/default-user-icon/" +
    "default-user-icon-28.jpg")

DEFAULT_HEADER_IMAGE_URL = (
    "https://images.unsplash.com/photo-1519751138087-5bf79df62d5b?ixlib=" +
    "rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=for" +
    "mat&fit=crop&w=2070&q=80")

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        u1 = User.query.get(self.u1_id)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)

    def test_user_following(self):
        """Does is_following successfully detect when user1 is following user2?
        Does is_followed_by successfully detect when user2 is followed by user1?
        """

        u1=User.query.get(self.u1_id)
        u2=User.query.get(self.u2_id)

        follow = Follow(user_being_followed_id=self.u2_id,
                        user_following_id=self.u1_id )

        db.session.add(follow)
        db.session.commit()


        self.assertTrue(u1.is_following(u2))
        self.assertTrue(u2.is_followed_by(u1))

    def test_user_not_following(self):
        """Does is_following successfully detect when user1 is not following
          user2?
          Does is_followed_by successfully detect when user2 is not followed
          by user1?
        """

        u1=User.query.get(self.u1_id)
        u2=User.query.get(self.u2_id)

        self.assertFalse(u1.is_following(u2))
        self.assertFalse(u2.is_followed_by(u1))

    def test_valid_signup(self):
        """Does User.signup successfully create a new user given
        valid credentials?"""

        self.assertEqual(User.query.count(),2)
        u3= User.signup('u3',"u3@email.com", "password", None)

        self.assertEqual(User.query.count(),3)
        self.assertEqual(u3.username,'u3')
        self.assertEqual(u3.email,'u3@email.com')
        self.assertEqual(u3.image_url, DEFAULT_IMAGE_URL)
        self.assertIn('$2b',u3.password)

        # signup(cls, username, email, password, image_url=DEFAULT_IMAGE_URL):

    def test_invalid_signup(self):
        """ Does User.signup fail to create a new user if any of the
        validations (eg uniqueness, non-nullable fields) fail?"""

        #test duplicate username
        u3= User.signup('u2',"u3@email.com", "password", None)
        db.session.add(u3)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()

        # #test duplicate email
        u4= User.signup('u4',"u2@email.com", "password", None)
        db.session.add(u4)
        self.assertRaises(IntegrityError, db.session.commit)
        breakpoint()
        db.session.rollback()

        # #test no username
        u5= User.signup(None,"u5@email.com", "password", None)
        db.session.add(u5)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()

        # #test no email
        u6= User.signup('u6',None, "password", None)
        db.session.add(u6)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()

        # # test no password
        self.assertRaises(ValueError, User.signup,'u5','u5@email.com',None)

#
#
#
#
# Does User.signup fail to create a new user if any of the validations (eg uniqueness, non-nullable fields) fail?
# Does User.authenticate successfully return a user when given a valid username and password?
# Does User.authenticate fail to return a user when the username is invalid?
# Does User.authenticate fail to return a user when the password is invalid?