import paho.mqtt.client as mqtt
import json
from MW import MiddlewareMQTT
from ERP import ERPClientMQTT
from RCS import RCSClientMQTT

BROKER = "broker.emqx.io"
PORT = 1883

TOPIC_ERP_TO_MW = "middleware/erp/task"
TOPIC_MW_TO_RCS = "rcs/task"
TOPIC_RCS_TO_MW = "rcs/feedback"
TOPIC_MW_TO_ERP = "erp/feedback"


mqtt_client = mqtt.Client()

# Create the simulated RCS Class
rcs = RCSClientMQTT(mqtt_client, TOPIC_MW_TO_RCS, TOPIC_RCS_TO_MW)

# Create the middleware
middleware = MiddlewareMQTT(mqtt_client, erp_topic=TOPIC_MW_TO_ERP, 
                            rcs_topic=TOPIC_MW_TO_RCS)

# Create the simulated ERP Class
erp = ERPClientMQTT(mqtt_client, TOPIC_ERP_TO_MW)


def on_message(client, userdata, msg):
    """
    The callback for when a PUBLISH message is received from the server.
    
    :param client: the MQTT client instance for this callback
    :param userdata: the private user data as set in Client() or None
    :param msg: an instance of MQTTMessage. This is a class that contains
        the following fields: topic, payload, qos, retain.
    """

    payload = msg.payload.decode()
    print("\n[MQTT] Nhận:", msg.topic, payload)

    if msg.topic == TOPIC_ERP_TO_MW:
        middleware.receive_from_erp(json.loads(payload))

    elif msg.topic == TOPIC_RCS_TO_MW:
        middleware.receive_from_rcs(json.loads(payload))

    elif msg.topic == TOPIC_MW_TO_RCS:
        rcs.on_task_received(payload)


mqtt_client.on_message = on_message
mqtt_client.connect(BROKER, PORT, 60)

mqtt_client.subscribe(TOPIC_ERP_TO_MW)
mqtt_client.subscribe(TOPIC_MW_TO_RCS)
mqtt_client.subscribe(TOPIC_RCS_TO_MW)

mqtt_client.loop_start()

# Gửi 1 task mô phỏng
erp.send_task({
    "task_id": "T001",
    "pickup": "Zone A3",
    "dropoff": "Line 5"
})

input("\nNhấn ENTER để thoát...\n")
mqtt_client.loop_stop()
