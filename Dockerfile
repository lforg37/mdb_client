FROM python:3-alpine

COPY app/ /app/

WORKDIR /app

RUN 	apk add --no-cache gcc musl-dev ;\
	pip install -r /app/requirements.txt ;\
	python -m pip install cx_Oracle --pre ;\
	apk del --no-cache gcc 


ENTRYPOINT ["python"]

CMD ["app.py"]

EXPOSE 8080
