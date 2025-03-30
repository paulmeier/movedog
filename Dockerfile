FROM python:3.9-bookworm

COPY . .

WORKDIR /src

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./app.py", "--source", "$SOURCE_DIR", "--destination", "$DESTINATION_DIR"]
