from src.config.config import GROUP_URL, GROUP_BEARER_TOKEN
from typing import List
import requests
import json

class Groups:

    def create_user_groups(user_id_list:List, course_id):
        url = f"{GROUP_URL}:id"  # Replace with your actual URL and endpoint

        headers = {
            'Authorization': f'Bearer {GROUP_BEARER_TOKEN}',
            'Content-Type': 'application/json'
        }

        data = {
            'courseId': course_id,
            'userIds': user_id_list
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response

# course_id = 'course_123'
# user_ids = ['user1', 'user2', 'user3']

# response = make_post_request(course_id, user_ids)
# print(response.status_code)
# print(response.json())  # Assuming the response is in JSON format