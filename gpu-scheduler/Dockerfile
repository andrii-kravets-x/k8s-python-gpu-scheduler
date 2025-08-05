FROM python:3.13-slim
WORKDIR /app
COPY main.py .
RUN pip install kubernetes loguru
CMD ["python", "main.py"]