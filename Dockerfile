FROM python:3-alpine

COPY app/ /app/

COPY instantclient-basic-linux.x64-12.2.0.1.0.zip /scratch/instant_client.zip

RUN 	cd /scratch/;\
	unzip instant_client.zip ;\
	mv  instantclient_12_2/lib* /usr/lib ;\
	rm -r instantclient_12_2/

WORKDIR /app

RUN 	apk add --no-cache gcc musl-dev;\
	pip install -r /app/requirements.txt ;\
	python -m pip install cx_Oracle --pre ;\
	apk del --no-cache gcc 


ENTRYPOINT ["python"]

CMD ["app.py"]

EXPOSE 8080
