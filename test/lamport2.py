import csv 

CSV=lp.csv

def main():
    events=[]
    with open(CSV,newline="") as f :
        for row in csv.DictReader(f):
            events.append(row)
    
    clocks={}
    messages={}
    results=[]

    for event in events :
        eid = event['event_id']
        process = event['process']
        kind = event['kind']
        peer = event['peer']

        if process not in clocks : 
            clocks[process]=0
        
        old =clocks[process]

        if kind == 'send':

            clocks[process]+=1
            timestamp = clocks[process]
            key = (process ,peer)
            results.append((process, eid , kind , timestamp ))

            if( key not in messages or not messages[key]):
                messages[key]=[]
            
            messages[key].append(timestamp)

        elif kind =='recieve':
            key = (peer , process)
            if key not in messages :
                return;
            recieved = messages[key].pop(0)
            clocks[process] = max(recieved,old)+1 
            timestamp = clocks[process]
            results.append((process, eid , kind , timestamp ))
        else :
            clocks[process]+=1
            timestamp = clocks[process]
            results.append((process, eid , kind , timestamp ))



    print(clocks)

if __name__=="__main__":
    main()