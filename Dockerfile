FROM python:3.7-slim
ADD analytics.py /
ADD process.py /
ADD client.py /
ENV WEBSOCKET ws://172.17.0.1:8888/ws/calibration
COPY ./requirements.txt /var/www/requirements.txt
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        make \
        gcc \
    && pip install -r /var/www/requirements.txt \
    && apt-get remove -y --purge make gcc build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
CMD [ "python", "./client.py" ]