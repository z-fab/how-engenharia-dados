#%%

## TODO: Alterar Readme, Ajustar para gerar dados entre dois periodos, ajustar save para JSON, ajustar formato dados, BUCKET e GLUE via Cloudform


import logging
import datetime
import time
from schedule import repeat, every, run_pending
from writer import BucketWriter
from ingestor import OrderIngestor


from dotenv import load_dotenv


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":            
    load_dotenv('.env')
    
    logger.info(f"Start Generate data and send to S3...")
    order_ingestor = OrderIngestor(
        writer=BucketWriter,
        default_start_date=datetime.date(2023, 6, 25)
    )
    
    order_ingestor.ingest()

    @repeat(every(1).seconds)
    def job():
        order_ingestor.ingest()
                    
    while True:
        run_pending()
        time.sleep(0.5)