from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Configure logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date, nullable=True)
    category = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Task({self.title}, {self.completed}, {self.due_date}, {self.category})'

@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except Exception as e:
        logging.error(f"Error loading user: {e}")
        return None

# Home route
@app.route('/')
@login_required
def index():
    try:
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        return render_template('index.html', tasks=tasks)
    except Exception as e:
        logging.error(f"Error fetching tasks: {e}")
        flash('An error occurred while fetching tasks.')
        return redirect(url_for('login'))

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except Exception as e:
            logging.error(f"Error during registration: {e}")
            flash('An error occurred during registration.')
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            flash('Login failed. Check your username or password.')
        except Exception as e:
            logging.error(f"Error during login: {e}")
            flash('An error occurred during login.')
    return render_template('login.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    try:
        logout_user()
    except Exception as e:
        logging.error(f"Error during logout: {e}")
        flash('An error occurred during logout.')
    return redirect(url_for('login'))

# Add task
@app.route('/add', methods=['POST'])
@login_required
def add_task():
    try:
        title = request.form.get('title')
        description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        category = request.form.get('category')
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
        if title:
            new_task = Task(title=title, description=description, due_date=due_date, category=category, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Task added successfully!')
    except Exception as e:
        logging.error(f"Error adding task: {e}")
        flash('An error occurred while adding the task.')
    return redirect(url_for('index'))

# Update task
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_task(id):
    try:
        task = db.session.get(Task, id)
        if request.method == 'POST':
            if task and task.user_id == current_user.id:
                task.title = request.form.get('title')
                task.description = request.form.get('description')
                due_date_str = request.form.get('due_date')
                task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
                task.category = request.form.get('category')
                db.session.commit()
                flash('Task updated successfully!')
                return redirect(url_for('index'))
    except Exception as e:
        logging.error(f"Error updating task: {e}")
        flash('An error occurred while updating the task.')
    return render_template('update_task.html', task=task)

# Toggle task completion
@app.route('/toggle/<int:id>', methods=['POST'])
@login_required
def toggle_task(id):
    try:
        task = db.session.get(Task, id)
        if task and task.user_id == current_user.id:
            task.completed = not task.completed
            db.session.commit()
            flash('Task updated successfully!')
    except Exception as e:
        logging.error(f"Error toggling task completion: {e}")
        flash('An error occurred while updating the task.')
    return redirect(url_for('index'))

# Delete task
@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_task(id):
    try:
        task = db.session.get(Task, id)
        if task and task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()
            flash('Task deleted successfully!')
    except Exception as e:
        logging.error(f"Error deleting task: {e}")
        flash('An error occurred while deleting the task.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            logging.error(f"Error creating database tables: {e}")
            print("An error occurred while creating the database tables.")
    app.run(debug=True)
