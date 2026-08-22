"""
Caça-Níqueis (Slot Machine) com sistema de apostas.
Evoluído a partir do protótipo original, agora integrado ao saldo do cassino.
"""

import random
import time

SIMBOLOS = ["🍒", "🍋", "🍇", "🔔", "⭐", "💎"]

# Multiplicador pago quando os 3 símbolos são iguais
MULTIPLICADOR_TRINCA = {
    "🍒": 2,
    "🍋": 3,
    "🍇": 4,
    "🔔": 5,
    "⭐": 8,
    "💎": 15,
}

# Multiplicador pago quando apenas 2 símbolos coincidem
MULTIPLICADOR_PAR = 1.2


def girar_rolo():
    return random.choice(SIMBOLOS)


def mostrar_animacao():
    for _ in range(5):
        print(f"| {random.choice(SIMBOLOS)} | {random.choice(SIMBOLOS)} | {random.choice(SIMBOLOS)} |", end="\r")
        time.sleep(0.15)
    print(" " * 25, end="\r")


def pedir_aposta(saldo):
    while True:
        entrada = input(f"Saldo: {saldo:.2f} fichas. Quanto deseja apostar? (0 para sair) ").strip()
        try:
            valor = float(entrada.replace(",", "."))
        except ValueError:
            print("Digite um número válido.")
            continue

        if valor == 0:
            return None
        if valor < 0:
            print("A aposta não pode ser negativa.")
        elif valor > saldo:
            print("Você não tem fichas suficientes para essa aposta.")
        else:
            return valor


def jogar_rodada(saldo):
    """Joga uma rodada do caça-níqueis e retorna o novo saldo."""
    aposta = pedir_aposta(saldo)
    if aposta is None:
        return saldo, False  # jogador optou por sair do jogo

    print("\nCaça-Níqueis")
    mostrar_animacao()

    resultado = [girar_rolo(), girar_rolo(), girar_rolo()]
    print(f"| {resultado[0]} | {resultado[1]} | {resultado[2]} |")

    if resultado[0] == resultado[1] == resultado[2]:
        multiplicador = MULTIPLICADOR_TRINCA[resultado[0]]
        premio = aposta * multiplicador
        saldo += premio
        print(f"🎉 TRINCA! Você ganhou {premio:.2f} fichas (x{multiplicador})!")
    elif resultado[0] == resultado[1] or resultado[1] == resultado[2] or resultado[0] == resultado[2]:
        premio = aposta * MULTIPLICADOR_PAR
        saldo += (premio - aposta)
        print(f"Quase! Você recuperou {premio:.2f} fichas.")
    else:
        saldo -= aposta
        print("Não saiu combinação. Você perdeu a aposta.")

    return saldo, True


def jogar(saldo):
    """Loop do caça-níqueis. Retorna ao menu principal quando o jogador sair ou zerar o saldo."""
    while True:
        if saldo <= 0:
            print("Você ficou sem fichas! Voltando ao menu principal.")
            return saldo

        saldo, continuar = jogar_rodada(saldo)
        if not continuar:
            return saldo

        resposta = input("\nEnter = jogar novamente / m = voltar ao menu: ").strip().lower()
        if resposta == "m":
            return saldo
