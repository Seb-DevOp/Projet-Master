FROM python:3.11-slim

WORKDIR /app
COPY app /app
COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8080
ARG ENV
ARG VERSION
ARG COMMIT
ARG BUILD_TIME

ENV ENV=$ENV
ENV VERSION=$VERSION
ENV COMMIT=$COMMIT
ENV BUILD_TIME=$BUILD_TIME

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
