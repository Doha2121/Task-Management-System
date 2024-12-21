import unittest
from app import app, db, User, Task
from flask_login import login_user
from werkzeug.security import generate_password_hash


class TaskManagementTestCase(unittest.TestCase):

    # Setup and teardown for test database
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SECRET_KEY'] = 'testsecret'
        self.client = app.test_client()
        db.create_all()

        # Create a test user
        self.user = User(username="testuser", password=generate_password_hash("testpassword"), gender="male")
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Test user registration
    def test_register(self):
        response = self.client.post('/register', data={
            'username': 'newuser',
            'password': 'newpassword',
            'gender': 'female'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to login page
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)

    # Test user login
    def test_login(self):
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to home page
        self.assertIn('home', response.location)

    # Test login failure (invalid credentials)
    def test_login_fail(self):
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Should stay on the login page
        self.assertIn(b'Invalid username or password.', response.data)

    # Test adding a task
    def test_add_task(self):
        with self.client:
            login_user(self.user)
            response = self.client.post('/add', data={
                'title': 'Test Task',
                'description': 'Task description',
                'due_date': '2024-12-31',
                'category': 'Work'
            })
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['status'], 'success')
            task = Task.query.filter_by(title='Test Task').first()
            self.assertIsNotNone(task)

    # Test updating a task
    def test_update_task(self):
        # Add a task
        task = Task(title='Test Task', description='Old description', user_id=self.user.id)
        db.session.add(task)
        db.session.commit()

        with self.client:
            login_user(self.user)
            response = self.client.post(f'/update/{task.id}', data={
                'title': 'Updated Task',
                'description': 'Updated description',
                'due_date': '2025-01-01',
                'category': 'Home'
            })
            self.assertEqual(response.status_code, 302)  # Should redirect to dashboard
            updated_task = Task.query.get(task.id)
            self.assertEqual(updated_task.title, 'Updated Task')
            self.assertEqual(updated_task.description, 'Updated description')

    # Test deleting a task
    def test_delete_task(self):
        # Add a task
        task = Task(title='Test Task', description='This will be deleted', user_id=self.user.id)
        db.session.add(task)
        db.session.commit()

        with self.client:
            login_user(self.user)
            response = self.client.post(f'/delete/{task.id}')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['status'], 'success')
            deleted_task = Task.query.get(task.id)
            self.assertIsNone(deleted_task)

    # Test home page access without login (should redirect to login)
    def test_home_no_login(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 302)  # Should redirect to login page

    # Test dashboard page access with login
    def test_dashboard_with_login(self):
        with self.client:
            login_user(self.user)
            response = self.client.get('/dashboard')
            self.assertEqual(response.status_code, 200)
            self.assertIn('dashboard.html', response.data)

    # Test logout
    def test_logout(self):
        with self.client:
            login_user(self.user)
            response = self.client.get('/logout')
            self.assertEqual(response.status_code, 302)  # Should redirect to login page
            self.assertIn('login', response.location)


if __name__ == '__main__':
    unittest.main()
