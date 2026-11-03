import csv
import os
from concurrent.futures import ThreadPoolExecutor

CSV_FILE = "matrix.csv"

# Fixed Matrix B
B = [
    [1, 2, 3, 4],
    [2, 0, 1, 3],
    [1, 1, 0, 2],
    [0, 2, 1, 1]
]

# Create sample CSV if it does not exist
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["row_id", "col_0", "col_1", "col_2", "col_3"])
        w.writerows([
            ["R0", 2, 4, 1, 5],
            ["R1", 1, 3, 2, 4],
            ["R2", 5, 2, 0, 1],
            ["R3", 3, 1, 4, 2]
        ])

# Each worker multiplies one row of A with B
def multiply_row(data):
    row_id, row = data
    result = []

    for j in range(4):
        total = 0

        for k in range(4):
            total += row[k] * B[k][j]

        result.append(total)

    print("Worker calculated", row_id, ":", result)
    return result


# MASTER: Read Matrix A
matrix_a = []

with open(CSV_FILE, "r") as f:
    reader = csv.DictReader(f)

    for row in reader:
        values = [int(row["col_" + str(i)]) for i in range(4)]
        matrix_a.append((row["row_id"], values))

print("MASTER: Matrix A")
for row in matrix_a:
    print(row)

# SCATTER: Send rows to workers
print("\nMASTER: Sending rows to workers...")

with ThreadPoolExecutor(max_workers=4) as executor:
    result = list(executor.map(multiply_row, matrix_a))

# GATHER: Collect results
print("\nMASTER: Final Matrix A x B")

for row in result:
    print(row)