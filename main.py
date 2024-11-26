import sys
import pygame as pg

# 画面サイズ
WIDTH = 320
HEIGHT = 270

# タイル数
TILE_X = 16
TILE_Y = 14

class Mario(pg.sprite.Sprite):
    ''' マリオのクラス '''
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        # 左右の向きフラグ
        self.__isLeft = False

        # マリオ画像読み込み
        self.__imgs = [
          pg.image.load('images/mario_001.png')
        ]

        self.image = self.__imgs[0]
        self.rect = pg.Rect(150, 200, 20, 20)

    def __right(self):
        self.rect.x += 5
        self.__isLeft = False

    def __left(self):
        self.rect.x -= 5
        self.__isLeft = True

    def update(self):
        # キーボードの状態を取得
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.__right()
        if keys[pg.K_LEFT]:
            self.__left()

        self.image = pg.transform.flip(self.__imgs[0], self.__isLeft, False)

class Kuriboh(pg.sprite.Sprite):
    ''' クリボーのクラス '''
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('images/kuriboh_001.png')
        self.rect = pg.Rect(180, 200, 20, 20)

class Nokonoko(pg.sprite.Sprite):
    ''' ノコノコのクラス '''
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('images/nokonoko_001.png')
        self.rect = pg.Rect(200, 200, 20, 20)

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
    # 各スプライトを構築してグループに追加
    mario = Mario()
    kuriboh = Kuriboh()
    nokonoko = Nokonoko()
    group.add(mario, kuriboh, nokonoko)

    # イベントループ
    while running:
        # イベント処理
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

        # 背景を水色に塗りつぶす
        win.fill((135, 206, 235))

        # グループの更新
        group.update()

        # グループの描画
        group.draw(win)

        # 画面を更新
        pg.display.flip()

        # フレームレートを設定
        clock.tick(30)

    pg.quit()
    sys.exit()

if __name__ == '__main__':
    main()
