import boto3
import logging
from botocore.exceptions import ClientError


class AWSS3Controller:

    def __init__(self, config):
        boto3.setup_default_session(aws_access_key_id=config['aws_access_key_id'],
                                    aws_secret_access_key=config['aws_secret_access_key'])
        self.s3_client = boto3.client('s3')

    def upload_to_s3(self, file_name, bucket, object_name=None, args=None):
        if object_name is None:
            object_name = file_name
        # Upload the file
        try:
            print('Uploading file to S3: ' + bucket + ' ' + object_name + ' ' + file_name)
            response = self.s3_client.upload_file(file_name, bucket, object_name, ExtraArgs=args)
        except ClientError as e:
            logging.error(e)
            return False
        return True
