import pygame as pg

from models.enemies.nokonoko import Nokonoko
from utils.status import NokonokoStatus as ns


def player_enemy_collision(player, enemy):
    '''
    マリオと敵の衝突判定

    Args:
        player: プレイヤーオブジェクト
        enemy: 敵キャラクターオブジェクト
    '''
    if pg.sprite.collide_rect(player, enemy):
        # ノコノコが甲羅状態で動いている場合
        if isinstance(enemy, Nokonoko) and enemy.status == ns.SHELL_MOVING:
            if enemy.safe_timer == 0: 
                player.set_game_over()
                return

         # ノコノコが甲羅状態の場合
        if isinstance(enemy, Nokonoko) and enemy.status == ns.SHELL:
            # 一定時間経過後蹴る
            if enemy.stomped_timer == 0:  
                if player.rect.centerx < enemy.rect.centerx:
                    enemy.kicked('right')
                else:
                    enemy.kicked('left')
            return

        if not enemy.is_stomped():
            if player.is_falling() and player.rect.bottom <= enemy.rect.top + 5:
                enemy.stomp()
            else:
                player.set_game_over()

def enemies_collision(processed, enemy, enemies):
    '''
    敵キャラクター同士の衝突判定

    Args:
        processed: 判定したペアを管理する
        enemy: 敵キャラクターオブジェクト
        enemies: 衝突判定を行う敵キャラクターグループ
    '''
    collided = pg.sprite.spritecollide(enemy, enemies, False)
    for other in collided:
        # 同じ衝突ペアが複数回処理されるのを回避
        if other != enemy and (enemy, other) not in processed and (other, enemy) not in processed:
            # ノコノコが甲羅移動中の場合
            if isinstance(enemy, Nokonoko) and enemy.status == ns.SHELL_MOVING:
                # 衝突相手を倒す
                enemies.remove(other)
                other.kill()
                continue

            if isinstance(other, Nokonoko) and other.status == ns.SHELL_MOVING:
                # 自分を削除
                enemies.remove(enemy)
                enemy.kill()
                continue

            # 通常の敵同士の衝突処理
            enemy.reverse_direction()
            other.reverse_direction()
            # 衝突判定したペアを記録
            processed.add((enemy, other))

def player_block_collision(player, blocks):
    '''
    プレイヤーと壁の衝突判定

    Args:
        player: プレイヤーオブジェクト
        blocks: 衝突判定を行うブロックグループ
    '''
    collided_blocks = pg.sprite.spritecollide(player, blocks, False)
    if collided_blocks:
        top_block = max(collided_blocks, key=lambda block: block.rect.top)
        # 上からの衝突
        if player.is_falling() and player.rect.bottom <= top_block.rect.top + 12:
            if not player.on_block:
                player.land_on_block(top_block.rect.top)
        # 下からの衝突（ジャンプ時）
        elif player.vy < 0:
            player.rect.top = top_block.rect.bottom
            player.vy = 0
        # 左右の衝突
        elif player.rect.right >= top_block.rect.left and player.rect.left < top_block.rect.centerx:
            player.rect.right = top_block.rect.left + 2
        elif player.rect.left <= top_block.rect.right and player.rect.right > top_block.rect.centerx:
            player.rect.left = top_block.rect.right + 2
    else:
        # マリオの下に他のブロックがない場合は `leave_block` を呼び出す
        block_below = [
            block for block in blocks
            if player.rect.left < block.rect.right and player.rect.right > block.rect.left
            and 0 <= block.rect.top - player.rect.bottom <= 5
        ]
        if not block_below and player.on_block:
            player.leave_block()


def enemy_block_collision(enemy, blocks):
    '''
    敵キャラクターと壁の衝突判定

    Args:
        enemy: 敵キャラクターオブジェクト
        blocks: 衝突判定を行うブロックグループ
    '''
    # 壁（ブロック）との衝突判定
    collided_blocks = pg.sprite.spritecollide(enemy, blocks, False)
    for block in collided_blocks:
        # 右に移動中
        if enemy.vx > 0:
            if enemy.rect.right >= block.rect.left:
                enemy.rect.right = block.rect.left
                enemy.reverse_direction()
        # 左に移動中
        elif enemy.vx < 0:
            if enemy.rect.left <= block.rect.right:
                enemy.rect.left = block.rect.right
                enemy.reverse_direction()
