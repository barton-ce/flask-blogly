import unittest
from app import app
from models import db, connect_db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Stop Flask-DebugToolbar from running in tests
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

connect_db(app)
db.create_all()


class UserViewsTestCase(unittest.TestCase):
    

    def setUp(self):
        

        User.query.delete()

        user = User(first_name='John', last_name='Doe', image_url='http://example.com')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        self.client = app.test_client()
        app.config['TESTING'] = True

    def tearDown(self):
        

        db.session.rollback()

    def test_users_index(self):
        

        with self.client as c:
            resp = c.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Doe', html)
            self.assertIn('http://example.com', html)

    def test_new_user_form(self):
        

        with self.client as c:
            resp = c.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a user</h1>', html)

    def test_show_user(self):
        

        with self.client as c:
            resp = c.get(f'/user/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>John Doe</h1>', html)
            self.assertIn('http://example.com', html)

    def test_edit_user(self):
        

        with self.client as c:
            resp = c.get(f'/users/{self.user_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit John Doe</h1>', html)
            self.assertIn('http://example.com', html)

    def test_users_destroy(self):
        

        with self.client as c:
            resp = c.post(f'/users/{self.user_id}/delete')
            self.assertEqual(resp.status_code, 302)

            user = User.query.get(self.user_id)
            self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()
