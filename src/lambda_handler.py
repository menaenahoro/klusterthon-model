import logging
import json
import os

from src.queue.queue_handler import Boto3Class

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(event)
    if "body" in event:
        body = event["body"]
        json_body = json.loads(body)
        url_for = json_body.get('url_for')
        user_id = json_body.get('user_id')
        course = json_body.get('course')

    else:
        url_for = event.get('url_for')
        user_id = event.get('user_id')
        course = event.get('user_id')

    if url_for=="queue":
        boto_3 = Boto3Class()
        result =  boto_3.send_message_queue(user_id=user_id, course=course)

        # Model to process function
        return dict(message="successful", error=False)