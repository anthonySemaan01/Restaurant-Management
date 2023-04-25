from datetime import datetime

from pydantic import BaseModel


class ReserveTableRequest(BaseModel):
    table_id: int
    customer_id: int
    time: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
