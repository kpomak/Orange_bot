FROM python:3.9.16

WORKDIR /bot

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /bot

CMD ["python3", "run.py"]