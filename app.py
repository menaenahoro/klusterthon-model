# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS

import logging
import json
import os
from src.service.model_service import ModelService
from src.queue.queue_handler import Boto3Class

logger = logging.getLogger()
logger.setLevel(logging.INFO)
boto_3 = Boto3Class()
model_service = ModelService()
 



app = Flask(__name__)
CORS(app)

 
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.

@app.route('/login',methods = ['POST', 'GET'])
# ‘/’ URL is bound with hello_world() function.
def hello_world(user_id, course_id):
        # get the post data
        request_data = json.loads(request.data)
        #check if user exists
        user_id = request_data.get('user_id')
        course_id = request_data.get('course_id')
        result = model_service.run_main_process(user_id=user_id, course_id=course_id)
        # Model to process function
        return {"message":"successful", "error":False, "data":result, 'headers': {
        'Access-Control-Allow-Origin': '*'},} 
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()