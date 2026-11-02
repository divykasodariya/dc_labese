import csv 
import pathlib as pb
CSV="bully.csv"
def main():
    nodes = []
    with open(CSV,newline="") as f:
        for r in csv.DictReader(f):
            nodes.append({
                "node":int(r['node']),
                "isalive":bool(r['alive']),
                "is_coordinator":bool(r['iscordi'])
            })
    alive =[]
    for node in nodes :
        if node["isalive"] : 
            alive.append(node)
    alive.sort(key=lambda n: n["node"])
    print("starting election ")
    cur =alive[0]
    for n in alive :
        for n2 in alive : 
            if n2['node']>n['node']:
                print(f"node {n["node"]} to node {n2["node"]} : ELECTION")
                
    ans = alive[-1]
    print(f"final coordinator : {ans}")
    

    print("coordinator broadcast")
    for n in alive :
        if n!=ans :
            print(f"coodinator to node {node}") 

                
if __name__ == "__main__":
    main()