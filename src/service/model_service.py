from src.queue.queue_handler import Boto3Class
from src.api.internal_api import ApiRequest
from src.model.model_kmeans import Clustering
from src.model.model_svm import SVMModel
import time


class ModelService:

    def __init__(self) -> None:
        self.boto_3 = Boto3Class()
        self.api_request = ApiRequest()
        pass

    def run_main_process(self, user_id, course_id):
        # GET OPEN GROUP DETAILS
        """A group is open if the number of users are lesser than or equals to 5"""
        data = None#self.api_request.get_user_by_course_id(course_id)

        if data:
            new_user = self.api_request.get_user_details(user_id)
            svm_model = SVMModel()
            group_id = svm_model.train_model_response(data, new_user)
            print(group_id)
            print("Adding user to existing user groups")
            response = self.api_request.add_user_to_group(user_id, course_id, group_id)
            print(f"Added user: {user_id} to user group: {group_id}")
            return response
        
        print("All available user groups have reached full capacity")
        # ADD USER TO QUEUE
        self.add_user_to_queue(user_id, course_id)
        print("user: {user_id} has been added to queue")

        time.sleep(3)
        
        # Run queue
        self.check_queue_and_run(course_id)
        return 

    def add_user_to_queue(self,user_id, course_id):
        result = self.boto_3.send_message_queue(user_id=user_id, course_id=course_id)
    
    def retrieve_current_queue(self, course_id):
        user_list = self.boto_3.get_queue(course_id)
        return user_list

    def run_process_24hr(self, user_list):

        # retrieve data from db
        data = self.api_request.get_user_array(user_list)

        # model response
        cluster = Clustering(data)
        result = cluster.process_data()

        data = result.to_dict(orient='records')

        # Create a dictionary to store user_ids for each cluster
        clusters = {}

        # Iterate through the data and organize user_ids into their respective clusters
        for item in data:
            cluster = item['cluster']
            user_id = item['user_id']

            # If the cluster is not in the dictionary, add it
            if cluster not in clusters:
                clusters[cluster] = []

            # Append the user_id to the respective cluster
            clusters[cluster].append(user_id)

        for key, lists in clusters.items():
            print(lists)
            response = self.api_request.create_user_groups(user_id_list=lists, course_id=course_id)
            return response
            #call create group function
    
    def check_queue_and_run(self, course_id):
        # retrieve current queue
        print(f"retrieving queue data for course id: {course_id}")
        user_list = self.retrieve_current_queue(course_id)

        # if users on on is greater or equals to 10 run model and create group
        if user_list>=10:
            # function to delete users from queue
            result = boto_3.delete_bulk_messages(course_id=course_id)
            self.run_process_24hr(user_list)
        else:
            print("Queue not at maximum capacity")

        

