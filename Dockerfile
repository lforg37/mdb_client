FROM python:3-alpine

COPY app/ /app/

WORKDIR /app

RUN pip install -r /app/requirements.txt

ENTRYPOINT ["python"]

CMD ["app.py"]

EXPOSE 8080
