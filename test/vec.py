
import csv
import os

CSV = "vector_events.csv"

PROCESSES = ["P1", "P2", "P3"]

# Create CSV if it doesn't exist
if not os.path.exists(CSV):
    with open(CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["event_id", "process_id", "event_action", "target_process"])
        w.writerows([
            ["E1", "P1", "SEND", "P2"],
            ["E2", "P2", "RECEIVE", "P1"],
            ["E3", "P2", "LOCAL", ""],
            ["E4", "P3", "LOCAL", ""],
            ["E5", "P1", "LOCAL", ""]
        ])

# Read CSV
events = []

with open(CSV, "r") as f:
    for row in csv.DictReader(f):
        events.append(row)

# Initialize vector clocks
clocks = {}

for p in PROCESSES:
    clocks[p] = [0, 0, 0]

messages = {}
results = []

# Process events
for e in events:

    eid = e["event_id"]
    process = e["process_id"].strip()
    kind = e["event_action"].strip().upper()
    peer = e["target_process"].strip()

    if process not in clocks:
        print("Unknown process:", process)
        break

    index = PROCESSES.index(process)

    # SEND
    if kind == "SEND":

        clocks[process][index] += 1

        timestamp = clocks[process].copy()

        key = (process, peer)

        if key not in messages:
            messages[key] = []

        messages[key].append(timestamp)

        print(eid, process, "SEND to", peer, "Clock:", timestamp)

    # RECEIVE
    elif kind == "RECEIVE":

        key = (peer, process)

        if key not in messages or not messages[key]:
            print("No matching message found!")
            break

        received = messages[key].pop(0)

        # Merge received vector with local vector
        for i in range(len(PROCESSES)):
            clocks[process][i] = max(clocks[process][i], received[i])

        # Increment own component
        clocks[process][index] += 1

        timestamp = clocks[process].copy()

        print(eid, process, "RECEIVE from", peer, "Clock:", timestamp)

    # LOCAL
    elif kind == "LOCAL":

        clocks[process][index] += 1

        timestamp = clocks[process].copy()

        print(eid, process, "LOCAL Clock:", timestamp)

    else:
        print("Invalid event:", kind)
        break

    results.append((eid, process, timestamp))


# Compare event vectors
print("\nCausal Ordering:")

for i in range(len(results)):
    for j in range(i + 1, len(results)):

        id1, p1, v1 = results[i]
        id2, p2, v2 = results[j]

        if all(v1[k] <= v2[k] for k in range(3)) and any(v1[k] < v2[k] for k in range(3)):
            print(id1, "->", id2, "(Causally Precedes)")

        elif all(v2[k] <= v1[k] for k in range(3)) and any(v2[k] < v1[k] for k in range(3)):
            print(id2, "->", id1, "(Causally Precedes)")

        elif v1 == v2:
            print(id1, "and", id2, "(Equal Vectors)")

        else:
            print(id1, "||", id2, "(Concurrent)")


print("\nFinal Vector Clocks:")

for p in PROCESSES:
    print(p, ":", clocks[p])
