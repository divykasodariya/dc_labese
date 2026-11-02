import csv 
# import PathLib as pb
import pathlib as Path
 
CSV="b.CSV"
def main():
    nodes = []
    with open(CSV,newline="") as f :
        
        for row in csv.DictReader(f):
            nodes.append(
                {
                    "nodeid":int(row["nodeid"]),
                    "clock":int(row["clock"]),
                    "ismaster":bool(row["ismaster"])
                }
            )
    totaldiff=int(0)
    master={}
    for node in nodes :
        if node['ismaster']:
            master=node
            break
    #master node reqs clock from every other node and then calculates  final clock
    masterclk=master['clock']
    for node in nodes: 
        totaldiff= totaldiff + (node['clock']- masterclk)

    avgtotaldiff = totaldiff/len(nodes)
    finalclock = masterclk+ avgtotaldiff
    print(f"finalclock : {finalclock}")


if __name__ == "__main__":
    main()



        