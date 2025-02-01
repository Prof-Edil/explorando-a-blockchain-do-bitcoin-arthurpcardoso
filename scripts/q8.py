import subprocess
import json

def run_bitcoin_cli(command):
    """Executa um comando bitcoin-cli e retorna a saída como string."""
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
        print(f"Erro ao executar bitcoin-cli: {e.stderr}")
        return None

def get_public_key_from_witness(txid):
    """Extrai a chave pública do campo txinwitness da primeira entrada da transação."""
    raw_tx = run_bitcoin_cli(["getrawtransaction", txid, "true"])
    
    if not raw_tx:
        print(f"Erro ao obter a transação {txid}")
        return None
    
    transaction = json.loads(raw_tx)

    # Verificar se a transação tem entradas
    if not transaction.get("vin") or len(transaction["vin"]) == 0:
        print("Nenhuma entrada encontrada na transação.")
        return None

    # Pegar a primeira entrada
    vin = transaction["vin"][0]

    # Verificar se txinwitness existe
    if "txinwitness" not in vin or len(vin["txinwitness"]) == 0:
        print("Nenhum dado de testemunha encontrado na entrada.")
        return None

    # Pegar o último elemento da lista txinwitness (que contém a chave pública)
    witness_data = vin["txinwitness"][-1]

    # Verificar se a witness tem tamanho suficiente
    if len(witness_data) < 4:
        print("Dados de testemunha inválidos.")
        return None

    # O segundo byte da witness contém o tamanho da chave pública
    pubkey_len = int(witness_data[2:4], 16)

    # Extrair a chave pública completa
    pubkey = witness_data[4:4 + pubkey_len * 2]

    return pubkey

# ID da transação alvo
txid = "e5969add849689854ac7f28e45628b89f7454b83e9699e551ce14b6f90c86163"

# Obter a chave pública
pubkey = get_public_key_from_witness(txid)

if pubkey:
    print(pubkey)
else:
    print("Falha ao extrair a chave pública.")
