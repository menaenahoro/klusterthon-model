
from src.api.internal_api import ApiRequest

api_request = ApiRequest()
users = api_request.get_user_array(["65609445ef691b001cd35b57", "6560f2385e7720001b01f3c9", "65600072c3ed16001c74d9c9"])

print(users)


