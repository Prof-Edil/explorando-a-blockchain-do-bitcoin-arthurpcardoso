import subprocess
import json

def run_bitcoin_cli(command):
    try:
        result = subprocess.run(
            ["bitcoin-cli"] + command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        result.check_returncode()
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running bitcoin-cli command: {e.stderr}")
        return None

# Função para obter a chave pública que assinou uma entrada
def get_public_key_for_input(txid, input_index):
    try:
        # Obter os detalhes da transação
        raw_tx = run_bitcoin_cli(["getrawtransaction", txid, "true"])
        transaction = json.loads(raw_tx) if raw_tx else None

        if not transaction:
            print(f"Erro ao obter detalhes da transação {txid}")
            return None

        # Obter os detalhes da entrada
        if input_index >= len(transaction['vin']):
            print(f"Índice de entrada {input_index} inválido para a transação {txid}")
            return None

        input_vin = transaction['vin'][input_index]
        
        # Obter a transação anterior para decodificar a saída
        prev_txid = input_vin['txid']
        prev_raw_tx = run_bitcoin_cli(["getrawtransaction", prev_txid, "true"])
        prev_transaction = json.loads(prev_raw_tx) if prev_raw_tx else None

        if not prev_transaction:
            print(f"Erro ao obter detalhes da transação anterior {prev_txid}")
            return None

        # Obter a saída referenciada
        vout_index = input_vin['vout']
        if vout_index >= len(prev_transaction['vout']):
            print(f"Índice de saída {vout_index} inválido na transação anterior {prev_txid}")
            return None

        output = prev_transaction['vout'][vout_index]
        print(output)
        script_pub_key = output['scriptPubKey']

        # Retornar a chave pública associada
        return script_pub_key.get('asm')
    except Exception as e:
        print(f"Erro ao processar a entrada {input_index} da transação {txid}: {str(e)}")
        return None

# Transação alvo e índice da entrada
target_txid = "e5969add849689854ac7f28e45628b89f7454b83e9699e551ce14b6f90c86163"
input_index = 0

# Obter a chave pública
public_key = get_public_key_for_input(target_txid, input_index)
if public_key:
    print(public_key)
else:
    print(f"Não foi possível determinar a chave pública para a entrada {input_index} da transação {target_txid}.")
