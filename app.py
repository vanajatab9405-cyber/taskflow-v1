from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)
DB = 'tasks.db'

# Initialize DB if not exists
def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        start_date TEXT NOT NULL,
                        due_date TEXT NOT NULL,
                        category TEXT,
                        status TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return redirect(url_for('create_task'))

@app.route('/create')
def create_task():
    return render_template('create_task.html')


@app.route('/add', methods=['POST'])
def add_task():
    try:
        name = request.form.get('name', '').strip()

        if not name:
            return {"success": False, "message": "Task name is required"}, 400

        start_date = request.form['start_date']
        due_date = request.form['due_date']

        if start_date > due_date:
            return {"success": False, "message": "End date must be after start date"}, 400


        description = request.form.get('description', '')
        start_date = request.form['start_date']
        due_date = request.form['due_date']
        category = request.form.get('category', '')
        status = request.form['status']

        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tasks (name, description, start_date, due_date, category, status) VALUES (?, ?, ?, ?, ?, ?)',
            (name, description, start_date, due_date, category, status)
        )
        conn.commit()
        conn.close()

        return {"success": True, "message": "Task saved successfully"}, 200

    except Exception as e:
        return {"success": False, "message": str(e)}, 500
    

@app.route('/edit/<int:id>')
def edit_task(id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id=?", (id,))
    t = cursor.fetchone()
    conn.close()

    task = {
        'id': t[0],
        'name': t[1],
        'description': t[2],
        'start_date': t[3],
        'due_date': t[4],
        'category': t[5],
        'status': t[6]
    }

    return render_template('edit_task.html', task=task)

@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    name = request.form['name']
    description = request.form.get('description', '')
    start_date = request.form['start_date']
    due_date = request.form['due_date']
    category = request.form.get('category', '')
    status = request.form['status']

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET name=?, description=?, start_date=?, due_date=?, category=?, status=?
        WHERE id=?
    """, (name, description, start_date, due_date, category, status, id))
    conn.commit()
    conn.close()

    return redirect(url_for('all_tasks'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return {"success": True}



@app.route('/tasks')
def all_tasks():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks_data = cursor.fetchall()
    tasks = []
    for t in tasks_data:
        tasks.append({
            'id': t[0],
            'name': t[1],
            'description': t[2],
            'start_date': t[3],
            'due_date': t[4],
            'category': t[5],
            'status': t[6]
        })
    conn.close()
    return render_template('all_tasks.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
