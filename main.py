import sys
import pygame as pg

import utils.collision as col
from utils.debug import debug_log
from utils.settings import WIDTH, HEIGHT, TILE_SIZE, BLOCK_MAP
from models.characters.mario import Mario
from models.enemies.kuriboh import Kuriboh
from models.enemies.nokonoko import Nokonoko
from models.objects.block import Block

def main():
    ''' メイン関数 '''
    # Pygameの初期化
    pg.init()
    # イベント実行フラグ
    running = True

    # 画面作成
    win = pg.display.set_mode((WIDTH, HEIGHT))

    # クロックを生成
    clock = pg.time.Clock()

    # スプライトグループを定義
    group = pg.sprite.RenderUpdates()
    # 敵キャラクターグループを定義
    enemies = pg.sprite.Group()
    # ブロックグループを定義
    blocks = pg.sprite.Group()

    # 各スプライトを構築してグループに追加
    mario = Mario()
    kuriboh = Kuriboh()
    nokonoko = Nokonoko()
    # グループに追加
    group.add(mario, kuriboh, nokonoko)
    enemies.add(kuriboh, nokonoko)

    # ブロック画像を読み込み
    Block.load_images(TILE_SIZE)
    # ブロックを生成してグループに追加
    blocks = Block.create_blocks(BLOCK_MAP, TILE_SIZE)
    group.add(blocks)

    # イベントループ
    while running:
        # イベント処理
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

        # 背景を水色に塗りつぶす
        win.fill((135, 206, 235))

        # クリボー衝突判定
        col.player_enemy_collision(mario, kuriboh)

        # ノコノコ衝突判定
        col.player_enemy_collision(mario, nokonoko)

        # 敵キャラクター同士の衝突判定
        col.enemies_collision(enemies)

        # 敵キャラクターと壁の衝突判定
        col.enemy_block_collision(enemies, blocks)

        # ブロックとの衝突判定
        col.player_block_collision(mario, blocks)

        # フレームレートを設定(1秒間に30フレーム)
        dt = clock.tick(30)
        # グループの更新
        group.update(dt)
        # グループの描画
        group.draw(win)
        # 画面を更新
        pg.display.flip()

    pg.quit()
    sys.exit()

if __name__ == '__main__':
    main()
