# syntax=docker/dockerfile:1

ARG app_port

FROM python:3.10-bullseye

WORKDIR /app

COPY Makefile .
COPY requirements.txt .

RUN make install

COPY . .

EXPOSE $app_port

ENTRYPOINT ["python"]
CMD ["src/main.py"]
