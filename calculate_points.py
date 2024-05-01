import sqlite3

conn = sqlite3.connect('competition_results.sqlite')
c = conn.cursor()
c.execute("SELECT * FROM tasks")
tasks = c.fetchall()

for task in tasks:
    task_id = task[0]
    c.execute(f"SELECT author_file_solution FROM tasks \
                  WHERE id = {task_id}")

conn.close()
