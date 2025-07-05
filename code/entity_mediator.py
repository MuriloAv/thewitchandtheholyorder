# code/entity_mediator.py

import pygame


class EntityMediator:
    """
    Mediador central para interações entre entidades, especialmente colisões.
    """

    @staticmethod
    def check_all_collisions(player, enemies_group, player_shots_group, enemy_shots_group):
        """
        Verifica e processa todas as colisões entre jogador, inimigos e projéteis.
        """

        # 1. Colisões: Tiros do jogador com inimigos
        collisions = pygame.sprite.groupcollide(
            player_shots_group, enemies_group, True, False
        )
        if collisions:
            for shot, enemies_hit in collisions.items():
                print(f"DEBUG MEDIATOR: Projétil do jogador '{getattr(shot, 'name', 'PlayerShot')}' colidiu com inimigos: {[e.name for e in enemies_hit]}")
                for enemy in enemies_hit:
                    enemy.take_damage(shot.damage)

        # 2. Colisões: Tiros dos inimigos com o jogador
        collisions = pygame.sprite.spritecollide(
            player, enemy_shots_group, True # O projétil inimigo é removido (True)
        )
        if collisions:
            print(f"DEBUG MEDIATOR: Jogador colidiu com projéteis de inimigos: {[getattr(s, 'name', 'EnemyShot') for s in collisions]}")
            # NOVO: Jogador leva dano
            player.take_damage(amount=1) # Cada tiro inimigo tira 1 vida

        # 3. Colisões físicas: jogador com inimigos
        # Aqui, você pode decidir se o jogador também leva dano ao tocar em um inimigo.
        collisions = pygame.sprite.spritecollide(
            player, enemies_group, False # Inimigo não é removido automaticamente
        )
        if collisions:
            # print(f"DEBUG MEDIATOR: Jogador colidiu fisicamente com inimigos: {[e.name for e e in collisions]}")
            # Exemplo: player.take_damage(amount=1) # Se você quiser dano por contato
            pass