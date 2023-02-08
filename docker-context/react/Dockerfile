FROM node:14

COPY ./run.sh /run.sh

EXPOSE 3000

RUN chmod +x /run.sh && \
    npx create-react-app webapp

WORKDIR /webapp

CMD ["run.sh"]