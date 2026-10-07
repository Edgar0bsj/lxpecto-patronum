import sys


def clear_terminal():
    # \033[H  -> Move o cursor para o topo/esquerda
    # \033[2J -> Limpa a tela visível
    # \033[3J -> Limpa o buffer de rolagem (scrollback)
    sys.stdout.write("\033[H\033[2J\033[3J")
    sys.stdout.flush()
