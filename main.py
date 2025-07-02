# C:\Users\muril\PycharmProjects\thewitchandtheholyorder\main.py

from code.game import Game # Importa a classe Game do módulo game dentro do pacote code

if __name__ == '__main__': # Garante que o código só execute quando o script for rodado diretamente
    my_game_instance = Game()
    my_game_instance.run()