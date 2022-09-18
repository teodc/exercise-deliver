# syntax=docker/dockerfile:1

ARG app_port

FROM node:18-alpine

WORKDIR /app

COPY Makefile .
COPY package.json .
COPY package-lock.json .

RUN make install

COPY . .

EXPOSE $app_port

ENTRYPOINT ["npm"]
CMD ["start"]

# prod stuff?
# RUN make build
# ENTRYPOINT ["npx"]
# CMD ["serve", "build"]
