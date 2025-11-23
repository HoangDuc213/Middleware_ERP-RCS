import json
import time
import threading

class RCSClientMQTT:
    def __init__(self, mqtt_client, task_topic, feedback_topic):
        self.mqtt = mqtt_client
        self.task_topic = task_topic
        self.feedback_topic = feedback_topic

    def simulate_robot(self, task):
        print("\n[RCS] Robot nhận nhiệm vụ:", task)
        print("[RCS] Robot đang thực hiện...")

        time.sleep(2)

        feedback = {
            "id": task["id"],
            "status": "completed",
            "duration": 12.5
        }

        print("[RCS] Publish → rcs/feedback:", feedback)
        self.mqtt.publish(self.feedback_topic, json.dumps(feedback))

    def on_task_received(self, payload):
        task = json.loads(payload)
        threading.Thread(target=self.simulate_robot, args=(task,)).start()
