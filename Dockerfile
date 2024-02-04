FROM python

RUN apt-get update && \
    apt-get install -y wget unzip && \
    rm -rf /var/lib/apt/lists/*

RUN wget -O /tmp/msedgedriver.zip https://msedgedriver.azureedge.net/121.0.2277.98/edgedriver_linux64.zip && \
    unzip /tmp/msedgedriver.zip -d /usr/local/bin/ && \
    rm /tmp/msedgedriver.zip

COPY . /app
WORKDIR /app

ENV DISPLAY=:99
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/app/downloader.py"]
