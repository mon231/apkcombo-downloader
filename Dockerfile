FROM python

RUN apt-get update                             \
 && apt-get install -y --no-install-recommends \
    ca-certificates curl firefox-esr           \
 && rm -fr /var/lib/apt/lists/*                \
 && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz | tar xz -C /usr/local/bin

COPY . /app
WORKDIR /app

ENV DISPLAY=:99
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/app/downloader.py"]
