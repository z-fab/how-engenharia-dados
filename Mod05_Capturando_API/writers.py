import datetime
import json
import os

class DataTypeNotSupportedForIngestionException(Exception):
    
    def __init__(self, data: any) -> None:
        self.data = data
        self.message = f"Data type {type(self.data)} not supported for ingestion"
        super().__init__(self.message)
        
        
class DataWriter:
    
    def __init__(self, coin: str, api: str) -> None:
        self.coin = coin
        self.api = api
        self.filename = f"{self.api}/{self.coin}/{datetime.datetime.now()}.json"
        
    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, "a") as file:
            file.write(row)
            
    def write(self, data: list|dict):
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        elif isinstance(data, list):
            for elem in data:
                self.write(elem)
        else:
            raise DataTypeNotSupportedForIngestionException(data)