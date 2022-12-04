FROM python:3-slim
WORKDIR /code
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "start_api.py"]