import unittest
from app import app, db, User, Task
from werkzeug.security import generate_password_hash

class TaskManagementTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SECRET_KEY'] = 'testsecret'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()
            # Create a test user
            user = User(username="testuser", password=generate_password_hash("testpassword"), gender="male")
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, username, password):
        return self.client.post('/login', data={
            'username': username,
            'password': password
        }, follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_register(self):
        response = self.client.post('/register', data={
            'username': 'newuser',
            'password': 'newpassword',
            'gender': 'female'
        })
        self.assertEqual(response.status_code, 302)
        with app.app_context():
            user = User.query.filter_by(username='newuser').first()
            self.assertIsNotNone(user)

    def test_login(self):
        response = self.login('testuser', 'testpassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    def test_login_fail(self):
        response = self.login('testuser', 'wrongpassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)


    def test_delete_task(self):
        with app.app_context():
            user = User.query.filter_by(username='testuser').first()
            task = Task(title='Test Task', description='This will be deleted', user_id=user.id)
            db.session.add(task)
            db.session.commit()

        self.login('testuser', 'testpassword')
        response = self.client.post(f'/delete/{task.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        with app.app_context():
            deleted_task = Task.query.get(task.id)
            self.assertIsNone(deleted_task)

    def test_home_no_login(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main()
