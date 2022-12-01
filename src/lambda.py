import json
import boto3

s3 = boto3.resource('s3')
rekognition = boto3.client('rekognition')


def extractLabels(image, bucket):
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': image
            }
        }
    )
    return response


def detectPersons(labels):
    numberOfPersons = 0
    for label in labels:
        label_name = label['Name']
        if "Person" in label_name:
            numberOfPersons += len(label['Instances'])
    return numberOfPersons


def lambda_handler(event, context):

    # Traer datos de la imagen puesta en S3
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        image = record['s3']['object']['key']
        imageScan = extractLabels(image, bucket)
        print(image, ":", detectPersons(imageScan['Labels']))

    return {
        'statusCode': 200,
    }
