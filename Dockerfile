FROM public.ecr.aws/lambda/python:3.9 
## donwloading lambda image

# ADD requirements.txt .
COPY /requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# set environment variables
# The SENTRY_AUTH_TOKEN is used to upload the source maps to Sentry


ARG SQS_QUEUE_URL_DS
ARG SQS_QUEUE_URL_UI
ARG SQS_QUEUE_URL_BE
ARG SQS_QUEUE_URL_FE
ARG SQS_QUEUE_URL_PM
ARG SQS_QUEUE_URL
ARG ACCESS_KEY
ARG SECRET_KEY


ENV SQS_QUEUE_URL_DS=$SQS_QUEUE_URL_DS
ENV SQS_QUEUE_URL_UI=$SQS_QUEUE_URL_UI
ENV SQS_QUEUE_URL_BE=$SQS_QUEUE_URL_BE
ENV SQS_QUEUE_URL_FE=$SQS_QUEUE_URL_FE
ENV SQS_QUEUE_URL_PM=$SQS_QUEUE_URL_PM
ENV SQS_QUEUE_URL=$SQS_QUEUE_URL
ENV ACCESS_KEY=$ACCESS_KEY
ENV SECRET_KEY=$SECRET_KEY


COPY src ./src
#COPY lambda_function.py .

CMD [ "src.lambda_handler.lambda_handler" ]

