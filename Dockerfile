FROM ubuntu:latest
LABEL authors="nikse"

ENTRYPOINT ["top", "-b"]