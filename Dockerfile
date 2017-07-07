FROM centos:centos7

COPY oracle-instantclient12.2-basic-12.2.0.1.0-1.x86_64.rpm /scratch/instant_client.rpm

RUN 	cd /scratch/;\
	yum update -y ;\
	yum install -y /scratch/instant_client.rpm ;\
	yum install -y yum-utils lzma make;\
	rm /scratch/* ;\
	yum-builddep -y python ;\
	yum install -y wget ;\
	wget https://python.org/ftp/python/3.6.0/Python-3.6.0.tgz;\
	tar xzf Python-3.6.0.tgz ;\
	cd Python-3.6.0 ;\
	./configure ;\
	make -j4 ;\
	make install 

COPY app/ /app/
WORKDIR /app

RUN 	pip3 install -r /app/requirements.txt ;\
	python3 -m pip install cx_Oracle --pre

ENTRYPOINT ["python3"]

CMD ["app.py"]

ENV LD_LIBRARY_PATH="/usr/lib/oracle/12.2/client64/lib/"

COPY tnsnames.ora /tnsnames.ora

ENV TNS_ADMIN "/"

EXPOSE 8080
