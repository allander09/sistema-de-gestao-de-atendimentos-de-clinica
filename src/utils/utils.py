import json
from pathlib import Path

# ---------------- ARQUIVOS ----------------
BASE_DIR = Path(__file__).resolve().parent.parent
ARQ_PACIENTES = BASE_DIR / "data" / "pacientes.json"
ARQ_ATENDIMENTOS = BASE_DIR / "data" / "atendimentos.json"

# ---------------- FUNÇÕES JSON ----------------
def carregar_dados(arquivo):
    arquivo = Path(arquivo)
    if arquivo.exists():
        with arquivo.open("r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_dados(arquivo, dados):
    arquivo = Path(arquivo)
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    with arquivo.open("w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)