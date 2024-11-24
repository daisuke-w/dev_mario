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

class Kuriboh(pg.sprite.Sprite):
  ''' クリボーのクラス
  '''
  def __init__(self):
    pg.sprite.Sprite.__init__(self)

    self.image = pg.image.load('images/kuriboh_001.png')
    self.rect = pg.Rect(180, 200, 20, 20)

def main():
    ''' メイン関数
    '''
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
    # マリオクラスを構築
    mario = Mario()
    # クリボークラスを構築
    kuriboh = Kuriboh()
    # マリオをグループに追加
    group.add(mario)
    # クリボーをグループに追加
    group.add(kuriboh)


    # イベントループ
    while running:
      for e in pg.event.get():
        if e.type == pg.QUIT:
          running = False
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
