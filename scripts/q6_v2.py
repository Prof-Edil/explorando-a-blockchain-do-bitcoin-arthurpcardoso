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

# Obtendo o hash dos blocos
block_256128_hash = run_bitcoin_cli(["getblockhash", "256128"])
block_257343_hash = run_bitcoin_cli(["getblockhash", "257343"])

if block_256128_hash and block_257343_hash:
    # Obtendo o bloco 256,128 e extraindo a transação coinbase
    block_256128 = run_bitcoin_cli(["getblock", block_256128_hash])
    block_256128 = json.loads(block_256128) if block_256128 else None

    if block_256128:
        coinbase_txid = block_256128['tx'][0]

        # Obtendo os detalhes da transação coinbase
        coinbase_tx = run_bitcoin_cli(["getrawtransaction", coinbase_txid, "true"])
        coinbase_tx = json.loads(coinbase_tx) if coinbase_tx else None

        if coinbase_tx:
            coinbase_vout_index = 0  # Geralmente é 0 para coinbase
            coinbase_vout_script = coinbase_tx['vout'][coinbase_vout_index]['scriptPubKey']['hex']

            # Obtendo o bloco 257,343
            block_257343 = run_bitcoin_cli(["getblock", block_257343_hash])
            block_257343 = json.loads(block_257343) if block_257343 else None

            if block_257343:
                achou = False

                # Iterando pelas transações do bloco 257,343 para encontrar a que consome a saída coinbase
                for txid in block_257343['tx']:
                    tx = run_bitcoin_cli(["getrawtransaction", txid, "true"])
                    tx = json.loads(tx) if tx else None

                    if tx:
                        for vin in tx['vin']:
                            if vin.get('txid') == coinbase_txid and vin.get('vout') == coinbase_vout_index:
                                print(txid)
                                achou = True
                                break
                    if achou:
                        break

if not block_256128_hash or not block_257343_hash:
    print("Erro ao obter os hashes dos blocos.")
