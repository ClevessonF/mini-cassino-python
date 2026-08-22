"""
Blackjack (21) simplificado para o mini-cassino de terminal.
Regras: dealer pede carta até somar 17+, Blackjack paga 1.5x, empate devolve a aposta.
"""

import random

NAIPES = ["♠", "♥", "♦", "♣"]
VALORES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


def criar_baralho():
    baralho = [(valor, naipe) for valor in VALORES for naipe in NAIPES]
    random.shuffle(baralho)
    return baralho


def valor_carta(carta):
    valor, _ = carta
    if valor in ("J", "Q", "K"):
        return 10
    if valor == "A":
        return 11
    return int(valor)


def valor_mao(mao):
    total = sum(valor_carta(c) for c in mao)
    ases = sum(1 for c in mao if c[0] == "A")
    # Ajusta Ases de 11 para 1 se estourar 21
    while total > 21 and ases > 0:
        total -= 10
        ases -= 1
    return total


def formatar_mao(mao, esconder_segunda=False):
    if esconder_segunda:
        cartas = [f"{mao[0][0]}{mao[0][1]}", "🂠"]
    else:
        cartas = [f"{v}{n}" for v, n in mao]
    return " | ".join(cartas)


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
    aposta = pedir_aposta(saldo)
    if aposta is None:
        return saldo, False

    baralho = criar_baralho()
    mao_jogador = [baralho.pop(), baralho.pop()]
    mao_dealer = [baralho.pop(), baralho.pop()]

    print(f"\nSua mão: {formatar_mao(mao_jogador)} (total: {valor_mao(mao_jogador)})")
    print(f"Mão do dealer: {formatar_mao(mao_dealer, esconder_segunda=True)}")

    # Blackjack natural
    if valor_mao(mao_jogador) == 21:
        print("🂡 BLACKJACK! Você ganha 1.5x a aposta.")
        saldo += aposta * 1.5
        return saldo, True

    # Turno do jogador
    while True:
        if valor_mao(mao_jogador) > 21:
            print("Você estourou 21! Perdeu a aposta.")
            saldo -= aposta
            return saldo, True

        acao = input("Pedir carta (h) ou parar (s)? ").strip().lower()
        if acao == "h":
            mao_jogador.append(baralho.pop())
            print(f"Sua mão: {formatar_mao(mao_jogador)} (total: {valor_mao(mao_jogador)})")
        elif acao == "s":
            break
        else:
            print("Digite 'h' para pedir carta ou 's' para parar.")

    # Turno do dealer
    print(f"\nMão do dealer: {formatar_mao(mao_dealer)} (total: {valor_mao(mao_dealer)})")
    while valor_mao(mao_dealer) < 17:
        mao_dealer.append(baralho.pop())
        print(f"Dealer pede carta: {formatar_mao(mao_dealer)} (total: {valor_mao(mao_dealer)})")

    total_jogador = valor_mao(mao_jogador)
    total_dealer = valor_mao(mao_dealer)

    if total_dealer > 21 or total_jogador > total_dealer:
        print(f"🎉 Você venceu! ({total_jogador} x {total_dealer})")
        saldo += aposta
    elif total_jogador == total_dealer:
        print(f"Empate ({total_jogador} x {total_dealer}). Aposta devolvida.")
    else:
        print(f"Dealer venceu ({total_dealer} x {total_jogador}). Você perdeu a aposta.")
        saldo -= aposta

    return saldo, True


def jogar(saldo):
    """Loop do blackjack. Retorna ao menu principal quando o jogador sair ou zerar o saldo."""
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
