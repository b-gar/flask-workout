FROM python:3.10-slim
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY /app /app
WORKDIR /app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "8", "--timeout", "0", "main:app"]