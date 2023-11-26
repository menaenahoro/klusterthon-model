from src.lambda_handler import lambda_handler



event = dict(url_for="model_service", user_id="65609445ef691b001cd35b57", course_id="65616a96b382b3456c422479")


response = lambda_handler(event=event, context=None)

print(response)