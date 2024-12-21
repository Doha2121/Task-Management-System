import unittest
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import app, db, User, Task, login_manager
from datetime import datetime

# Setting up a test database and app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_tasks.db'
app.config['TESTING'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'test_secret_key'

# Initialize Flask-Login
login_manager.init_app(app)

class FlaskTestCase(unittest.TestCase):
    # Set up and tear down methods for test environment
    def setUp(self):
        # Create a test client
        self.client = app.test_client()
        # Create all tables in the test database
        with app.app_context():
            db.create_all()

        # Create a test user
        self.user = User(username='testuser', password='testpassword')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        # Drop all tables after tests
        with app.app_context():
            db.drop_all()

    # Test case for registration
    def test_register(self):
        response = self.client.post('/register', data={
            'username': 'newuser',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)  # Expecting redirect to login page
        new_user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(new_user)  # Check if new user exists in DB

    # Test case for login
    def test_login(self):
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Expecting redirect to index page
        self.assertIn(b'Logout', response.data)  # Check if logged-in user is on the page

    # Test case for adding a task
    def test_add_task(self):
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        response = self.client.post('/add', data={
            'title': 'New Task',
            'description': 'Task Description',
            'due_date': '2024-12-25',
            'category': 'Work'
        })
        task = Task.query.filter_by(title='New Task').first()
        self.assertIsNotNone(task)  # Task should be in DB
        self.assertEqual(task.title, 'New Task')

    # Test case for updating a task
    def test_update_task(self):
        task = Task(title='Old Task', description='Old Description', user_id=self.user.id)
        db.session.add(task)
        db.session.commit()

        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        response = self.client.post(f'/update/{task.id}', data={
            'title': 'Updated Task',
            'description': 'Updated Description',
            'due_date': '2024-12-31',
            'category': 'Personal'
        })
        updated_task = Task.query.get(task.id)
        self.assertEqual(updated_task.title, 'Updated Task')
        self.assertEqual(updated_task.description, 'Updated Description')

    # Test case for toggling task completion
    def test_toggle_task(self):
        task = Task(title='Task to Toggle', description='Task Description', user_id=self.user.id)
        db.session.add(task)
        db.session.commit()

        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        response = self.client.post(f'/toggle/{task.id}')
        updated_task = Task.query.get(task.id)
        self.assertTrue(updated_task.completed)  # Check if task is toggled

    # Test case for deleting a task
    def test_delete_task(self):
        task = Task(title='Task to Delete', description='Task Description', user_id=self.user.id)
        db.session.add(task)
        db.session.commit()

        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        response = self.client.post(f'/delete/{task.id}')
        deleted_task = Task.query.get(task.id)
        self.assertIsNone(deleted_task)  # Task should be deleted

    # Test case for handling errors in the home route
    def test_home_route_error(self):
        # Force an error by causing a failure in database query (e.g., user is not logged in)
        self.client.get('/')
        self.assertIn(b'An error occurred while fetching tasks.', self.client.get('/').data)

if __name__ == '__main__':
    unittest.main()
