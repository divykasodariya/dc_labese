
import csv
import os

CSV = "events.csv"

# Create sample CSV
if not os.path.exists(CSV):
    with open(CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["event_id", "process_id", "event_type", "message_to", "initial_clock"])
        w.writerows([
            ["E1", "P1", "SEND", "P2", 0],
            ["E2", "P2", "RECEIVE", "P1", 0],
            ["E3", "P1", "LOCAL", "", 0],
            ["E4", "P2", "LOCAL", "", 0]
        ])

# Read CSV
events = []

with open(CSV, "r") as f:
    for row in csv.DictReader(f):
        events.append(row)

# Initialize
clocks = {}
messages = {}
results = []

# Process events
for e in events:

    eid = e["event_id"]
    process = e["process_id"]
    kind = e["event_type"].upper()
    peer = e["message_to"]

    if process not in clocks:
        clocks[process] = int(e["initial_clock"] or 0)

    old = clocks[process]

    # SEND
    if kind == "SEND":

        clocks[process] += 1
        timestamp = clocks[process]

        key = (process, peer)

        if key not in messages:
            messages[key] = []

        messages[key].append(timestamp)

        print(eid, process, "SEND to", peer, "Clock:", timestamp)

    # RECEIVE
    elif kind == "RECEIVE":

        key = (peer, process)

        if key not in messages or not messages[key]:
            raise SystemExit("ERROR: No matching message found!")

        received = messages[key].pop(0)

        clocks[process] = max(old, received) + 1

        timestamp = clocks[process]

        print(eid, process, "RECEIVE from", peer,
              "Message:", received, "Clock:", timestamp)

    # LOCAL
    elif kind == "LOCAL":

        clocks[process] += 1
        timestamp = clocks[process]

        print(eid, process, "LOCAL Clock:", timestamp)

    else:
        raise SystemExit("Invalid event type: " + kind)

    results.append((timestamp, process, eid, kind))

# Sort events by timestamp and process ID
results.sort()

print("\nFinal Total Order:")

for timestamp, process, eid, kind in results:
    print(eid, process, kind, "->", timestamp)

print("\nFinal Clocks:", clocks)
