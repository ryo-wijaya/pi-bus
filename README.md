## PI Stock Trader

Backend microservice to handle bus timings data display for the https://github.com/ryo-wijaya/my-pi-board Raspberry Pi dashboard. Consumes the cheeaun/arrivelah API which itself consumes LTA's DataMall Bus Arrival API.

### Command Bank

- Run Local Application

```bash
    uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

- Build Container

```bash
    docker build -t pi-bus:latest .
```

- Run Container

```bash
    docker run -d --name pi-bus-container -p 8002:8002 pi-bus:latest
```
