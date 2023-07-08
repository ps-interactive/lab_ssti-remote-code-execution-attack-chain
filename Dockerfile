FROM ubuntu:20.04
RUN apt-get update -y && apt-get install -y python3 python3-pip python3-dev
COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt && rm /tmp/requirements.txt
ADD app /app
ENTRYPOINT ["python3"]
CMD ["/app/run.py"]
