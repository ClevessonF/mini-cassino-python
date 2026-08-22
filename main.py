"""
Mini-Cassino em Python
Menu principal que integra Caça-Níqueis e Blackjack, com saldo persistente.
"""

import os
import sys

import saldo as saldo_manager
import caca_niquel
import blackjack


def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_menu(saldo):
    limpar_terminal()
    print("=" * 36)
    print("        🎰  MINI-CASSINO PYTHON  🎰")
    print("=" * 36)
    print(f"Saldo atual: {saldo:.2f} fichas\n")
    print("[1] Caça-Níqueis")
    print("[2] Blackjack (21)")
    print("[3] Resetar saldo")
    print("[q] Sair")
    print("=" * 36)


def main():
    saldo = saldo_manager.carregar_saldo()

    while True:
        mostrar_menu(saldo)
        escolha = input("Escolha uma opção: ").strip().lower()

        if escolha == "1":
            saldo = caca_niquel.jogar(saldo)
            saldo_manager.salvar_saldo(saldo)
        elif escolha == "2":
            saldo = blackjack.jogar(saldo)
            saldo_manager.salvar_saldo(saldo)
        elif escolha == "3":
            confirmar = input("Tem certeza que deseja resetar o saldo? (s/n) ").strip().lower()
            if confirmar == "s":
                saldo = saldo_manager.resetar_saldo()
                print("Saldo resetado!")
                input("Pressione Enter para continuar...")
        elif escolha == "q":
            saldo_manager.salvar_saldo(saldo)
            print("Saldo salvo. Obrigado por jogar! 👋")
            sys.exit(0)
        else:
            print("Opção inválida.")
            input("Pressione Enter para continuar...")


if __name__ == "__main__":
    main()
