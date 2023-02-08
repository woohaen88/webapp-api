FROM node:16
LABEL maintainer="woohaen88@gmail.com"

RUN echo "helloworld"

COPY ./run.sh /run.sh

EXPOSE 3000

RUN npx create-react-app webapp

RUN chmod +x /run.sh

WORKDIR /webapp

CMD ["/run.sh"]