FROM selenium/standalone-chrome:dev
USER root

RUN apt update && apt upgrade -y
RUN apt install -y python3 python3-pip

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/app/downloader.py"]
