import datetime
import pandas as pd


import boto3
from botocore import exceptions
from botocore.exceptions import ClientError

from abc import ABC, abstractmethod
from io import BytesIO
from os import getenv
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class DataWriter(ABC):
    
    def __init__(self, schema_name:str, table_name:str) -> None:
        self.filepath = f"{schema_name}/{table_name}/"
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id = getenv('AWS_ID'),
            aws_secret_access_key = getenv('AWS_KEY'),
        )
            
    @abstractmethod
    def write(self, data:pd.DataFrame, date:datetime.date):
        pass
    
class BucketWriter(DataWriter):
    
    def __init__(self, schema_name:str, table_name:str) -> None:
        super().__init__(schema_name, table_name)
        self.bucket = 'zfab-s3-bucket-how'
    
    def write(self, data:pd.DataFrame, date:datetime.date):
        full_path = self.filepath + f"date-order={date.strftime('%Y-%m-%d')}/{datetime.datetime.now()}.parquet"
        logger.info(f"Writing to S3 at {full_path}")
        out_buffer = BytesIO()
        data.to_parquet(out_buffer, index=False)
        self.s3_client.put_object(
            Body=out_buffer.getvalue(),
            Bucket=self.bucket,
            Key= full_path
        )