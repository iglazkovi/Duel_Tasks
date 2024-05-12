import shutil
import sqlite3


def run(sol1_name, sol2_name, runner_name):
    shutil.copy(runner_name, f'now_runner/now_runner_file.py')
    from now_runner import now_runner_file
    return now_runner_file.run(sol1_name, sol2_name)


conn = sqlite3.connect('competition_results.sqlite')
c = conn.cursor()
c.execute("SELECT * FROM tasks")
tasks = c.fetchall()

data = {}
c.execute(f"SELECT * FROM participants")
participants = c.fetchall()
for participant in participants:
    for task in tasks:
        if participant[0] not in data.keys():
            data[participant[0]] = {}
        data[participant[0]][task[0]] = 0

for task in tasks:
    task_id = task[0]
    c.execute(f"SELECT * FROM solutions \
                  WHERE task_id = {task_id}")
    solutions = c.fetchall()
    participantId_solIdx = dict()
    for participant in participants:
        participantId_solIdx[participant[0]] = -1
    for i in range(len(solutions)):
        participantId_solIdx[solutions[i][3]] = i
    for part1 in range(len(participants)):
        i = participantId_solIdx[participants[part1][0]]
        for part2 in range(part1 + 1, len(participants)):
            j = participantId_solIdx[participants[part2][0]]
            if i == -1:
                if j == -1:
                    continue
                else:
                    sol2 = solutions[j]
                    path_to_sol2 = sol2[1]
                    participant2_id = sol2[3]
                    data[participant2_id][task_id] += 1
            else:
                if j == -1:
                    sol1 = solutions[i]
                    path_to_sol1 = sol1[1]
                    participant1_id = sol1[3]
                    data[participant1_id][task_id] += 1
                else:
                    sol1 = solutions[i]
                    path_to_sol1 = sol1[1]
                    participant1_id = sol1[3]

                    sol2 = solutions[j]
                    path_to_sol2 = sol2[1]
                    participant2_id = sol2[3]

                    task_name = task[1]
                    path_to_task_runner = f'runners/{task_name}_{task[3]}'

                    result = run(path_to_sol1, path_to_sol2, path_to_task_runner)
                    if result == 1 or result == -2:
                        data[participant1_id][task_id] += 1
                    else:
                        data[participant2_id][task_id] += 1

print(data)
c.execute("DELETE FROM results")
for task in tasks:
    for participant in participants:
        participant_id = participant[0]
        task_id = task[0]
        score = data[participant_id][task_id]
        print(task, participant)
        c.execute("INSERT INTO results (participant_id, task_id, score) VALUES (?, ?, ?)",
                  (participant_id, task_id, score))

c.execute("SELECT participants.id, participants.name, results.task_id, results.score FROM participants \
               JOIN results ON participants.id = results.participant_id \
               ORDER BY participants.id, results.task_id")
results = c.fetchall()
print(results)
conn.commit()
conn.close()
