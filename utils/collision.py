import pygame as pg

from configs.config_manager import ConfigManager as cm
from models.enemies.nokonoko import Nokonoko
from models.objects.block import Block
from utils.debug import debug_log
from utils.settings import BLOCK_MAP
from utils.status import NokonokoStatus as ns


def handle_nokonoko_state(player, enemy):
    # ノコノコが通常状態の場合
    if enemy.status == ns.NORMAL:
        return
    # ノコノコが甲羅状態の場合
    elif enemy.status == ns.SHELL:
        # 一定時間経過後蹴る
        if enemy.stomped_timer == 0:
            if player.rect.centerx < enemy.rect.centerx:
                enemy.kicked('right')
            else:
                enemy.kicked('left')
    # ノコノコが甲羅状態で動いている場合
    elif enemy.status == ns.SHELL_MOVING:
        if enemy.safe_timer == 0: 
                player.set_game_over()

def handle_nokonoko_kill(enemy, other, enemies):
    # ノコノコが甲羅移動中の場合
    if isinstance(enemy, Nokonoko) and enemy.status == ns.SHELL_MOVING:
        # 衝突相手を倒す
        enemies.remove(other)
        other.kill()
    elif isinstance(other, Nokonoko) and other.status == ns.SHELL_MOVING:
        # 自分を削除
        enemies.remove(enemy)
        enemy.kill()

def handle_block_direction(player, top_block, group, items):
    bt = cm.get_block().types
    # 上からの衝突
    if player.is_falling() and player.rect.bottom <= top_block.rect.top + 12:
        if not player.on_block:
            player.land_on_block(top_block.rect.top)
    # 下からの衝突（ジャンプ時）
    elif player.vy < 0:
        if player.is_big() and top_block.cell_type == bt.block:
            top_block.break_into_fragments(group)
        else:
            player.rect.top = top_block.rect.bottom
            player.vy = 0
        if top_block.cell_type == bt.hatena_kinoko:
            top_block.release_item(group, items, player)
        elif top_block.cell_type == bt.hatena_coin:
            top_block.release_item(group, items, player)
    # 左からの衝突
    elif player.rect.right >= top_block.rect.left and player.rect.left < top_block.rect.centerx:
        player.rect.right = top_block.rect.left - 2
    # 右からの衝突
    elif player.rect.left <= top_block.rect.right and player.rect.right > top_block.rect.centerx:
        player.rect.left = top_block.rect.right + 2

def handle_item_horizontal(item, collisions):
    for block in collisions:
        if item.rect.right > block.rect.left and item.vx > 0:
            item.rect.right = block.rect.left
            item.vx *= -1
        elif item.rect.left < block.rect.right and item.vx < 0:
            item.rect.left = block.rect.right
            item.vx *= -1

def handle_item_vertical(item, collisions):
    for block in collisions:
        if item.is_falling() and item.rect.bottom <= block.rect.top + 12:
            item.land_on_block(block.rect.top)
            if block.cell_type == 1:
                item.on_ground = True

def player_enemy_collision(player, enemy):
    '''
    プレイヤーと敵の衝突判定

    Args:
        player: プレイヤーオブジェクト
        enemy: 敵キャラクターオブジェクト
    '''
    if pg.sprite.collide_rect(player, enemy):
        # 無敵状態なので衝突判定を実行しない
        if player.is_invincible:
            return

        if isinstance(enemy, Nokonoko):
            handle_nokonoko_state(player, enemy)

        if not enemy.is_stomped():
            if player.is_falling() and player.rect.bottom <= enemy.rect.top + 10:
                enemy.stomp()
            else:
                if player.is_big() or player.is_shrink():
                    player.shrink()
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
            handle_nokonoko_kill(enemy, other, enemies)
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
    gc = cm.get_display()
    if collided_blocks:
        top_block = min(collided_blocks, key=lambda block: block.rect.top)
        # ブロックとの衝突方向で処理分岐
        handle_block_direction(player, top_block, group, items)
    else:
        # プレイヤーの下に他のブロックがない場合は `leave_block` を呼び出す
        result = is_touching_player_block_below(player, gc.tile_size, BLOCK_MAP)
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
        # アイテム出現中は衝突判定をスキップ
        if item.active:
            continue

        # 衝突がない場合はスキップ
        collisions = pg.sprite.spritecollide(item, blocks, False)
        if not collisions:
            continue

        # 横方向の衝突処理
        if item.on_ground and item.vx != 0:
            handle_item_horizontal(item, collisions)

        # 縦方向の衝突処理
        if not item.on_ground and not item.on_block:
            handle_item_vertical(item, collisions)


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

def is_touching_player_block_below(player, tile_size, block_map):
    '''
    プレイヤーが下のブロックに触れているかを確認
    '''
    bottom_tile_y = (player.rect.bottom - 1) // tile_size
    left_tile_x = player.rect.left // tile_size
    right_tile_x = (player.rect.right - 1) // tile_size

    if bottom_tile_y + 1 < len(block_map):
        for x in range(left_tile_x, right_tile_x + 1):
            if 0 <= x < len(block_map[0]):
                if block_map[bottom_tile_y + 1][x] != 0:
                    if not Block.get_block(x, bottom_tile_y + 1).is_destroyed:
                        # ブロックが破壊されていない場合
                        return True
    return False

def is_touching_item_block_below(item, tile_size, block_map):
    '''
    アイテムが下のブロックに触れているかを確認
    '''
    bottom_tile_y = (item.rect.bottom - 1) // tile_size
    left_tile_x = item.rect.left // tile_size
    right_tile_x = (item.rect.right - 1) // tile_size

    if bottom_tile_y + 1 < len(block_map):
        for x in range(left_tile_x, right_tile_x + 1):
            if 0 <= x < len(block_map[0]):
                if block_map[bottom_tile_y + 1][x] != 0:
                    block = Block.get_block(x, bottom_tile_y + 1)
                    if not block.is_destroyed:
                        # ブロックが破壊されていない場合
                        if abs(item.rect.bottom - block.rect.top) <= 2:
                            return True
    return False
