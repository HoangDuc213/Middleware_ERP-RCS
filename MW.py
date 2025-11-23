import json

class MiddlewareMQTT:
    def __init__(self, mqtt_client, erp_topic, rcs_topic):
        self.mqtt = mqtt_client
        self.erp_topic = erp_topic
        self.rcs_topic = rcs_topic

    def receive_from_erp(self, data):
        print("\n[MIDDLEWARE] Nhận yêu cầu ERP:", data)
        task = self._map_erp_to_rcs(data)
        self.send_to_rcs(task)

    def receive_from_rcs(self, data):
        print("\n[MIDDLEWARE] Nhận phản hồi RCS:", data)
        erp_data = self._map_rcs_to_erp(data)
        self.send_to_erp(erp_data)

    def send_to_rcs(self, task):
        print("[MIDDLEWARE] Publish → rcs/task:", task)
        self.mqtt.publish(self.rcs_topic, json.dumps(task))

    def send_to_erp(self, data):
        print("[MIDDLEWARE] Publish → erp/feedback:", data)
        self.mqtt.publish(self.erp_topic, json.dumps(data))

    def _map_erp_to_rcs(self, data):
        return {
            "id": data["task_id"],
            "from": data["pickup"],
            "to": data["dropoff"]
        }

    def _map_rcs_to_erp(self, data):
        return {
            "task_id": data["id"],
            "status": data["status"],
            "time": data.get("duration", 0)
        }
