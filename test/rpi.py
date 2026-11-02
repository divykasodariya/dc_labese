import csv
import pathlib as Path
CSV="rmi.csv"

def main():
    with open(CSV,newline="") as f :
        for col in csv.DictReader(f):
            method = col["method"]
            value = float(col['value'])
            print(f"client {col['client_name'] } called {method} with value = {value+3 } client id {col['client_id']} ")



if __name__ == "__main__":
    main()