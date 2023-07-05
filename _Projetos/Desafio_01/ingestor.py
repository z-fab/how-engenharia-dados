from abc import ABC, abstractmethod
import datetime
import logging
from writer import DataWriter
from generator import OrderData

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DataIngestor(ABC):
        
    def __init__(self, writer:DataWriter, default_start_date: datetime.date) -> None:
        self.default_start_date = default_start_date
        self.writer = writer
        self._checkpoint = self._load_checkpoint()
    
    @property
    def _checkpoint_filename(self) -> str:
        return f"{self.__class__.__name__}.checkpoint"
    
    def _write_checkpoint(self):
        with open(self._checkpoint_filename, "w") as file:
            file.write(str(self._checkpoint))
            
    def _load_checkpoint(self) -> datetime.date:
        try:
            with open(self._checkpoint_filename, "r") as file:
                return datetime.datetime.strptime(file.read(), "%Y-%m-%d").date()
        except FileNotFoundError:
            return None
        
    def _get_checkpoint(self):
        if not self._checkpoint:
            return self.default_start_date
        return self._checkpoint
    
    def _update_checkpoint(self, value):
        self._checkpoint = value
        self._write_checkpoint()
    
    @abstractmethod
    def ingest(self) -> None:      
        pass


class OrderIngestor(DataIngestor):
    
    def __init__(self, writer: DataWriter, default_start_date: datetime.date) -> None:
        super().__init__(writer, default_start_date)
        self.default_start_date = default_start_date
        self.writer = writer
        self.schema_name = 'marketplace'
        self.table_name = 'order'
    
    
    def ingest(self) -> None:
        date = self._get_checkpoint()
        if date < datetime.date.today():
            logger.info(f"Start Ingestion to S3 -> {date}")
            order_data = OrderData()
            data = order_data.get_data(date=date)
            self.writer(schema_name = self.schema_name, table_name = self.table_name).write(data=data, date=date)
            self._update_checkpoint(date + datetime.timedelta(days=1))