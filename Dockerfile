FROM python:3.9-bookworm

ENV SOURCE_DIR=/watchsrc
ENV DESTINATION_DIR=/watchdst
ENV RECURSIVE=true
ENV DEBUG=false
ENV SLEEP_TIME=10

COPY . .

WORKDIR /src

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./app.py", "--source", "$SOURCE_DIR", "--destination", "$DESTINATION_DIR", "--recursive", "$RECURSIVE", "--debug", "$DEBUG", "--sleep-time", "$SLEEP_TIME"]
