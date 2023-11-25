


import os
import boto3
from src.config.config import (
    SQS_QUEUE_URL, SQS_QUEUE_URL_DS, SQS_QUEUE_URL_UI, SQS_QUEUE_URL_BE, SQS_QUEUE_URL_FE, 
    SQS_QUEUE_URL_PM, ACCESS_KEY, SECRET_KEY)
from datetime import datetime
# 'https://sqs.eu-west-1.amazonaws.com/091735408223/GroupingQueue'


class Boto3Class:
    def __init__(self):
        AWS_REGION="eu-west-1"
        self.sqs = boto3.client(
            'sqs', region_name=AWS_REGION, aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY,)

        self.dict_sqs_url = {
            'data_science':SQS_QUEUE_URL_DS,
            'ui_ux':SQS_QUEUE_URL_UI,
            'porduct_management':SQS_QUEUE_URL_PM,
            'frontend':SQS_QUEUE_URL_FE,
            'backend':SQS_QUEUE_URL_BE,
            'general':SQS_QUEUE_URL,
        }

    def send_message_queue(self, user_id, course=None):
        # Send message to SQS queue
        date = datetime.now()
        date_time = date.strftime("%Y-%m-%d, %H:%M:%S")
        response = self.sqs.send_message(
            QueueUrl=self.dict_sqs_url.get(course, SQS_QUEUE_URL),
            MessageAttributes={
                'User': {
                    'DataType': 'String',
                    'StringValue': user_id
                },
                'Date': {
                    'DataType': 'String',
                    'StringValue': date_time
                },
                'Course': {
                    'DataType': 'String',
                    'StringValue': course
                },
            },
            MessageBody=(
                f'{user_id}'
                f'{date_time}'
                f'{course}'
            ),MessageGroupId=course, MessageDeduplicationId=course
        )

        return response['MessageId']


    def get_queue(self, course=None):

        # Receive message from SQS queue
        response = self.sqs.receive_message(
            QueueUrl=self.dict_sqs_url.get(course, SQS_QUEUE_URL),
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=10,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0,
            WaitTimeSeconds=0,
        )

        message = response['Messages']
        # receipt_handle = message[0]['ReceiptHandle']
        # print('RECEIPT HANDLE  ',receipt_handle)
        return self.get_message_info(message, course)

    def delete_message(self, receipt_handle, course):

        # Delete received message from queue
        self.sqs.delete_message(
            QueueUrl=self.dict_sqs_url.get(course, SQS_QUEUE_URL),
            ReceiptHandle=receipt_handle
        )
        print('Received and deleted message: %s' % receipt_handle)

    def get_message_info(self, messages, course):
        user_id_list = [
                message.get('MessageAttributes', {}).get('User', {}).get('StringValue') for message in messages]
        receipt_handle = [message.get('ReceiptHandle', {}) for message in messages] 
        return dict(user_id_list=user_id_list, receipt_handle=receipt_handle, course=course)
        











"""
    def send_message_queue(self, user_id, course):

        # Send message to SQS queue
        date = datetime.now()
        date_time = date.strftime("%Y-%m-%d, %H:%M:%S")
        response = self.sqs.send_message(
            QueueUrl=self.dict_sqs_url.get(course, SQS_QUEUE_URL),
            DelaySeconds=10,
            MessageAttributes={
                'User': {
                    'DataType': 'String',
                    'StringValue': user_id
                },
                'Date': {
                    'DataType': 'String',
                    'StringValue': date_time
                },
                'Course': {
                    'DataType': 'String',
                    'StringValue': course
                },
            },
            MessageBody=(
                f'{user_id}'
                f'{date_time}'
                f'{course}'
            ),MessageGroupId='586474de88e03', MessageDeduplicationId='586474de88e03'
        )

        print(response['MessageId'])


    def get_queue(self, course):

        # Receive message from SQS queue
        response = self.sqs.receive_message(
            QueueUrl=self.dict_sqs_url.get(course, SQS_QUEUE_URL),
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=10,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0,
            WaitTimeSeconds=0
        )

        message = response['Messages']
        receipt_handle = message[0]['ReceiptHandle']
        print('RECEIPT HANDLE  ',receipt_handle)
        print(message)

    def delete_message(self, receipt_handle, course):

        # Delete received message from queue
        self.sqs.delete_message(
            QueueUrl=self.dict_sqs_url.get(course, SQS_QUEUE_URL),
            ReceiptHandle=receipt_handle
        )
        print('Received and deleted message: %s' % message)

"""