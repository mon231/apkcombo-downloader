FROM ultrafunk/undetected-chromedriver
USER root

COPY . /app
WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "/app/downloader.py"]
