import logging
import json
import os
from src.service.model_service import ModelService
from src.queue.queue_handler import Boto3Class

logger = logging.getLogger()
logger.setLevel(logging.INFO)
boto_3 = Boto3Class()
model_service = ModelService()


def lambda_handler(event, context):
    logger.info(event)
    if "body" in event:
        body = event["body"]
        json_body = json.loads(body)
        url_for = json_body.get('url_for')
        user_id = json_body.get('user_id')
        course_id = json_body.get('course_id')

    else:
        url_for = event.get('url_for')
        user_id = event.get('user_id')
        course_id = event.get('course_id')

    if url_for=="queue":
        result =  boto_3.send_message_queue(user_id=user_id, course_id=course_id)

        # Model to process function
        return dict(message="successful", error=False, data=[result])
    

    if url_for=="get_queue":
        result =  boto_3.get_queue(course_id=course_id)

        # Model to process function
        return dict(message="successful", error=False, data=[result])

    if url_for=="model_service":
        result = model_service.run_main_process(user_id=user_id, course_id=course_id)
        # Model to process function
        return dict(message="successful", error=False, data=result)

    if url_for=="event_bridge":
        try:
            result = model_service.run_main_process(user_id=user_id, course_id=course_id)
            return dict(message="successful", error=False, data=result)
        except Exception as e:
            return dict(error=True, message=f'error: {e}')
        # Model to process function
        return dict(message="successful", error=False, data=result)


