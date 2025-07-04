import pygame


class EntityMediator:
    """
    Mediador central para interações entre entidades, especialmente colisões.
    """

    @staticmethod
    def check_all_collisions(player, enemies_group, player_shots_group, enemy_shots_group):
        """
        Verifica e processa todas as colisões entre jogador, inimigos e projéteis.

        Args:
            player (Player): instância do jogador.
            enemies_group (pygame.sprite.Group): inimigos ativos.
            player_shots_group (pygame.sprite.Group): tiros do jogador ativos.
            enemy_shots_group (pygame.sprite.Group): tiros dos inimigos ativos.
        """

        # 1. Colisões: Tiros do jogador com inimigos
        # Remove o projétil do jogador (dokill1=True)
        # Não remove o inimigo automaticamente (dokill2=False), pois a vida será reduzida via take_damage
        collisions = pygame.sprite.groupcollide(
            player_shots_group, enemies_group, True, False
        )
        if collisions:
            for shot, enemies_hit in collisions.items():
                print(f"DEBUG MEDIATOR: Projétil do jogador '{getattr(shot, 'name', '')}' colidiu com inimigos: {[e.name for e in enemies_hit]}")
                for enemy in enemies_hit:
                    enemy.take_damage(shot.damage)  # Aplica dano; o inimigo se mata se a vida acabar

        # 2. Colisões: Tiros dos inimigos com o jogador
        # Remove o projétil inimigo após acertar o jogador
        collisions = pygame.sprite.spritecollide(
            player, enemy_shots_group, True
        )
        if collisions:
            print(f"DEBUG MEDIATOR: Jogador colidiu com projéteis de inimigos: {[getattr(s, 'name', '') for s in collisions]}")
            # Exemplo futuro: aplicar dano no jogador
            # for shot in collisions:
            #     player.take_damage(shot.damage)

        # 3. Colisões físicas: jogador com inimigos
        collisions = pygame.sprite.spritecollide(
            player, enemies_group, False
        )
        if collisions:
            print(f"DEBUG MEDIATOR: Jogador colidiu fisicamente com inimigos: {[e.name for e in collisions]}")
            # Exemplo futuro: aplicar dano, interações etc.
            # for enemy in collisions:
            #     player.take_damage(enemy.collision_damage)
            #     enemy.on_player_collision(player)

