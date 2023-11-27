


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
            '65616d2ab382b3456c42247f':SQS_QUEUE_URL_DS,
            '65616c6cb382b3456c42247d':SQS_QUEUE_URL_UI,
            '65616501b382b3456c422477':SQS_QUEUE_URL_PM,
            '65616a96b382b3456c422479':SQS_QUEUE_URL_FE,
            '65616b81b382b3456c42247b':SQS_QUEUE_URL_BE,
            'general':SQS_QUEUE_URL,
        }

    def send_message_queue(self, user_id, course_id=None):
        # Send message to SQS queue
        date = datetime.now()
        response = self.sqs.send_message(
            QueueUrl=self.dict_sqs_url.get(course_id, SQS_QUEUE_URL),
            MessageAttributes={
                'User': {
                    'DataType': 'String',
                    'StringValue': user_id
                },
                'CourseId': {
                    'DataType': 'String',
                    'StringValue': course_id
                },
            },
            MessageBody=(
                f'{user_id}'
                f'{course_id}'
            ),MessageGroupId=course_id, MessageDeduplicationId=course_id
        )

        return response['MessageId']


    def get_queue(self, course_id=None):

        # Receive message from SQS queue
        response = self.sqs.receive_message(
            QueueUrl=self.dict_sqs_url.get(course_id, SQS_QUEUE_URL),
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=10,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=30,
            WaitTimeSeconds=10,
        )

        # message = response['Messages']
        # receipt_handle = message[0]['ReceiptHandle']
        # print('RECEIPT HANDLE  ',receipt_handle)
        # result = self.get_message_info(message, course_id)
        # user_id_list = result.get('user_id_list', [])
        return response

    def delete_message(self, receipt_handle, course_id):

        # Delete received message from queue
        self.sqs.delete_message(
            QueueUrl=self.dict_sqs_url.get(course_id, SQS_QUEUE_URL),
            ReceiptHandle=receipt_handle
        )
        print('Received and deleted message: %s' % receipt_handle)

    def delete_bulk_messages(self, course_id):
        response = self.sqs.receive_message(
            QueueUrl=self.dict_sqs_url.get(course_id, SQS_QUEUE_URL),
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=10,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=30,
            WaitTimeSeconds=10,
        )

        messages = response['Messages']

        # # transform data
        # message_to_delete = [dict(Id=i.get('MessageId'), ReceiptHandle=i.get('ReceiptHandle'), VisibilityTimeout=30) for i in messages]
        # print(self.dict_sqs_url.get(course_id, SQS_QUEUE_URL))

        # # Change Visibility timeout

        # response = self.sqs.change_message_visibility_batch(
        #     QueueUrl=self.dict_sqs_url.get(course_id, SQS_QUEUE_URL),
        #     Entries=message_to_delete
        # )

        message_to_delete = [dict(Id=i.get('MessageId'), ReceiptHandle=i.get('ReceiptHandle')) for i in messages]

        # Delete messages batch
        response = self.sqs.delete_message_batch(
            QueueUrl=self.dict_sqs_url.get(course_id, SQS_QUEUE_URL),
            Entries=message_to_delete
        )
        return response


    def get_message_info(self, messages, course_id):
        user_id_list = [
                message.get('MessageAttributes', {}).get('User', {}).get('StringValue') for message in messages]
        receipt_handle = [message.get('ReceiptHandle', {}) for message in messages] 
        return dict(user_id_list=user_id_list, receipt_handle=receipt_handle, course_id=course_id)
        











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