import pygame as pg

from utils.settings import WIDTH, HEIGHT, TILE_SIZE, BLOCK_MAP
from models.player.mario import Mario
from models.enemies.kuriboh import Kuriboh
from models.enemies.nokonoko import Nokonoko
from models.objects.block import Block


def game_init():
    '''
    スプライトを生成して返却
    
    return:
        win: 画面
        clock: クロック
        mario: プレイヤー
        group: プレイヤーと敵キャラクターのグループ
        enemies: 敵キャラクターグループ
        blocks: ブロックグループ
    '''
    # 画面作成
    win = pg.display.set_mode((WIDTH, HEIGHT))
    # クロックを生成
    clock = pg.time.Clock()

    # スプライトグループを定義
    group = pg.sprite.LayeredUpdates()
    # 敵キャラクターグループを定義
    enemies = pg.sprite.Group()
    # ブロックグループを定義
    blocks = pg.sprite.Group()
    # アイテムグループを定義
    items = pg.sprite.Group()

    # 各スプライトを構築してグループに追加
    mario = Mario()
    kuriboh = Kuriboh(mario)
    nokonoko = Nokonoko(mario)
    # ブロック画像を読み込み
    Block.load_images(TILE_SIZE)
    # ブロックを生成してグループに追加
    blocks = Block.create_blocks(BLOCK_MAP, TILE_SIZE)
    # グループに追加
    group.add(mario, layer=3)
    group.add(kuriboh, nokonoko, layer=2)
    group.add(blocks, layer=1)
    enemies.add(kuriboh, nokonoko)

    return win, clock, mario, group, enemies, blocks, items
