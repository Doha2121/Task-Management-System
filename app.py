from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)

# Set database path relative to the instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'tasks_management.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key

# Ensure the instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)


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


# Initialize the database
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Routes for the app
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('Home page.html', tasks=tasks)


@app.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        gender = request.form.get('gender')

        # Check if user exists already
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('Username already taken. Please choose another one.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password, gender=gender)
        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful! You can now login.')

        # Redirect to the login page after successful signup
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the user exists in the database
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
            return render_template('login.html')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/add', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    due_date_str = request.form.get('due_date')
    category = request.form.get('category')
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None

    if not title:
        flash('Title is required for the task!')
        return jsonify({'status': 'error', 'message': 'Title is required!'})

    new_task = Task(title=title, description=description, due_date=due_date, category=category, user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    flash('Task added successfully!')

    # Return JSON response with task data
    return jsonify({
        'status': 'success',
        'task_id': new_task.id,
        'task_title': new_task.title,
        'task_description': new_task.description,
        'task_due_date': new_task.due_date,
        'task_category': new_task.category
    })


@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_task(id):
    task = db.session.get(Task, id)
    if not task or task.user_id != current_user.id:
        flash('Task not found or you are not authorized to edit this task.')
        return redirect(url_for('home'))

    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
        task.category = request.form.get('category')
        db.session.commit()
        flash('Task updated successfully!')

        # After updating, redirect to the dashboard page, where updated tasks will be shown
        return redirect(url_for('dashboard'))

    # Pass the formatted due_date to ensure proper format for the input field
    formatted_due_date = task.due_date.strftime('%Y-%m-%d') if task.due_date else None
    return render_template('update.html', task=task, formatted_due_date=formatted_due_date)


@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_task(id):
    task = db.session.get(Task, id)
    if task and task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!')

        # Return JSON response for task deletion
        return jsonify({'status': 'success', 'task_id': id})

    flash('Task not found or you are not authorized to delete this task.')
    return jsonify({'status': 'error', 'message': 'Failed to delete task'})


if __name__ == '__main__':
    app.run(debug=True)
