FROM python:3.12.0-alpine

WORKDIR /app

COPY . .

RUN pip install -r requirement.txt

CMD ["python", "main.py"]

