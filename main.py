import sys
import pygame as pg

from settings import WIDTH, HEIGHT
from mario import Mario
from kuriboh import Kuriboh
from nokonoko import Nokonoko

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
    # 各スプライトを構築してグループに追加
    mario = Mario()
    kuriboh = Kuriboh()
    nokonoko = Nokonoko()
    # グループに追加
    group.add(mario, kuriboh, nokonoko)
    enemies.add(kuriboh, nokonoko)

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
