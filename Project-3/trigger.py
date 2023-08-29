import json
import os
import boto3
import threading


# Initializing all clients and services
sqs = boto3.client('sqs', region_name='us-east-1')
awslambda = boto3.client('lambda', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')
input_sqs_queue = 'https://sqs.us-east-1.amazonaws.com/458362110587/ndk-request-queue'
output_sqs_queue = 'https://sqs.us-east-1.amazonaws.com/458362110587/ndk-response-queue'
lambda_function_name = 'cs546-proj2-container'

def receive_output_messages():
    while True:
        response = sqs.receive_message(QueueUrl=output_sqs_queue, MaxNumberOfMessages=1, VisibilityTimeout=20, MessageAttributeNames=['All'], WaitTimeSeconds=20)

        if 'Messages' in response:
            try:
                message = response['Messages'][0]
                receipt_handle = message['ReceiptHandle']
                msg_body = json.loads(message['Body'])
                bucket_name = msg_body['Records'][0]['s3']['bucket']['name']
                key_name = msg_body['Records'][0]['s3']['object']['key']
                if os.path.exists(f'/home/ubuntu/{key_name}'):
                    os.remove(f'/home/ubuntu/{key_name}')
                s3.download_file(bucket_name, key_name, f'/home/ubuntu/{key_name}')
                try:
                    message_content = None
                    with open(f'/home/ubuntu/{key_name}', 'r') as file:
                        message_content = file.read()
                        print(f'{key_name} : {message_content}')
                except Exception as e:
                    print('Error reading file:', e)
                sqs.delete_message(QueueUrl=output_sqs_queue, ReceiptHandle=receipt_handle)
            except Exception as e:
                print('Error:', e)

# sqs_thread = threading.Thread(target=receive_output_messages)
# sqs_thread.start()

def receive_input_messages():
    while True:
        response = sqs.receive_message(QueueUrl=input_sqs_queue, MaxNumberOfMessages=1, VisibilityTimeout=20, MessageAttributeNames=['All'], WaitTimeSeconds=20)

        if 'Messages' in response:
            for message in response['Messages']:
                try:
        
                    s3_key = message['Body']
                    awslambda.invoke(
                        FunctionName=lambda_function_name,
                        InvocationType='Event',
                        Payload=s3_key
                    )
                    sqs.delete_message(QueueUrl=input_sqs_queue, ReceiptHandle=message['ReceiptHandle'])
                except Exception as e:
                    print('Error', e)
input_thread = threading.Thread(target=receive_input_messages)
output_thread = threading.Thread(target=receive_output_messages)
input_thread.start()
output_thread.start()