FROM python:3.10.15-alpine3.20

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY models ./models
COPY schema ./schema
COPY routes ./routes
COPY service ./service

#RUN python -c "from service.database import create_tables; create_tables()" \
#    && python -c "from service.parking import create_triggers; create_triggers()"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
