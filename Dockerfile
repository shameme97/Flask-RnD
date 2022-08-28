FROM alpine:latest

# RUN apk add --no-cache python3-dev && pip install --upgrade pip

WORKDIR /controller
COPY . /controller
# RUN pip --no-cache-dir install -r requirements.txt
EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["movies.py"]