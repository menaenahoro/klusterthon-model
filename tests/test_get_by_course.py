from src.api.internal_api import ApiRequest

api_request = ApiRequest()
data = api_request.get_user_by_course_id("65616501b382b3456c422477")
print(data)

