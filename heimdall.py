import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import datetime
import logging
import os  

BROKER = os.environ['BROKER_IP']
BROKER_PORT = 1883

INFLUXDB = os.environ['INFLUX_IP']
INFLUXDB_PORT = 8086

def on_connect(client, userdata, flags, rc):
    logging.info("Connect received with code %d." % (rc))

def on_subscribe(client, userdata, mid, granted_qos):
    logging.info("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message_general(mosq, obj, msg):
    logging.info("Receive " + msg.topic + " value")

    current_time = datetime.datetime.utcnow().isoformat()
    json_body = [
        {
            "measurement": msg.topic,
            "tags": {},
            "time": current_time,
            "fields": {
                "value": msg.payload if msg.topic.find("relay") != -1 else int(msg.payload)
            }
        }
    ]
    try:
        influx_client.write_points(json_body)
        logging.info(json_body)
    except:
        logging.error("Error trying to connect to InfluxDB")
        quit()

logging.basicConfig(level = logging.INFO)

logging.info("BROKER IP: %s", BROKER)
logging.info("INFLUX IP: %s", INFLUXDB)

influx_client = InfluxDBClient(host=INFLUXDB, port=INFLUXDB_PORT, database="sensors")
client = mqtt.Client(client_id="heimdall")

client.on_connect = on_connect
client.connect(BROKER, BROKER_PORT, 60)

client.subscribe("esp32/#", qos=0)
client.on_message = on_message_general

client.loop_forever()
