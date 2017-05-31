FROM node:alpine

RUN 	mkdir -p /usr/src/app ; \
	mkdir -p /tmp/images

WORKDIR /usr/src/app

COPY app/package.json /usr/src/app/

RUN npm install

COPY app/* /usr/src/app/

EXPOSE 8080
CMD ["npm", "start"]
