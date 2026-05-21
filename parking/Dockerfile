FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5428

CMD ["gunicorn", "--bind", "0.0.0.0:5428", "--workers", "4", "app:app"]
