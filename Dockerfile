FROM python:3.7-slim
ADD analytics.py /
ADD process.py /
ADD response.py /
ADD TaskDistance.py /
ADD client.py /
ENV DATA_DIR /home/david/temp/docker
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