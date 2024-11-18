from pydantic import BaseModel
from typing import List, Optional


class BusTiming(BaseModel):
    order: int
    time: str  # e.g., "4 mins", "Arriving", or "Unknown"
    type: Optional[
        str
    ]  # e.g., "SD" or "DD", or None if unavailable. SD is single-decker and DD is double-decker.


class BusTimingsResponse(BaseModel):
    bus_stop_id: str
    bus_service: str
    timings: List[BusTiming]
