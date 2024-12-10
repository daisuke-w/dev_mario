import sys
import pygame as pg

from debug import debug_log
from settings import WIDTH, HEIGHT, TILE_SIZE, BLOCK_MAP
from mario import Mario
from kuriboh import Kuriboh
from nokonoko import Nokonoko
from block import Block

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
        if pg.sprite.collide_rect(mario, kuriboh):
            if not kuriboh.is_stomped():
                # マリオの底辺がクリボーの上辺に触れているかを確認
                if mario.is_falling() and mario.rect.bottom <= kuriboh.rect.top + 5:
                    kuriboh.stomp()
                else:
                    mario.set_game_over()

        # ノコノコ衝突判定
        if pg.sprite.collide_rect(mario, nokonoko):
            if not nokonoko.is_stomped():
                # マリオの底辺がノコノコの上辺に触れているかを確認
                if mario.is_falling() and mario.rect.bottom <= nokonoko.rect.top + 5:
                    nokonoko.stomp()
                else:
                    mario.set_game_over()

        # 敵キャラクター同士の衝突判定
        # 判定したペアを管理
        processed = set()
        for enemy in enemies:
            collided = pg.sprite.spritecollide(enemy, enemies, False)
            for other in collided:
                # 同じ衝突ペアが複数回処理されるのを回避（A が B と衝突）（B が A と衝突）
                if other != enemy and (enemy, other) not in processed and (other, enemy) not in processed:
                    if isinstance(enemy, (Kuriboh, Nokonoko)) and isinstance(other, (Kuriboh, Nokonoko)):
                        enemy.reverse_direction()
                        other.reverse_direction()
                        # 衝突判定したペアを記録
                        processed.add((enemy, other))

        # ブロックとの衝突判定
        collided_blocks = pg.sprite.spritecollide(mario, blocks, False)
        if collided_blocks:
            top_block = max(collided_blocks, key=lambda block: block.rect.top)
            # 上からの衝突
            if mario.is_falling() and mario.rect.bottom <= top_block.rect.top + 6:
                if not mario.on_block:
                    mario.land_on_block(top_block.rect.top)
            # 下からの衝突（ジャンプ時）
            elif mario.vy < 0:
                mario.rect.top = top_block.rect.bottom
                mario.vy = 0
            # 左右の衝突
            elif mario.rect.right >= top_block.rect.left and mario.rect.left < top_block.rect.centerx:
                mario.rect.right = top_block.rect.left + 2
            elif mario.rect.left <= top_block.rect.right and mario.rect.right > top_block.rect.centerx:
                mario.rect.left = top_block.rect.right + 2
        else:
            # マリオの下に他のブロックがない場合は `leave_block` を呼び出す
            block_below = [
                block for block in blocks
                if mario.rect.left < block.rect.right and mario.rect.right > block.rect.left
                and 0 <= block.rect.top - mario.rect.bottom <= 5
            ]
            if not block_below and mario.on_block:
                mario.leave_block()

        # グループの更新
        group.update()
        # グループの描画
        group.draw(win)
        # 画面を更新
        pg.display.flip()
        # フレームレートを設定(1秒間に30フレーム)
        clock.tick(30)

    pg.quit()
    sys.exit()

if __name__ == '__main__':
    main()
