from src.queue.queue_handler import Boto3Class
import json


boto_3 = Boto3Class()

# result =  boto_3.send_message_queue(user_id="6560f2385e7720001b01f3c9", course_id="65616d2ab382b3456c42247f")

result = boto_3.get_queue(course_id="65609445ef691b001cd35b57")

# result = boto_3.delete_bulk_messages(course_id="65616d2ab382b3456c42247f")

# result = boto_3.delete_message(receipt_handle="AQEBdOhTOQDHe5fGo1fMmFiGoZ29IaSHuED6B5KMMmeUpPJ5LUdk2HL7GgMUBtQBdR2bNg+5as/gBYjzCjjbpLnZhIUZH88VwPR+BUNQ4uNGp2RLZOSCtJEDvhXGIQ9qamTSZW0ZQCYfgzAbCjdyAswYfZyrdA5LJ9RwbFlp4cGFkGmS7lu73zPmpbQm87yL91J3zfkK4xsHM/90+5tkTmp9YB6iOUSI2sPSbaomQkJE61WZKj6r1Rmjwea8MRJYIPOqWDbmsqB+SbJy51/jRtwX8LKK7nqoJOITzUSZrYw3Nes=" ,course='data_science')




with open("sample_lambda_handler_00.json", "w") as outfile:
    json.dump(result, outfile)
