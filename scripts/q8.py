from bitcoinrpc.authproxy import AuthServiceProxy

rpc_host = "84.247.182.145"  # Endereço do nó
rpc_user = "user_207"            # Nome de usuário RPC
rpc_password = "urJozzHS1XYO"    # Senha RPC
rpc_port = 8332              # Porta padrão RPC do Bitcoin

p = AuthServiceProxy(service_url=f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

# Hash da transação
txid = "e5969add849689854ac7f28e45628b89f7454b83e9699e551ce14b6f90c86163"

# Obtém a transação bruta
raw_tx = p.getrawtransaction(txid)

# Decodifica a transação
decoded_tx = p.decoderawtransaction(raw_tx)

# Obtém os detalhes da entrada 0
input_0 = decoded_tx["vin"][0]
script_sig = input_0.get("scriptSig", {})

# Extrai a assinatura e a chave pública
asm = script_sig.get("asm", "")
asm_parts = asm.split(" ")
if len(asm_parts) > 1:
	signature = asm_parts[0]
	public_key = asm_parts[1]
	print("Assinatura:", signature)
	print("Chave Pública:", public_key)
else:
	print("Não foi possível extrair a assinatura e a chave pública.")
