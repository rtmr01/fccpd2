FROM python:3.9-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev postgresql-dev 
RUN pip install flask redis psycopg2-binary

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]