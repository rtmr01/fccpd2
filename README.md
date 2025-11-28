Projeto de Desafios: Docker e Microsserviços

Este repositório contém as soluções para cinco desafios focados na orquestração de containers com Docker e Docker Compose, cobrindo tópicos como redes customizadas, persistência de dados (volumes) e arquitetura de Microsserviços (com e sem API Gateway).

A implementação foi feita utilizando Python/Flask para os serviços de aplicação (APIs) e imagens oficiais (Redis e PostgreSQL) para os serviços de infraestrutura.

1. Desafio 1 — Containers em Rede

Objetivo: Demonstrar a comunicação entre dois containers orquestrados através de um docker-compose.yml, que gerencia automaticamente a rede de comunicação.

1.1. Arquitetura e Decisões Técnicas

Serviços: Um Servidor Web (Flask, porta 8080) e um Cliente (Alpine com curl em loop).

Orquestração: Uso do docker-compose.yml para definir e iniciar ambos os serviços simultaneamente.

Rede: O Docker Compose cria uma rede Bridge padrão (nomeada automaticamente) que permite a comunicação entre os serviços.

Comunicação: O serviço cliente utiliza o Nome do Serviço (servidor-web) para fazer a requisição, provando que o DNS interno do Compose está funcionando.

Inicialização: Uso de depends_on para garantir que o servidor-web inicie antes do cliente.

1.2. Estrutura do Projeto

/desafio1 ├── docker-compose.yml (Novo arquivo de orquestração) ├── client/ │   └── Dockerfile (Instala o curl e faz requisição em loop) └── server/     ├── app.py (Servidor Flask simples)     └── Dockerfile

1.3. Instruções de Execução (Passo a Passo)

Navegue até o diretório desafio1.

Inicie os Serviços O Docker Compose irá construir as imagens, criar a rede e iniciar os dois contêineres.

Bash
docker compose up --build
Nota: Remova o -d para ver o log de ambos os serviços no terminal. O log do cliente será a prova da comunicação.

Obtenha o Print O log do contêiner cliente (ou desafio1_cliente_1) deve mostrar as respostas periódicas do servidor-web.

Print: Faça uma captura de tela mostrando o log do terminal com o docker compose up, onde o contêiner do cliente está recebendo as mensagens do servidor.

Limpeza (Opcional) Use o comando de down para parar e remover os contêineres e a rede criada pelo Compose.

Bash
docker compose down



<img width="1280" height="832" alt="image" src="https://github.com/user-attachments/assets/5db0fd28-d294-460f-b74e-bc8e668b4c4e" />




2. Desafio 2 — Volumes e Persistência

Objetivo: Provar que os dados de uma aplicação persistem mesmo após a remoção (destruição) do container.

2.1. Arquitetura e Decisões Técnicas

Aplicação: Um script Python (Flask) que simula um processo de atualização de um contador persistido em um arquivo (/data/contador.txt).

Persistência: Foi utilizado um Volume Nomeado (dados-contador) mapeado para o diretório /data dentro do container.

Prova: O container 1 é executado, incrementa o contador e é destruído (--rm). O container 2 é executado em seguida, lê o valor final deixado pelo primeiro, e continua a contagem, comprovando a persistência.

2.2. Estrutura do Projeto

/desafio2
├── app.py (Lê, incrementa e escreve no volume)
└── Dockerfile


2.3. Instruções de Execução (Passo a Passo)

Construa a imagem:

docker build -t imagem-contador ./desafio2


Primeira Execução (Criação do Dado): O contador deve ir de 1 a 3. O --rm remove o container, mas o volume permanece.

docker run --rm --name container-v1 -v dados-contador:/data imagem-contador


Segunda Execução (Comprovação da Persistência): O contador deve iniciar do 3 (o valor persistido) e subir até 6.

docker run --rm --name container-v2 -v dados-contador:/data imagem-contador


Limpeza (opcional, para remover o volume):

docker volume rm dados-contador


(Aqui você deve inserir o print dos dois logs, mostrando o valor inicial de 0 e o valor inicial de 3.)

3. Desafio 3 — Docker Compose Orquestrando Serviços

Objetivo: Orquestrar uma aplicação de três serviços dependentes (Web, Cache e DB) usando docker-compose.yml.

