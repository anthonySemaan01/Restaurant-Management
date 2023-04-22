from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime


class ReserveTableRequest(BaseModel):
    table_id: int
    customer_id: int
    time: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
