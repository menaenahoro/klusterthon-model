import os
from src.config.config import (GROUP_BEARER_TOKEN, DEV_URL)
from typing import List
import requests
import json

class ApiRequest:
    no_groups=False

    def create_user_groups(self, user_id_list:List, course_id):
        """
        Function to create user groups for a specific course.

        This function sends a POST request to a given URL with the user IDs and course ID.
        It is used to create groups of users enrolled in a specific course.

        :param user_id_list: List of user IDs to be grouped.
        :param course_id: The ID of the course for which the groups are being created.
        :return: The response from the server after attempting to create the groups.
        """

        url = f"{DEV_URL}/chat/group"

        headers = {
            'Authorization': f'Bearer {GROUP_BEARER_TOKEN}',
            'Content-Type': 'application/json'
        }

        data = {
            'courseId': course_id,
            'userIds': user_id_list
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.json()


    def add_user_to_group(self, user_id, course_id, group_id):
        """
        Function to add a user groups to a specific study group.

        This function sends a POST request to a given URL with the user IDs and course ID.
        It is used to add a user to study groups of users enrolled in a specific course.

        :param user_id: user ID
        :param course_id: The ID of the course for which the group is.
        :param group_id: the groups ID.
        :return: The response from the server after attempting to create the groups.
        """

        url = f"{DEV_URL}/chat/groups/addUsers"

        headers = {
            'Authorization': f'Bearer {GROUP_BEARER_TOKEN}',
            'Content-Type': 'application/json'
        }

        data = {
            'groupId': group_id,
            'courseId': course_id,
            'userIds': [user_id]
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.json()

    
    def get_user_array(self, user_id_list:List):
        """
        Function to retrieve user details based on a list of user IDs.

        This function sends a GET request to the specified URL with a list of user IDs.
        It is used to fetch an array of user details from the server.

        :param user_id_list: List of user IDs for which details are to be fetched.
        :return: Processed list of user details, after processing the server response.
        """

        url = f"{DEV_URL}/user/array/users" 
        headers =  {'Content-Type': 'application/json'}
        data = {
            'userIds': user_id_list
        }
        response = requests.get(url, headers=headers, data=json.dumps(data))
        return self.process_get_user_array(response.json())

    def get_user_details(self, user_id:str):
        """
        Function to retrieve user details based on a user ID.

        This function sends a GET request to the specified URL with a user ID.
        It is used to fetch user details from the server.

        :param user_id: user ID for which details are to be fetched.
        :return: Processed list of user details, after processing the server response.
        """

        url = f"{DEV_URL}/user/array/users" 
        headers =  {'Content-Type': 'application/json'}
        data = {
            'userIds': [user_id]
        }
        response = requests.get(url, headers=headers, data=json.dumps(data))
        return self.process_get_user_array(response.json())


    def get_user_by_course_id(self, course_id):
        """
        Function to retrieve user details for a specific course ID.

        This function sends a GET request to a predefined URL with a course ID.
        It is used to obtain details of users enrolled in a particular course.

        :param course_id: The ID of the course for which user details are to be fetched.
        :return: Processed list of user details for the specified course, after processing the server response.
        """
        
        url = f"{DEV_URL}/user/course/user" 
        print("DEV_URL", DEV_URL)
        print("GROUP_BEARER_TOKEN", GROUP_BEARER_TOKEN)
        headers =  {'Content-Type': 'application/json'}
        data = {
            'courseId': f"{course_id}"
        }
        response = requests.get(url, headers=headers, data=json.dumps(data))
        response_data = response.json()
        
        # if no existing group
        if len(data)==0:
            self.no_groups = True
        data = self.combine_group_lists(self.filter_course_data(response_data))
        return data, self.no_groups
    

    def process_get_user_array(self, users):
        """
        Function to process data returned from get_user_array API route

        :param data: List of Dictionaries containing user details.
        :return: List of Dictionaries containing user details for modelling.
        """

        # Extracting the required information
        extracted_data = []
        for user in users:
            user_info = {
                "user_id": user.get("_id", None),
                "iqScore": user.get("scoringResult", {}).get("iqScore", None),
                "personalityScore": user.get("scoringResult", {}).get("personalityScore", None),
                "gender": user.get("demographics", {}).get("gender", None),
                "dateOfBirth": user.get("demographics", {}).get("dateOfBirth", None),
                "experience": user.get("learningInfo", {}).get("experience", None),
                "styles": user.get("learningInfo", {}).get("styles", None),
                "goals": user.get("learningInfo", {}).get("goals", None),
                "preference": user.get("learningInfo", {}).get("preference", None),
                "age": user.get("age", None),
                "language": user.get("analysis", {}).get("language", None)
            }
            extracted_data.append(user_info)
        return extracted_data


    def process_get_user_by_course_id(self, data):
        """
        Function to process data returned from get_user_by_course_id API route

        :param data: List of Dictionaries containing user details.
        :return: List of Dictionaries containing user details for modelling.
        """

        # Extracting the required information
        extracted_data = []
        for entry in data:
            extracted_info = {
                "user_id": entry.get("_id", None),
                "iqScore": entry.get("scoringResult", {}).get("iqScore", None),
                "personalityScore": entry.get("scoringResult", {}).get("personalityScore", None),
                "gender": entry.get("demographics", {}).get("gender", None),
                "dateOfBirth": entry.get("demographics", {}).get("dateOfBirth", None),
                "experience": entry.get("learningInfo", {}).get("experience", None),
                "styles": entry.get("learningInfo", {}).get("styles", None),
                "goals": entry.get("learningInfo", {}).get("goals", None),
                "preference": entry.get("learningInfo", {}).get("preference", None),
                "age": entry.get("age", None),
                "language": entry.get("analysis", {}).get("language", None)
            }
            extracted_data.append(extracted_info)
        return extracted_data


    def filter_course_data(self, data):
        # Extracting and organizing data by groupId
        grouped_data = {}
        for user in data:
            for group in user.get("chat", {}).get("groups", None):
                group_id = group.get("groupId", None)
                user_info = {
                    "user_id": user.get("_id", None),
                    "iqScore": user.get("scoringResult", {}).get("iqScore", None),
                    "personalityScore": user.get("scoringResult", {}).get("personalityScore", None),
                    "gender": user.get("demographics", {}).get("gender", None),
                    "dateOfBirth": user.get("demographics", {}).get("dateOfBirth", None),
                    "experience": user.get("learningInfo", {}).get("experience", None),
                    "styles": user.get("learningInfo", {}).get("styles", None),
                    "goals": user.get("learningInfo", {}).get("goals", None),
                    "preference": user.get("learningInfo", {}).get("preference", None),
                    "age": user.get("age", None),
                    "language": user.get("analysis", {}).get("language", None),
                    "groupId": group_id
                }
                if group_id not in grouped_data:
                    grouped_data[group_id] = []
                grouped_data[group_id].append(user_info)

        # Filter groups with less than 15 users
        filtered_groups = {group_id: users for group_id, users in grouped_data.items() if len(users) < 15}
        return filtered_groups

    # print(filtered_groups)

    def combine_group_lists(self, group_data):
        """
        Combine multiple lists of user details associated with the same group identifier.

        :param group_data: Dictionary where keys are group identifiers and values are lists of user details.
        :return: Dictionary with combined lists for each group identifier.
        """
        combined_groups = []

        for group_id, user_details in group_data.items():
            combined_groups.extend(user_details)

        return combined_groups

    


# course_id = 'course_123'
# user_ids = ['user1', 'user2', 'user3']

# response = make_post_request(course_id, user_ids)
# print(response.status_code)
# print(response.json())  # Assuming the response is in JSON format