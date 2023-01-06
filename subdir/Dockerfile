FROM python:3.10-alpine3.16

# Create user rssbot for security purpose and switch to it
RUN adduser -D -u 1000 rssbot
USER rssbot
WORKDIR /home/rssbot
RUN mkdir $HOME/backups

COPY *.py requirements.txt /opt/
COPY src/ /opt/src/

RUN python -m pip install --no-cache-dir --upgrade pip
RUN python -m pip install --no-cache-dir -r /opt/requirements.txt

CMD python /opt/main.py
