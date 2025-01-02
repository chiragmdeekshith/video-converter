from kafka import KafkaProducer
import cv2
import json
import base64
import logging


logging.basicConfig(level=logging.INFO)


def serialize_frame(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    frame_data = base64.b64encode(buffer).decode()
    return frame_data


producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

video = cv2.VideoCapture('test2.mp4')
frame_number = 0
topic_name = "video_topic"

while video.isOpened():
    success, frame = video.read()
    if not success:
        break

    frame_data = serialize_frame(frame)

    # Log each frame number
    logging.info(f"Sending frame {frame_number}")

    # Send frame to Kafka
    producer.send(topic_name, value={'frame_number': frame_number, 'data': frame_data})
    frame_number += 1
producer.send(topic_name, value={'data': 'EOF'})

video.release()
producer.close()
