from src.lambda_handler import lambda_handler



event = dict(url_for="model_service", user_id="65609445ef691b001cd35b57", course_id="65616d2ab382b3456c42247f")


response = lambda_handler(event=event, context=None)

print(response)