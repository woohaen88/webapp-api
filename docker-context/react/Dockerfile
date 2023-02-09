FROM node:16
LABEL maintainer="woohaen88@gmail.com"

WORKDIR /webapp

COPY ./run.sh /run.sh

EXPOSE 3000

RUN chmod +x /run.sh

CMD ["/run.sh"]