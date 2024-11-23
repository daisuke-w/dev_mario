import sys
import pygame as pg

# 画面サイズ
WIDTH = 320
HEIGHT = 270

# タイル数
TILE_X = 16
TILE_Y = 14

class Mario(pg.sprite.Sprite):
  ''' マリオのクラス
  '''
  def __init__(self):
    pg.sprite.Sprite.__init__(self)

    self.image = pg.image.load('images/mario_001.png')
    self.rect = pg.Rect(150, 200, 20, 20)

def main():
    ''' メイン関数
    '''
    # Pygameの初期化
    pg.init()

    # 画面作成
    win = pg.display.set_mode((WIDTH, HEIGHT))

    # クロックを生成
    clock = pg.time.Clock()

    # スプライトグループを定義
    group = pg.sprite.RenderUpdates()
    # マリオクラスを構築
    mario = Mario()
    # マリオをグループに追加
    group.add(mario)

    # イベントループ
    while True:
      for e in pg.event.get():
        if e.type == pg.QUIT:
          pg.quit()
          sys.exit()

        # 背景を水色に塗りつぶす
        win.fill((135, 206, 235))

        # グループを更新
        group.update()

        # グループを描画
        group.draw(win)

        # 画面を更新
        pg.display.flip()

if __name__ == '__main__':
    main()
