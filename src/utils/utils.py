import json
import os

# ---------------- ARQUIVOS ----------------
# Não reconhece o caminho -- ajustar -- fix
ARQ_PACIENTES = os.path.abspath("./data/pacientes.json")
ARQ_ATENDIMENTOS = os.path.abspath("./data/atendimentos.json")

# ---------------- FUNÇÕES JSON ----------------
def carregar_dados(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            return json.load(f)
    
    return []
print (carregar_dados(ARQ_PACIENTES))


def salvar_dados(arquivo, dados):
    with open(arquivo, "w") as f:
        json.dump(dados, f, indent=4)