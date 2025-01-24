import pygame as pg

from utils.debug import debug_log
from utils.settings import TILE_SIZE, BLOCK_MAP
from models.enemies.nokonoko import Nokonoko
from utils.status import NokonokoStatus as ns
from utils.status import PlayerStatus as ps


def player_enemy_collision(player, enemy):
    '''
    マリオと敵の衝突判定

    Args:
        player: プレイヤーオブジェクト
        enemy: 敵キャラクターオブジェクト
    '''
    if pg.sprite.collide_rect(player, enemy):
        # 無敵状態なので衝突判定を実行しない
        if player.is_invincible:
            return

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
            if player.is_falling() and player.rect.bottom <= enemy.rect.top + 10:
                enemy.stomp()
            else:
                if player.is_big() or player.is_shrink():
                    player.status = ps.SHRINKING
                    player.is_invincible = True
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

def player_block_collision(group, player, blocks, items):
    '''
    プレイヤーと壁の衝突判定

    Args:
        player: プレイヤーオブジェクト
        blocks: 衝突判定を行うブロックグループ
    '''
    collided_blocks = pg.sprite.spritecollide(player, blocks, False)
    if collided_blocks:
        top_block = min(collided_blocks, key=lambda block: block.rect.top)
        # 上からの衝突
        if player.is_falling() and player.rect.bottom <= top_block.rect.top + 12:
            if not player.on_block:
                player.land_on_block(top_block.rect.top)
        # 下からの衝突（ジャンプ時）
        elif player.vy < 0:
            if player.is_big() and top_block.cell_type == 2:
                top_block.break_into_fragments(group)
            else:
                player.rect.top = top_block.rect.bottom
                player.vy = 0
            if top_block.cell_type == 3:
                top_block.release_item(group, items, player)
        # 左からの衝突
        elif player.rect.right >= top_block.rect.left and player.rect.left < top_block.rect.centerx:
            player.rect.right = top_block.rect.left - 2
        # 右からの衝突
        elif player.rect.left <= top_block.rect.right and player.rect.right > top_block.rect.centerx:
            player.rect.left = top_block.rect.right + 2
    else:
        # マリオの下に他のブロックがない場合は `leave_block` を呼び出す
        result = is_touching_block_below(player.rect, TILE_SIZE, BLOCK_MAP)
        if not result and player.on_block:
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

def item_block_collision(items, blocks):
    '''
    アイテムとブロックの衝突判定処理
    Args:
        items: アイテムのグループ
        blocks: ブロックのグループ
    '''
    for item in items:
        if item.active:
            continue

        # 衝突判定
        if item.on_ground:
            collisions = pg.sprite.spritecollide(item, blocks, False)
            if collisions:
                for block in collisions:
                    # 横方向の衝突（壁との接触）
                    if item.vx != 0:
                        if item.rect.right > block.rect.left and item.vx > 0:
                            item.rect.right = block.rect.left
                            item.vx *= -1
                        elif item.rect.left < block.rect.right and item.vx < 0:
                            item.rect.left = block.rect.right
                            item.vx *= -1

def player_item_collision(player, items):
    '''
    マリオとアイテムの衝突判定

    Args:
        player: プレイヤーオブジェクト
        items: アイテムオブジェクト
    '''
    for item in items:
        if item.active:
            continue

        if player.rect.colliderect(item.rect):
            item.kill()
            player.grow()

def is_touching_block_below(target_rect, tile_size, block_map):
    '''
    targetが下のブロックに触れているかを確認
    '''
    bottom_tile_y = (target_rect.bottom - 1) // tile_size
    left_tile_x = target_rect.left // tile_size
    right_tile_x = (target_rect.right - 1) // tile_size

    # アイテムがタイルサイズに差し掛かった際にTrueを返却しないようにする暫定対応
    # 例えば地面が220:240の位置にある時、
    # アイテムのbottomが205等に入ると200:220のエリアにいることになり、Trueを返却してしまうが
    # 画面上は地面(220)に触れていない為浮いた状態になってしまう
    # 地面の位置により値が変動する為この対応ではまずい
    if 200 <= target_rect.bottom < 220:
        return False 

    if bottom_tile_y + 1 < len(block_map):
        for x in range(left_tile_x, right_tile_x + 1):
            if 0 <= x < len(block_map[0]):
                if block_map[bottom_tile_y + 1][x] != 0:
                    return True
    return False
