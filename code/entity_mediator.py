# code/entity_mediator.py

import pygame


# Não precisamos importar 'const' aqui inicialmente, a menos que tenhamos constantes específicas
# de colisão ou tipos de entidade definidos lá que o mediador precise.

class EntityMediator:
    """
    Classe utilitária que atua como um mediador central para interações entre entidades.
    Inicialmente focada na detecção e processamento de colisões.
    Implementada com métodos estáticos conforme solicitação.
    """

    @staticmethod
    def check_all_collisions(player, enemies_group, player_shots_group, enemy_shots_group):
        """
        Verifica e processa todas as colisões entre o jogador, inimigos e projéteis.

        Args:
            player (Player): A instância do jogador.
            enemies_group (pygame.sprite.Group): Grupo de todos os inimigos ativos.
            player_shots_group (pygame.sprite.Group): Grupo de todos os projéteis do jogador ativos.
            enemy_shots_group (pygame.sprite.Group): Grupo de todos os projéteis dos inimigos ativos.
        """

        # --- 1. Colisões entre Projéteis do Jogador e Inimigos ---
        # `dokill1=True` remove o projétil do jogador do seu grupo após colisão.
        # `dokill2=True` remove o inimigo do seu grupo após colisão.
        # No futuro, 'matar' o inimigo pode significar reduzir sua vida,
        # então esse `dokill2` pode mudar para `False` e a lógica de dano ser aplicada.
        collisions_player_shot_enemy = pygame.sprite.groupcollide(
            player_shots_group, enemies_group, True, True
        )
        if collisions_player_shot_enemy:
            for shot, enemies_hit in collisions_player_shot_enemy.items():
                print(
                    f"DEBUG MEDIATOR: Projétil do jogador '{shot.name}' colidiu com inimigos: {[e.name for e in enemies_hit]}")
                # Exemplo futuro: Aplicar dano ao inimigo
                # for enemy in enemies_hit:
                #     enemy.take_damage(shot.damage)

        # --- 2. Colisões entre Projéteis dos Inimigos e o Jogador ---
        # `dokill=True` remove o projétil do inimigo do seu grupo se ele atingir o jogador.
        collisions_enemy_shot_player = pygame.sprite.spritecollide(
            player, enemy_shots_group, True  # True para remover o projétil do inimigo
        )
        if collisions_enemy_shot_player:
            print(
                f"DEBUG MEDIATOR: Jogador colidiu com projéteis de inimigos: {[s.name for s in collisions_enemy_shot_player]}")
            # Exemplo futuro: Aplicar dano ao jogador
            # for shot in collisions_enemy_shot_player:
            #     player.take_damage(shot.damage)

        # --- 3. Colisões entre Jogador e Inimigos (colisão física) ---
        # `dokill=False` aqui para apenas detectar a colisão, sem remover o inimigo.
        # O dano e remoção do inimigo/jogador serão tratados por métodos específicos
        # (ex: player.take_damage(), enemy.on_player_collision()).
        collisions_player_enemy = pygame.sprite.spritecollide(
            player, enemies_group, False  # False para não remover o inimigo automaticamente
        )
        if collisions_player_enemy:
            print(
                f"DEBUG MEDIATOR: Jogador colidiu fisicamente com inimigos: {[e.name for e in collisions_player_enemy]}")
            # Exemplo futuro: Aplicar dano e interações
            # for enemy in collisions_player_enemy:
            #     player.take_damage(enemy.collision_damage)
            #     enemy.on_player_collision(player)
            pass

        # Este método pode retornar um dicionário com os resultados das colisões
        # ou acionar eventos/métodos nas entidades colididas diretamente.
        # Por enquanto, ele aplica a lógica de 'matar' os sprites conforme definido pelos `dokill`.
