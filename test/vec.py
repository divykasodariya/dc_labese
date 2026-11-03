
import csv
import os
import threading
import time

CSV = "tasks_4.csv"

lock = threading.Lock()
completed = []

# Create CSV if it doesn't exist
if not os.path.exists(CSV):
    with open(CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["task_id", "thread_name", "burst_ms", "priority", "status"])
        w.writerows([
            ["T1", "Worker_1", 300, "HIGH", "PENDING"],
            ["T2", "Worker_2", 200, "MEDIUM", "PENDING"],
            ["T3", "Worker_3", 400, "LOW", "PENDING"],
            ["T4", "Worker_1", 250, "HIGH", "PENDING"]
        ])

# Read tasks
tasks = []

with open(CSV, "r") as f:
    for row in csv.DictReader(f):
        tasks.append(row)


# Function executed by each thread
def process_task(task):

    tid = task["task_id"]
    worker = task["thread_name"]

    print(worker, "waiting for", tid)

    time.sleep(int(task["burst_ms"]) / 1000)

    # Critical section
    lock.acquire()

    print(worker, "LOCK ACQUIRED")

    completed.append(tid)

    print(tid, "COMPLETED")

    lock.release()

    print(worker, "LOCK RELEASED")


# Start threads
threads = []

for task in tasks:
    t = threading.Thread(target=process_task, args=(task,))
    t.start()
    threads.append(t)

# Wait for all threads
for t in threads:
    t.join()

print("\nFinal Completed Tasks:")
print(completed)
