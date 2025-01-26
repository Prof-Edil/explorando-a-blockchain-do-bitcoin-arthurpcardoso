from bitcoin.rpc import RawProxy

# Conectando ao nó Bitcoin
# Configurando o objeto RawProxy para conexão ao nó Bitcoin
rpc_host = "84.247.182.145"  # Endereço do nó
rpc_user = "user_207"            # Nome de usuário RPC
rpc_password = "urJozzHS1XYO"    # Senha RPC
rpc_port = 8332              # Porta padrão RPC do Bitcoin

# Conectando ao nó com as credenciais fornecidas
service_url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}"
p = RawProxy(service_url)

# Obtendo o hash dos blocos
block_256128_hash = p.getblockhash(256128)
block_257343_hash = p.getblockhash(257343)

# Obtendo o bloco 256,128 e extraindo a transação coinbase
block_256128 = p.getblock(block_256128_hash)
coinbase_txid = block_256128['tx'][0]

# Obtendo os detalhes da transação coinbase
coinbase_tx = p.getrawtransaction(coinbase_txid, True)

# O índice e o script da saída
coinbase_vout_index = 0  # Geralmente é 0 para coinbase
coinbase_vout_script = coinbase_tx['vout'][coinbase_vout_index]['scriptPubKey']['hex']

# Obtendo o bloco 257,343
block_257343 = p.getblock(block_257343_hash)

# Iterando pelas transações do bloco 257,343 para encontrar a que consome a saída coinbase
for txid in block_257343['tx']:
    tx = p.getrawtransaction(txid, True)
    for vin in tx['vin']:
        if vin.get('txid') == coinbase_txid and vin.get('vout') == coinbase_vout_index:
            print(f"Transação encontrada: {txid}")
            break