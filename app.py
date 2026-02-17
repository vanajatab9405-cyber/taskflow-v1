from flask import render_template, request, redirect, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

import os

database_url = os.environ.get("DATABASE_URL")

if database_url:
    database_url = database_url.replace("postgres://", "postgresql://")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or "sqlite:///local.db"



db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.String(20), nullable=False)
    due_date = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(100))
    status = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return redirect(url_for('create_task'))

@app.route('/create')
def create_task():
    return render_template('create_task.html')

@app.route('/add', methods=['POST'])
def add_task():
    name = request.form.get('name', '').strip()

    if not name:
        return {"success": False, "message": "Task name is required"}, 400

    start_date = request.form['start_date']
    due_date = request.form['due_date']

    if start_date > due_date:
        return {"success": False, "message": "End date must be after start date"}, 400

    description = request.form.get('description', '')
    category = request.form.get('category', '')
    status = request.form['status']

    new_task = Task(
        name=name,
        description=description,
        start_date=start_date,
        due_date=due_date,
        category=category,
        status=status
    )

    db.session.add(new_task)
    db.session.commit()

    return {"success": True, "message": "Task saved successfully"}, 200

@app.route('/tasks')
def all_tasks():
    tasks = Task.query.all()
    return render_template('all_tasks.html', tasks=tasks)

@app.route('/edit/<int:id>')
def edit_task(id):
    task = Task.query.get_or_404(id)
    return render_template('edit_task.html', task=task)

@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    task = Task.query.get_or_404(id)

    task.name = request.form['name']
    task.description = request.form.get('description', '')
    task.start_date = request.form['start_date']
    task.due_date = request.form['due_date']
    task.category = request.form.get('category', '')
    task.status = request.form['status']

    db.session.commit()

    return redirect(url_for('all_tasks'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()

    return {"success": True}



if __name__ == "__main__":
    app.run(debug=True)
