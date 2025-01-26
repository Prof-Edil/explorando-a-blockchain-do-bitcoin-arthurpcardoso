from bitcoinrpc.authproxy import AuthServiceProxy

rpc_host = "84.247.182.145"  # Endereço do nó
rpc_user = "user_207"            # Nome de usuário RPC
rpc_password = "urJozzHS1XYO"    # Senha RPC
rpc_port = 8332              # Porta padrão RPC do Bitcoin

p = AuthServiceProxy(service_url=f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")
# Função para verificar se uma saída está gasta
def is_output_unspent(txid, vout_index):
    try:
        p.gettxout(txid, vout_index)
        return True  # Retorna True se a saída não foi gasta
    except Exception:
        return False  # Retorna False se foi gasta

# Obter o hash do bloco 123,321
block_hash = p.getblockhash(123321)

# Obter detalhes do bloco
block = p.getblock(block_hash)

# Iterar pelas transações do bloco
for txid in block['tx']:
    tx = p.getrawtransaction(txid, True)
    for vout_index, vout in enumerate(tx['vout']):
        if is_output_unspent(txid, vout_index):
            address = vout['scriptPubKey'].get('addresses', ["Endereço desconhecido"])[0]
            print(f"Transação {txid}, saída {vout_index} permanece não gasta.")
            print(f"Endereço: {address}")