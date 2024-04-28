import shutil

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = 'secret_key'


# Создаем базу данных и таблицы для результатов участников и задач
def create_tables():
    conn = sqlite3.connect('competition_results.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS participants 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 author_file_solution TEXT NOT NULL,
                 runner_file TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS results 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 participant_id INTEGER NOT NULL,
                 task_id INTEGER NOT NULL,
                 language TEXT NOT NULL,
                 score INTEGER NOT NULL,
                 FOREIGN KEY (participant_id) REFERENCES participants(id),
                 FOREIGN KEY (task_id) REFERENCES tasks(id))''')
    conn.commit()
    conn.close()


create_tables()


@app.route('/')
def index():
    tasks = get_tasks()
    participants = get_participants()
    return render_template('upload_file.html', tasks=tasks, participants=participants)


@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    language_author = request.form['language_author']
    file_author = request.files['file_author']
    file_runner = request.files['file_runner']
    if task_name.strip() != '':
        if file_author and allowed_file(file_author.filename, language_author) and file_runner and allowed_file(
                file_runner.filename, "python"):
            file_author.save(f'author_solutions/{task_name}_{file_author.filename}')
            file_runner.save(f'runners/{task_name}_{file_runner.filename}')

            conn = sqlite3.connect('competition_results.db')
            c = conn.cursor()
            c.execute("INSERT INTO tasks (name, author_file_solution, runner_file) VALUES (?, ?, ?)",
                      (task_name, file_author.filename, file_runner.filename,))
            conn.commit()
            conn.close()
            flash('Задача успешно добавлена', 'success')
        else:
            return 'Ошибка: Неверный формат файла или язык программирования'
    else:
        flash('Пожалуйста, введите название задачи', 'error')
    return redirect(url_for('index'))


@app.route('/add_participant', methods=['POST'])
def add_participant():
    participant_name = request.form['participant_name']
    if participant_name.strip() != '':
        conn = sqlite3.connect('competition_results.db')
        c = conn.cursor()
        c.execute("INSERT INTO participants (name) VALUES (?)", (participant_name,))
        conn.commit()
        conn.close()
        flash('Участник успешно добавлен', 'success')
    else:
        flash('Пожалуйста, введите имя участника', 'error')
    return redirect(url_for('index'))


def get_tasks():
    conn = sqlite3.connect('competition_results.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks


def get_participants():
    conn = sqlite3.connect('competition_results.db')
    c = conn.cursor()
    c.execute("SELECT * FROM participants")
    participants = c.fetchall()
    conn.close()
    return participants


@app.route('/submit_solution', methods=['POST'])
def upload_file():
    selected_task_id = int(request.form['task'])
    selected_language = request.form['language']
    file = request.files['file']
    participant_id = int(request.form['participant'])

    if file and allowed_file(file.filename, selected_language):
        # Сохраняем результаты в базу данных
        if save_result(participant_id, selected_task_id, selected_language, file):
            return redirect(url_for('show_results'))
        else:
            return 'Ошибка: ваше решение не соответствует протоколу взаимодействия'
    else:
        return 'Ошибка: Неверный формат файла или язык программирования'


def allowed_file(filename, language):
    if language == 'cpp':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'cpp'
    elif language == 'python':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'py'
    else:
        return False


# -1 - у первого RE
# -2 - у второго RE
# 1 - первый победил
# 2 - второй победил
def check(sol1_name, sol2_name, runner_name):
    shutil.copy(runner_name, f'now_runner/now_runner_file.py')
    from now_runner import now_runner_file
    if now_runner_file.run(sol1_name, sol2_name) > 0:
        return True
    return False


def save_result(participant_id, task_id, language, participant_solution):
    conn = sqlite3.connect('competition_results.db')
    c = conn.cursor()
    c.execute(f"SELECT author_file_solution FROM tasks \
              WHERE id = {task_id}")
    author_file = c.fetchall()[0][0]

    c.execute(f"SELECT name FROM tasks \
                  WHERE id = {task_id}")
    task_name = c.fetchall()[0][0]

    c.execute(f"SELECT runner_file FROM tasks \
                      WHERE id = {task_id}")
    runner_file = f'runners/{task_name}_{c.fetchall()[0][0]}'

    participant_solution.save(f'participants_solutions/{task_name}_{participant_id}_{participant_solution.filename}')

    sol1_name = f'author_solutions/{task_name}_{author_file}'
    sol2_name = f'participants_solutions/{task_name}_{participant_id}_{participant_solution.filename}'
    if check(sol1_name, sol2_name, runner_file):
        # Просто для примера, результат участника генерируется случайным образом
        import random
        score = random.randint(0, 100)

        c.execute("INSERT INTO results (participant_id, task_id, language, score) VALUES (?, ?, ?, ?)",
                  (participant_id, task_id, language, score))
        conn.commit()
        conn.close()

        return True
    else:
        return False


@app.route('/results')
def show_results():
    conn = sqlite3.connect('competition_results.db')
    c = conn.cursor()

    # Получаем список задач для заголовков таблицы
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()

    # Получаем результаты для каждой задачи и каждого участника
    c.execute("SELECT participants.id, participants.name, results.task_id, results.score FROM participants \
               JOIN results ON participants.id = results.participant_id \
               ORDER BY participants.id, results.task_id")
    results = c.fetchall()
    conn.close()

    # Создаем словарь, где ключи - это идентификаторы участников,
    # а значения - словари, содержащие количество баллов для каждой задачи
    participant_scores = {}
    for result in results:
        participant_id = result[0]
        participant_name = result[1]
        task_id = result[2]
        score = result[3]

        if participant_id not in participant_scores:
            participant_scores[participant_id] = {'name': participant_name, 'scores': {}, 'total_score': 0}

        participant_scores[participant_id]['scores'][task_id] = score
        participant_scores[participant_id]["total_score"] += score

    participant_scores_sorted = []
    for participant_id, participant_info in participant_scores.items():
        participant_scores_sorted.append([participant_id, participant_info])
    participant_scores_sorted.sort(key=lambda item: item[1]['total_score'], reverse=True)

    return render_template('results.html', tasks=tasks, participant_scores=participant_scores_sorted)


app.run(debug=True, port=8000)
# app.run(debug=True, ssl_context=('/Users/ilyaglazkov/PycharmProjects/flaskProject2/server.crt', '/Users/ilyaglazkov/PycharmProjects/flaskProject2/server.key'))
