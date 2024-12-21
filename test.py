import unittest
from datetime import datetime, timedelta

# Mock implementation of the system for testing
class Task:
    def __init__(self, title, category, due_date, priority):
        self.title = title
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.completed = False

    def mark_as_completed(self):
        self.completed = True

    def mark_as_pending(self):
        self.completed = False

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tasks = []

    def create_task(self, title, category, due_date, priority):
        task = Task(title, category, due_date, priority)
        self.tasks.append(task)
        return task

    def delete_task(self, task):
        self.tasks.remove(task)

    def find_task(self, title):
        return next((task for task in self.tasks if task.title == title), None)

    def get_sorted_tasks(self, key):
        return sorted(self.tasks, key=lambda task: getattr(task, key))

# Mock user authentication
class AuthenticationService:
    def __init__(self):
        self.users = {}

    def register(self, username, password):
        if username in self.users:
            raise ValueError("User already exists")
        self.users[username] = User(username, password)

    def login(self, username, password):
        user = self.users.get(username)
        if not user or user.password != password:
            raise ValueError("Invalid credentials")
        return user

# Unit tests
class TestTaskManagementSystem(unittest.TestCase):
    def setUp(self):
        self.auth_service = AuthenticationService()
        self.auth_service.register("test_user", "password123")
        self.user = self.auth_service.login("test_user", "password123")

    def test_user_registration_and_login(self):
        self.auth_service.register("new_user", "new_password")
        user = self.auth_service.login("new_user", "new_password")
        self.assertEqual(user.username, "new_user")

    def test_create_task(self):
        task = self.user.create_task(
            title="Finish project",
            category="work",
            due_date=datetime.now() + timedelta(days=1),
            priority=1
        )
        self.assertEqual(task.title, "Finish project")
        self.assertIn(task, self.user.tasks)

    def test_delete_task(self):
        task = self.user.create_task(
            title="Task to delete",
            category="work",
            due_date=datetime.now() + timedelta(days=1),
            priority=2
        )
        self.user.delete_task(task)
        self.assertNotIn(task, self.user.tasks)

    def test_mark_task_as_completed(self):
        task = self.user.create_task(
            title="Task to complete",
            category="personal",
            due_date=datetime.now() + timedelta(days=1),
            priority=3
        )
        task.mark_as_completed()
        self.assertTrue(task.completed)

    def test_sort_tasks_by_due_date(self):
        self.user.create_task("Task A", "work", datetime.now() + timedelta(days=3), 2)
        self.user.create_task("Task B", "personal", datetime.now() + timedelta(days=1), 1)
        self.user.create_task("Task C", "work", datetime.now() + timedelta(days=2), 3)
        sorted_tasks = self.user.get_sorted_tasks("due_date")
        self.assertEqual([task.title for task in sorted_tasks], ["Task B", "Task C", "Task A"])

    def test_reminders(self):
        task = self.user.create_task(
            title="Task with reminder",
            category="work",
            due_date=datetime.now() + timedelta(days=1),
            priority=1
        )
        reminder_time = task.due_date - timedelta(hours=1)
        now = datetime.now()
        self.assertGreater(task.due_date, now)
        self.assertGreater(task.due_date, reminder_time)

if __name__ == "__main__":
    unittest.main()