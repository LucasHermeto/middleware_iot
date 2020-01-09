from flask import render_template
from flask import request
from flask import jsonify
from flask import redirect
from app import app

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import json

# MQTT = "172.27.9.216" # IP at "IoT-Projects Network"
MQTT = "localhost"
MQTT_PORT = 1883

INFLUXDB = "localhost"
INFLUXDB_PORT = 8086

client = mqtt.Client(client_id="hermodr")
influx_client = InfluxDBClient(
    host=INFLUXDB, port=INFLUXDB_PORT, database="sensors")

query_temperature = "SELECT value FROM \"esp32/temperature\" ORDER BY time DESC LIMIT 1"
query_humidity = "SELECT value FROM \"esp32/humidity\" ORDER BY time DESC LIMIT 1"
query_relay = "SELECT value FROM \"esp32/relay\" ORDER BY time DESC LIMIT 1"
query_potenciometer = "SELECT value FROM \"esp32/potenciometer\" ORDER BY time DESC LIMIT 1"

def get_humidity():
    result = influx_client.query(query_humidity)
    for item in result.get_points():
        return {"value": item['value']}

def get_temperature():
    result = influx_client.query(query_temperature)
    for item in result.get_points():
        return {"value": item['value']}

def get_relay():
    result = influx_client.query(query_relay)
    for item in result.get_points():
        return {"value": item['value']}

def get_potenciometer():
    result = influx_client.query(query_potenciometer)
    for item in result.get_points():
        return {"value": item['value']}

@app.route('/')
@app.route('/index')
def index(): 
    return render_template('index.html',
        temp=get_temperature(), humid=get_humidity(),
        relay=get_relay(), pot=get_potenciometer())

@app.route('/api/humidity', methods=['GET'])
def humidity():
    return jsonify(get_humidity())

@app.route('/api/temperature', methods=['GET'])
def temperature():
    return jsonify(get_temperature())

@app.route('/api/alert/relay', methods=['POST'])
def alert_relay():
    data = request.form

    if (data['status'] != "on" and data['status'] != "off"):
        print("ERROR")
        return redirect("/")

    client.connect(MQTT, MQTT_PORT, 60)
    client.publish(topic="esp32/alert/relay",
                   payload=data['status'], retain=True)
    return redirect("/")

@app.route('/api/alert/potenciometer', methods=['POST'])
def alert_potenciometer():
    data = request.form
    level = int(data['level'])

    if (level > 255 or level < 0):
        return jsonify({'error': "Input not valid"})

    client.connect(MQTT, MQTT_PORT, 60)
    client.publish(topic="esp32/alert/potenciometer",
                   payload=level, retain=True)
    return redirect("/")

@app.route('/api/alert/control', methods=['POST'])
def alert_control():
    data = request.form

    if (data['status'] != "on" and data['status'] != "off"):
        return jsonify({'error': "Input not valid"})

    client.connect(MQTT, MQTT_PORT, 60)
    client.publish(topic="esp32/alert/control",
                   payload=data['status'], retain=True)
    return redirect("/")
