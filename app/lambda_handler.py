import logging
import json
import os
from app.app import chatbot

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(event)
    if "body" in event:
        body = event["body"]
        json_body = json.loads(body)
        chat = json_body.get('chat')

    else:
        chat = event.get('chat')

    if chat:
        response = chatbot(chat)
        return dict(error=False, message="successful", data=response)
    
    return dict(error=True, message="unsuccessful", data=[])
