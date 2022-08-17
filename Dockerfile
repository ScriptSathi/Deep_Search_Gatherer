FROM python:3.9.13-alpine3.16

# Create user feedbot for security purpose and switch to it
RUN adduser -D -u 1000 rssbot
USER rssbot
WORKDIR /home/rssbot
RUN mkdir $HOME/backups

# Add path for pip modules
ENV PATH="~/.local/bin:${PATH}"

COPY *.py requirements.txt /opt/
COPY src/*.py /opt/src/

RUN python -m pip install --no-cache-dir --upgrade pip && \
	python -m pip install --no-cache-dir -r /opt/requirements.txt

CMD python /opt/main.py