3.1. Arquitetura e Decisões Técnicas

Serviços: web (Flask API), redis (Cache) e db (PostgreSQL).

Docker Compose: Usado para configurar os 3 serviços em uma rede Bridge única (app_network).

Conexão: A API web usa o nome dos serviços (redis e db) para comunicação interna.

Persistência/Volume: O serviço db utiliza um volume nomeado (pg_data) para persistir os dados do banco de dados.

Dependência: Utilização de depends_on e de uma função de polling (wait_for_db no app.py) para garantir que o serviço db esteja totalmente pronto antes de a aplicação Web tentar o setup.

3.2. Estrutura do Projeto

/desafio3
├── docker-compose.yml
└── web/
    ├── app.py (Testa comunicação com Redis e DB)
    └── Dockerfile


3.3. Instruções de Execução (Passo a Passo)

Navegue até a pasta desafio3.

Suba os serviços:

docker compose up -d --build


Acesse a API para testar as conexões (mapeado para a porta 80 do host):

curl http://localhost


A cada curl, os contadores do Redis e do PostgreSQL devem incrementar, comprovando a comunicação com os três serviços.

(Aqui você deve inserir o print mostrando o curl retornando o HTML com os contadores em 5, após 5 requisições.)

4. Desafio 4 — Microsserviços Independentes

Objetivo: Criar dois microsserviços que se comunicam via HTTP sem um orquestrador centralizado (como o Compose).

4.1. Arquitetura e Decisões Técnicas

Microsserviços:

Users-Service (A): Fornece uma lista estática de usuários (JSON).

Consumer-Service (B): Consome a API do Serviço A, filtra os usuários ativos e retorna um resumo.

Rede e Comunicação: Foi utilizada uma rede Bridge customizada (minha-rede-desafio4) para que o Serviço B pudesse resolver o nome DNS do Serviço A (users-service).

4.2. Estrutura do Projeto

/desafio4
├── consumer-service/
│   ├── app.py (Faz requisição HTTP para o Serviço A)
│   └── Dockerfile
└── users-service/
    ├── app.py (Fornece dados)
    └── Dockerfile


4.3. Instruções de Execução (Passo a Passo)

Crie a rede customizada e construa as imagens.

Inicie o Serviço A (Users):

docker run -d --name users-service --network minha-rede-desafio4 users-image


Inicie o Serviço B (Consumer), expondo-o publicamente na porta 8080:

docker run -d -p 8080:5002 --name consumer-service --network minha-rede-desafio4 consumer-image


Acesse o endpoint final (Serviço B):

curl http://localhost:8080/summary


(Aqui você deve inserir o print do curl retornando o JSON processado, mostrando apenas os usuários ativos.)

5. Desafio 5 — Microsserviços com API Gateway

Objetivo: Centralizar o acesso a múltiplos microsserviços através de um único API Gateway, orquestrado via Docker Compose.

5.1. Arquitetura e Decisões Técnicas

Serviços: users-service, orders-service (microsserviços internos) e api-gateway (ponto de entrada).

Gateway (Flask): O Gateway atua como um Reverse Proxy, recebendo requisições em rotas públicas (/users, /orders) e encaminhando-as internamente para os respectivos microsserviços usando seus nomes de serviço.

Orquestração: Docker Compose gerencia os três serviços em uma rede interna, e o Gateway é o único serviço com porta exposta publicamente (porta 8080).

5.2. Estrutura do Projeto

/desafio5
├── docker-compose.yml
├── gateway/      (Ponto de entrada, faz proxy para os outros serviços)
├── orders/       (Fornece dados de pedidos)
└── users/        (Fornece dados de usuários)


5.3. Instruções de Execução (Passo a Passo)

Navegue até a pasta desafio5.

Suba os três serviços:

docker compose up -d --build


Teste o Gateway (Home):

curl http://localhost:8080/


Teste o Proxy Users: Acessa o users-service via Gateway.

curl http://localhost:8080/users


Teste o Proxy Orders: Acessa o orders-service via Gateway.

curl http://localhost:8080/orders


(Aqui você deve inserir o print das três chamadas curl (home, users, orders) comprovando que o Gateway está roteando corretamente.)
