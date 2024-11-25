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

  def __right(self):
    self.rect.x += 5
  
  def __left(self):
    self.rect.x -= 5

  def update(self):
    # キーボードの状態を取得
    keys = pg.key.get_pressed()
    if keys[pg.K_RIGHT]:
      self.__right()
    if keys[pg.K_LEFT]:
      self.__left()

class Kuriboh(pg.sprite.Sprite):
  ''' クリボーのクラス
  '''
  def __init__(self):
    pg.sprite.Sprite.__init__(self)

    self.image = pg.image.load('images/kuriboh_001.png')
    self.rect = pg.Rect(180, 200, 20, 20)

class Nokonoko(pg.sprite.Sprite):
  ''' ノコノコのクラス
  '''
  def __init__(self):
    pg.sprite.Sprite.__init__(self)

    self.image = pg.image.load('images/nokonoko_001.png')
    self.rect = pg.Rect(200, 200, 20, 20)

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
    # ノコノコクラスを構築
    nokonoko = Nokonoko()
    # マリオをグループに追加
    group.add(mario)
    # クリボーをグループに追加
    group.add(kuriboh)
    # ノコノコをグループに追加
    group.add(nokonoko)

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

      # フレームレートを設定
      clock.tick(30)

if __name__ == '__main__':
    main()
