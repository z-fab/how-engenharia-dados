from abc import ABC, abstractmethod
import datetime
import logging
import pandas as pd
import random
import faker as fk

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class GenerateData(ABC):

    def __init__(self, nrows:int = 100):
        self.nrows = nrows

    @abstractmethod
    def _generate(self, **kwargs) -> str:
        pass

    def get_data(self, **kwargs) -> dict:

        result = self._generate(**kwargs)
        return result
    

class OrderData(GenerateData):

    def _generate(self, date:datetime.date) -> str:
        
        logger.info(f"Generating data...")
        
        fake = fk.Faker('PT-BR')

        order_status = ['Delivered', 'Shipped', 'Canceled', 'Processing', 'Awaiting payment', 'Approved']
        payment_type = ['Credit Card', 'Debit Card', 'Boleto', 'PIX', 'PayPal', 'Gift Card']
        delivery_type = ['Comum', 'Sedex', 'Agendamento']
        fake_company = [fake.company() for _ in range(20)]
        
        df_temp = pd.DataFrame(
            {
                "date_order": [date for _ in range(self.nrows)],
                "seller": [random.choice(fake_company) for _ in range(self.nrows)],
                "customer": [fake.name() for _ in range(self.nrows)],
                "qtd_itens": [fake.random_int(min=1, max=15) for _ in range(self.nrows)],
                "order_value": [float(fake.random_int(min=100, max=99999)/100) for _ in range(self.nrows)],
                "freight_value": [float(fake.random_int(min=100, max=9999)/100) for _ in range(self.nrows)],
                "delivery_address": [fake.address() for _ in range(self.nrows)],
                "delivery_type": [random.choice(delivery_type) for _ in range(self.nrows)],
                "delivery_date": [fake.date_between(start_date='-1M') for _ in range(self.nrows)],
                "payment_type": [random.choice(payment_type) for _ in range(self.nrows)],
                "order_status": [random.choice(order_status) for _ in range(self.nrows)]
            }
        )
        
        df_temp['delivery_date'] = df_temp['date_order'].apply(
            lambda x: x + pd.Timedelta(days=fake.random_int(min=1, max=21))
        )
        
        df_temp['delivery_date'] = pd.to_datetime(df_temp['delivery_date'])
        df_temp['date_order'] = pd.to_datetime(df_temp['date_order'])
        
        return df_temp