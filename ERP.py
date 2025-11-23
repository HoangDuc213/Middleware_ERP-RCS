import json

class ERPClientMQTT:
    def __init__(self, mqtt_client, topic):
        self.mqtt = mqtt_client
        self.topic = topic

    def send_task(self, task):
        print("\n[ERP] Publish → middleware/erp/task:", task)
        self.mqtt.publish(self.topic, json.dumps(task))
