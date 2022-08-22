#AWS lambda function for api file upload to S3 bucket
#used with AWS API Gateway

import logging
import boto3
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')

def lambda_handler(event, context):

    #edit these:
    expectedToken = 'Bearer ' #generate a token and add at end of string
    bucketName = '' #bucket for file uploads

    
    goodResponse  = {
    'statusCode': 200,
    'headers': {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true'
    },
    'body': ''
    }

    badResponse = {
        'statusCode': 403,
        'body':'Unauthorized'
    }

    sourceIP = event['requestContext']['http']['sourceIp']
    
    # Access token
    token = event['headers']['authorization']
    
    # Date based folders
    # -original project called for uploads to be separated into year,month,day for later processing
    today = datetime.datetime.now()
    year = today.strftime('%Y')
    month = today.strftime('%-m')
    day = today.strftime('%-d')
    baseFolder = "upload/" + year + "/" + month + "/" + day + "/" 

    fileName = baseFolder + event['headers']['file-name']
    fileContent = event['body']
    
    if (token == expectedToken):
        logger.info(f"Accepted token from {sourceIP}")
        logger.info(f"File: {fileName}")
        try:
            s3_response = s3_client.put_object(Bucket=bucketName, Key=fileName, Body=fileContent)   
            logger.info('S3 Response: {}'.format(s3_response))
            goodResponse['body'] = 'Your file has been uploaded'
            return goodResponse

        except Exception as e:
            raise IOError(e)
    else:
        logger.error(f"Blocked request from {sourceIP}")
        return  badResponse
