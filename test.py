import unittest
from app import app, db, User, Task
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user

class TaskManagementTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test environment and create a test client."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SECRET_KEY'] = 'testsecretkey'
        self.client = app.test_client()
        
        # Create all tables
        with app.app_context():
            db.create_all()

        # Create a sample user
        self.user = User(username="testuser", password="testpassword", gender="Male")
        with app.app_context():
            db.session.add(self.user)
            db.session.commit()

    def tearDown(self):
        """Clean up after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_user(self):
        """Test the user registration functionality."""
        response = self.client.post('/register', data=dict(
            username="newuser", password="newpassword", gender="Female"), follow_redirects=True)
        self.assertIn(b'Signup successful!', response.data)
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)

    def test_login_user(self):
        """Test the user login functionality."""
        response = self.client.post('/login', data=dict(
            username="testuser", password="testpassword"), follow_redirects=True)
        self.assertIn(b'Home page', response.data)

    def test_add_task(self):
        """Test adding a task."""
        self.client.post('/login', data=dict(
            username="testuser", password="testpassword"), follow_redirects=True)
        response = self.client.post('/add', data=dict(
            title="Test Task", description="Test task description", due_date="2024-12-25", category="General"), follow_redirects=True)
        self.assertIn(b'Task added successfully!', response.data)

    def test_update_task(self):
        """Test updating a task."""
        self.client.post('/login', data=dict(
            username="testuser", password="testpassword"), follow_redirects=True)
        task = Task(title="Old Task", description="Old description", user_id=self.user.id)
        db.session.add(task)
        db.session.commit()
        response = self.client.post(f'/update/{task.id}', data=dict(
            title="Updated Task", description="Updated description", due_date="2024-12-30", category="Updated Category"), follow_redirects=True)
        self.assertIn(b'Task updated successfully!', response.data)

    def test_delete_task(self):
        """Test deleting a task."""
        self.client.post('/login', data=dict(
            username="testuser", password="testpassword"), follow_redirects=True)
        task = Task(title="Task to delete", description="This task will be deleted", user_id=self.user.id)
        db.session.add(task)
        db.session.commit()
        response = self.client.post(f'/delete/{task.id}', follow_redirects=True)
        self.assertIn(b'Task deleted successfully!', response.data)

    def test_access_dashboard_without_login(self):
        """Test access to dashboard without login."""
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn(b'Login', response.data)

if __name__ == '__main__':
    unittest.main()
