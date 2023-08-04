"""User user views."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follow, Like
from flask import session


# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app, CURR_USER_KEY

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

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

app.config['WTF_CSRF_ENABLED'] = False


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        self.client = app.test_client()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)
        db.session.flush()

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id



    def tearDown(self):
        db.session.rollback()


    def test_show_user_profile(self):
        user = User.query.get(self.u1_id)

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.get(f"/users/{self.u1_id}", follow_redirects=True)
            self.assertEqual(resp.status_code, 200) #test status code
            html = resp.get_data(as_text=True)
            self.assertIn("FOR ROUTE TEST: USER PROFILE PAGE", html)
            self.assertIn(user.username, html)


    def test_show_user_profile_logged_out_state(self):

        with self.client as c:
            resp = c.get(f"/users/{self.u1_id}", follow_redirects=True)
            self.assertEqual(resp.status_code, 200,) #test status code
            html = resp.get_data(as_text=True)
            self.assertIn("FOR ROUTE TEST: HOME-ANON", html)
            self.assertIn("Access unauthorized", html)


    def test_show_user_profile_redirection_logged_out(self):

        with self.client as c:
            resp = c.get(f"/users/{self.u1_id}")
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/")


    def test_login(self):
        """Test to see if user is logged in and session is updating
        curr user key."""

        with self.client as c:
            resp = c.post(
                "/login",
                data={
                    'username': 'u1',
                    'password': 'password'
                },
                follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("FOR ROUTE TEST: HOMEPAGE", html)
            self.assertTrue(session.get(CURR_USER_KEY))


#     def test_show_following(self):
#         """Show list of people this user is following."""
#         ...


#     def test_show_followers(self):
#         """Show list of followers of this user."""
#         ...


#     def test_start_following(self):
#         """Redirects to 'following' page of the current user"""
#         ...


#     def test_stop_following(self):
#         ...

#     def test_profile_page(self):
#         ...

#     def test_delete_user(self):
#         ...


#     def test_add_message(self):
#         ...

#     def test_show_message(self):
#         ...

#     def test_delete_message(self):
#         ...

#     def test_homepage(self):
#         ...

#     def test_like_message(self):
#         ...

#     def test_unlike_message(self):
#         ...

#     def test_display_user_likes(self):
#         ...

# @session_test
#     def test_view(self):
#     def session_test(fn):
#         self.client = app.test_client()
#         fn()
#         # test for invalid user error




