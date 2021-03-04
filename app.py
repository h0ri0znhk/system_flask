from flask import Flask
import psutil
import json

app = Flask(__name__)

class SystemStats:
    def __init__(self):
        self.cpu_percent = psutil.cpu_percent()

        self.virtual_memory = psutil.virtual_memory().percent

        network = psutil.net_if_addrs()
        self.network = dict()
        for i in network:
            if i != 'lo':
                self.network[i] = network[i][0].address

        sensors = psutil.sensors_temperatures()
        self.sensors = dict()
        for i in sensors:
            self.sensors[i] = list()
            for j in sensors[i]:
                self.sensors[i].append({j.label: j.current})

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

@app.after_request
def apply_caching(response):
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/')
def get():
    p1 = SystemStats()
    return p1.to_json()

if __name__ == '__main__':
    app.run()
