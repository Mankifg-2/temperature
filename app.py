from flask import Flask,render_template,url_for,request,redirect, make_response
import random
import json
import time
import random 
from flask import Flask, render_template, make_response
import os
import glob
import time
 
os.system('sudo modprobe w1-gpio')
os.system('sudo modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
'''
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
'''



dir1 = f"{base_dir}28-0118762581ff/w1_slave"
dir2 = ""


def read_temp_raw(dir):
    f = open(dir, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp(dir):
    lines = read_temp_raw(dir)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(dir)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
        



app = Flask(__name__)

def getdata1():
    return read_temp(dir1)


def getdata2():
    return random.randint(10,40)

@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')


@app.route('/data', methods=["GET", "POST"])
def data():
    data = [time.time() * 1000, getdata1(dir1)]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/data2', methods=["GET", "POST"])
def data2():
    data2 = [time.time() * 1000, getdata2(dir2)]
    response2 = make_response(json.dumps(data))
    response2.content_type = 'application/json'
    return response2


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
