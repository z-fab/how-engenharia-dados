import argparse
import logging
import datetime
import time

from dotenv     import load_dotenv
from schedule   import repeat, every, run_pending
from writer     import BucketWriter, LocalWriter
from ingestor   import OrderIngestor



parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("--start", "-s", help='Start Date. Format YYY-MM-DD', default='2023-06-01')
parser.add_argument("--end", "-e", help='End Date. Format YYY-MM-DD', default='2023-06-31')
parser.add_argument("--type", "-t", help='Save to Local or S3', default='local')

args = parser.parse_args()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":            
    load_dotenv('.env')
    
    logger.info(f"Start Generate data and saving...")
    order_ingestor = OrderIngestor(
        writer=(BucketWriter if args.type == 'S3' else LocalWriter),
        start_date=datetime.datetime.strptime(args.start, "%Y-%m-%d").date(),
        end_date=datetime.datetime.strptime(args.end, "%Y-%m-%d").date()
    )
    
    order_ingestor.ingest()

    @repeat(every(1).seconds)
    def job():
        order_ingestor.ingest()
                    
    while True:
        run_pending()
        time.sleep(0.5)