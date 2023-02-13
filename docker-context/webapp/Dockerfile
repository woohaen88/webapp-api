FROM node:16
LABEL maintainer="woohaen88@gmail.com"

COPY ./run.sh /run.sh

EXPOSE 8080

RUN npm install -g @vue/cli

RUN chmod +x /run.sh

CMD ["/run.sh"]