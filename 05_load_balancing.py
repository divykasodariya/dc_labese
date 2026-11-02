
import csv
import os

CSV = "workload.csv"

WORKERS = ["Worker_1", "Worker_2", "Worker_3"]

METHOD = "least"  # "least" or "round_robin"

# Create sample CSV if it doesn't exist
if not os.path.exists(CSV):
    with open(CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["job_id", "compute_units", "assigned_worker", "status"])
        w.writerows([
            ["J101", 35, "UNASSIGNED", "PENDING"],
            ["J102", 20, "UNASSIGNED", "PENDING"],
            ["J103", 50, "UNASSIGNED", "PENDING"],
            ["J104", 15, "UNASSIGNED", "PENDING"],
            ["J105", 40, "UNASSIGNED", "PENDING"]
        ])

# Read jobs
jobs = []

with open(CSV, "r") as f:
    for row in csv.DictReader(f):
        jobs.append(row)

# Initialize worker loads and job counts
loads = {}
counts = {}

for worker in WORKERS:
    loads[worker] = 0
    counts[worker] = 0

print("Method:", METHOD)
# jobs.sort(key = lambda s : s['job_id'])
# Assign jobs
for i, job in enumerate(jobs):

    if METHOD == "round_robin":
        worker = WORKERS[i % len(WORKERS)]

    else:
        worker = min(loads, key=loads.get)

    units = int(job["compute_units"])

    loads[worker] += units
    counts[worker] += 1

    print(job["job_id"], "->", worker)

# Display final results
print("\nFinal Worker Load:")

for worker in WORKERS:
    print(worker, ":", loads[worker], "units,", counts[worker], "jobs")
