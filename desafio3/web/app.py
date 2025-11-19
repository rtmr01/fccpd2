import os
from flask import Flask, g
import redis
import psycopg2
import time
from functools import wraps

app = Flask(__name__)

# --- Configurações de Conexão ---
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
r = redis.Redis(host=REDIS_HOST, port=6379)

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_NAME = os.environ.get('POSTGRES_DB', 'mydb')
DB_USER = os.environ.get('POSTGRES_USER', 'user')
DB_PASS = os.environ.get('POSTGRES_PASSWORD', 'password')

# --- Variável de estado para controle do setup ---
# Usada para garantir que o setup do DB rode APENAS uma vez, na primeira requisição.
DB_SETUP_COMPLETE = False

def wait_for_db():
    """Aguarda o PostgreSQL ficar disponível antes de tentar a conexão."""
    connected = False
    max_retries = 10
    attempts = 0
    
    while not connected and attempts < max_retries:
        try:
            # Tenta conectar
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
            conn.close()
            connected = True
            print(">>> PostgreSQL conectado com sucesso! <<<")
        except psycopg2.OperationalError:
            attempts += 1
            print(f">>> Aguardando o PostgreSQL... Tentativa {attempts}/{max_retries}.")
            time.sleep(2)
    
    if not connected:
        print("!!! ERRO CRÍTICO: Não foi possível conectar ao PostgreSQL após múltiplas tentativas.")
        raise ConnectionError("Falha na conexão inicial com o DB.")


@app.before_request
def setup_db_once():
    """Roda a inicialização do DB, garantindo que aconteça apenas na primeira requisição."""
    global DB_SETUP_COMPLETE
    
    if not DB_SETUP_COMPLETE:
        print("\n>>> Iniciando Setup de primeira requisição (Criação de Tabela)...")
        try:
            # 1. Espera o DB ficar online
            wait_for_db()
            
            # 2. Conecta e cria a estrutura
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
            cur = conn.cursor()
            
            # Cria a tabela de requests se não existir
            cur.execute("CREATE TABLE IF NOT EXISTS requests (count INTEGER)")
            
            # Garante que haja uma linha inicial para o contador (se não houver)
            cur.execute("INSERT INTO requests (count) SELECT 0 WHERE NOT EXISTS (SELECT * FROM requests)")
            
            conn.commit()
            cur.close()
            conn.close()
            
            DB_SETUP_COMPLETE = True # Marca como concluído
            print(">>> Setup do DB (Tabela 'requests') concluído com sucesso. <<<\n")
            
        except ConnectionError as e:
            # Se a espera falhar, o serviço web não deve subir
            print(f"Erro no setup: {e}")
            # Em produção, isso levaria a um erro HTTP 500
        except Exception as e:
            print(f"Erro inesperado durante o setup do DB: {e}")
            
    # O restante do código do Flask segue normalmente, DB_SETUP_COMPLETE garante que esta seção não rode novamente.


@app.route('/')
def index():
    if not DB_SETUP_COMPLETE:
        # Se o setup falhar por algum motivo, retorna erro
        return "Serviços internos não estão prontos. Verifique os logs do container 'web'.", 503

    try:
        # --- Teste 1: Comunicação com o Cache (Redis) ---
        r.incr('hit_counter')
        hits = r.get('hit_counter').decode('utf-8')

        # --- Teste 2: Comunicação com o DB (PostgreSQL) ---
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = conn.cursor()
        
        # Incrementa o contador do DB
        cur.execute("UPDATE requests SET count = count + 1 RETURNING count")
        db_count = cur.fetchone()[0]
        
        conn.commit()
        cur.close()
        conn.close()

        return (
            f"<h1>Orquestração Docker Compose OK!</h1>"
            f"<p>Serviços funcionando e comunicando:</p>"
            f"<hr>"
            f"<h2>Contador do Cache (Redis)</h2>"
            f"<p>Requisições totais no **CACHE (Redis)**: <strong>{hits}</strong></p>"
            f"<p style='color: orange;'>* Este contador será **resetado** ao reiniciar o container 'redis'.</p>"
            f"<h2>Contador do Banco de Dados (PostgreSQL)</h2>"
            f"<p>Atualizações totais no **DB (PostgreSQL)**: <strong>{db_count}</strong></p>"
            f"<p style='color: green;'>* Este contador é **persistido** graças ao volume 'pg_data'.</p>"
        )

    except Exception as e:
        return f"Erro na comunicação com um dos serviços após o setup inicial: {e}", 500

if __name__ == '__main__':
    # Flask 2.x+ usa a função run para rodar o app no contexto de desenvolvimento
    app.run(host='0.0.0.0', port=5000)