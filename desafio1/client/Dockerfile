FROM alpine:latest

RUN apk add --no-cache curl

CMD sh -c "while true; do echo 'Enviando requisicao...'; curl http://servidor-web:8080; sleep 5; done"