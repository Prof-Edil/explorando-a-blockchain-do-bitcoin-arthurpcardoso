from bitcoinrpc.authproxy import AuthServiceProxy

rpc_host = "84.247.182.145"  # Endereço do nó
rpc_user = "user_207"            # Nome de usuário RPC
rpc_password = "urJozzHS1XYO"    # Senha RPC
rpc_port = 8332              # Porta padrão RPC do Bitcoin

p = AuthServiceProxy(service_url=f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")
# Função para verificar se uma saída está gasta
def is_output_unspent(txid, vout_index):
    try:
        result = p.gettxout(txid, vout_index)
        return True, result  # Retorna True se a saída não foi gasta
    except Exception:
        return False  # Retorna False se foi gasta

# Obter o hash do bloco 123,321
block_hash = p.getblockhash(123321)

# Obter detalhes do bloco
block = p.getblock(block_hash)

# Iterar pelas transações do bloco
for tx in block['tx']:
        #print(tx)
        # pegar transação
        tx = p.getrawtransaction(tx, True)
        for vout in tx['vout']:
            flag, result = is_output_unspent(tx['txid'], vout['n'])
            if flag and result != None:
                print(vout)
                print(result)