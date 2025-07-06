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
        collisions_player_shot_enemy = pygame.sprite.groupcollide(
            player_shots_group, enemies_group, True, False
        )
        if collisions_player_shot_enemy:
            for shot, enemies_hit in collisions_player_shot_enemy.items():
                for enemy in enemies_hit:
                    enemy.take_damage(shot.damage)

        collisions_enemy_shot_player = pygame.sprite.spritecollide(
            player, enemy_shots_group, True
        )
        if collisions_enemy_shot_player:
            player.take_damage(amount=1)

        collisions_player_enemy = pygame.sprite.spritecollide(
            player, enemies_group, False
        )
        if collisions_player_enemy:
            pass