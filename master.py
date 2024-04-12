from flask import Flask,request
import argparse
import json
import threading
import time
import requests
app = Flask(__name__) 
t = None
def checkAliveness(workers):
    print("Check aliveness",workers)
    aliveWorkers = []
    for worker in workers:
        try:
            response = requests.get(worker+"poll")
            print(response.text)
            if response.text == "1":
                aliveWorkers.append(worker)
        except Exception as e:
            print(e)
            continue
    return aliveWorkers

def allocateWork(websiteContent):
    allocatedWorkers = []
    with open('config.json') as configFile:
        configuration = json.loads(configFile.read())
        while(len(websiteContent)!=0):
            aliveWorkers = checkAliveness(configuration["workers"])
            print("Alive Workers",aliveWorkers)
            if len(aliveWorkers) ==0:
                time.sleep(configuration["workerAlivenessTimout"])
            else:
                while(len(aliveWorkers)!=0 and len(aliveWorkers) !=0):
                    worker = aliveWorkers.pop(0)
                    website = websiteContent.pop(0)
                    res = requests.post(worker+"scrape",json = website)
                    print("Allocated to:",worker)
                    allocatedWorkers.append(worker)
        print("Alocation Complete")
        while(len(allocatedWorkers)!=0):
            time.sleep(configuration['pollInterval'])
            for worker in allocatedWorkers:
                response = requests.get(worker+"poll")
                if response.text== "1":
                    allocatedWorkers.remove(worker)
                    print(allocatedWorkers)

@app.route('/poll')
def polling():
    if t == None:
        return "1"
    else:
        if t.is_alive() == True:
            return "0"
        else:
            return "1"

@app.route('/allocateWork',methods = ["POST"])
def getReq():
    global t
    content = request.json
    print(content)
    websiteContent = json.loads(content)
    t = threading.Thread(target=allocateWork,args=(websiteContent,))
    t.start()
    return "Done"

if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument("portno",type=int)
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.portno)