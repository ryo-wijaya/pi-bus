from typing import Union
import os

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import requests

from util import calculate_minutes_from_now
from models import BusTiming, BusTimingsResponse

load_dotenv()

app = FastAPI(root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"Health-check for pi-bus."}


@app.get("/bus-timings", response_model=BusTimingsResponse)
async def get_bus_timings(
    bus_stop_id: str = Query(..., description="The ID of the bus stop"),
    bus_service: str = Query(..., description="The specific bus service number"),
):
    """
    Get the next two bus timings for a specific bus service at a specific bus stop.
    Args:
        bus_stop_id (str): The ID of the bus stop.
        bus_service (str): The bus service number.
    Returns:
        BusTimingsResponse: The formatted response.
    """

    ARRIVELAH_URL = os.getenv("API_BUS_URL")

    try:
        response = requests.get(f"{ARRIVELAH_URL}?id={bus_stop_id}")
        response.raise_for_status()
        data = response.json()

        # Check if services data exists, if not return 400
        services = data.get("services")
        if not services:
            raise HTTPException(
                status_code=400, detail="No bus services found at this bus stop."
            )

        # Filter to return the next 2 bus timings and bus type ONLY, with timings in terms of minutes from now
        for service in services:
            if service.get("no") == bus_service:
                next_buses = []

                # Filter results for 1st bus
                if "next" in service and service["next"].get("time"):
                    next_buses.append(
                        BusTiming(
                            order=1,
                            time=calculate_minutes_from_now(service["next"]["time"]),
                            type=service["next"].get("type"),
                        )
                    )

                # Filter results for 2nd bus
                if "subsequent" in service and service["subsequent"].get("time"):
                    next_buses.append(
                        BusTiming(
                            order=2,
                            time=calculate_minutes_from_now(
                                service["subsequent"]["time"]
                            ),
                            type=service["subsequent"].get("type"),
                        )
                    )

                return BusTimingsResponse(
                    bus_stop_id=bus_stop_id, bus_service=bus_service, timings=next_buses
                )

        # If the bus service is not found, return 400
        raise HTTPException(
            status_code=400,
            detail=f"Bus service {bus_service} not found at bus stop {bus_stop_id}.",
        )

    except requests.exceptions.RequestException as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail="Please check server logs.")
