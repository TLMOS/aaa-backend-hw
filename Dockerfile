FROM python:3.10

WORKDIR /app

COPY src/ ./src
COPY model_weights/ ./model_weights
COPY requirements.txt ./
RUN pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html

CMD [ "python", "./src/app.py" ]

