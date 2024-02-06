FROM ultrafunk/undetected-chromedriver
USER root

RUN apt update && apt upgrade -y
RUN yes | apt install python3-pip

COPY . /app
WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "/app/downloader.py"]
