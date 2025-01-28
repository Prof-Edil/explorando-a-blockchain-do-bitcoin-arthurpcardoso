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

# Função para verificar se uma saída está gasta
def is_output_unspent(txid, vout_index):
    try:
        result = run_bitcoin_cli(["gettxout", txid, str(vout_index)])
        return True, json.loads(result) if result else None  # Retorna True se a saída não foi gasta
    except Exception:
        return False, None  # Retorna False se foi gasta

# Obter o hash do bloco 123,321
block_hash = run_bitcoin_cli(["getblockhash", "123321"])

if block_hash:
    # Obter detalhes do bloco
    block = run_bitcoin_cli(["getblock", block_hash])
    block = json.loads(block) if block else None

    if block:
        # Iterar pelas transações do bloco
        for txid in block['tx']:
            # Obter transação
            tx = run_bitcoin_cli(["getrawtransaction", txid, "true"])
            tx = json.loads(tx) if tx else None

            if tx:
                for vout in tx['vout']:
                    flag, result = is_output_unspent(tx['txid'], vout['n'])
                    if flag and result is not None:
                        print(vout['scriptPubKey']['address'])
else:
    print("Erro ao obter o hash do bloco 123,321.")
