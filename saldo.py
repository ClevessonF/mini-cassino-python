"""
Módulo responsável por carregar e salvar o saldo do jogador.
Persistência simples em arquivo JSON (saldo.json).
"""

import json
import os

ARQUIVO_SALDO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saldo.json")
SALDO_INICIAL = 100.0


def carregar_saldo():
    """Lê o saldo salvo em disco. Se não existir, cria com o valor inicial."""
    if not os.path.exists(ARQUIVO_SALDO):
        salvar_saldo(SALDO_INICIAL)
        return SALDO_INICIAL

    try:
        with open(ARQUIVO_SALDO, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            return float(dados.get("saldo", SALDO_INICIAL))
    except (json.JSONDecodeError, ValueError):
        # Arquivo corrompido ou inválido: reinicia o saldo
        salvar_saldo(SALDO_INICIAL)
        return SALDO_INICIAL


def salvar_saldo(saldo):
    """Grava o saldo atual no arquivo JSON."""
    with open(ARQUIVO_SALDO, "w", encoding="utf-8") as arquivo:
        json.dump({"saldo": round(saldo, 2)}, arquivo, indent=2)


def resetar_saldo():
    """Reseta o saldo para o valor inicial (útil se o jogador zerar as fichas)."""
    salvar_saldo(SALDO_INICIAL)
    return SALDO_INICIAL
