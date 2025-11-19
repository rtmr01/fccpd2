import os
import time

DATA_DIR = '/data'
DATA_FILE = os.path.join(DATA_DIR, 'contador.txt')

def read_counter():
    """Lê o valor atual do contador (se existir) ou inicia em 0."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return int(f.read().strip())
        except Exception:
            return 0
    return 0

def write_counter(value):
    """Salva o novo valor no volume."""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    with open(DATA_FILE, 'w') as f:
        f.write(str(value))
    
    print(f"[{time.strftime('%H:%M:%S')}] Contador atualizado e persistido: {value}")

if __name__ == "__main__":
    current_value = read_counter()
    
    print(f"\n>>>> Container iniciando. Valor lido do volume: {current_value} <<<<")
    
    for i in range(1, 4):
        current_value += 1
        write_counter(current_value)
        time.sleep(1)
    
    print(f"\n**** Processo finalizado. Valor final persistido: {current_value} ****\n")