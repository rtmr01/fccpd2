FROM python:3.9-alpine
WORKDIR /app
RUN pip install flask requests
COPY app.py .
EXPOSE 8000
CMD ["python", "app.py"]