import sys
import pygame as pg

# 画面サイズ
WIDTH = 320
HEIGHT = 270

# タイル数
TILE_X = 16
TILE_Y = 14

def main():
    '''メイン関数
    '''
    # Pygameの初期化
    pg.init()

    # 画面作成
    win = pg.display.set_mode((WIDTH, HEIGHT))

    # クロックを生成
    clock = pg.time.Clock()

    # イベントループ
    while True:
      for e in pg.event.get():
        if e.type == pg.QUIT:
          pg.quit()
          sys.exit()

        # 背景を水色に塗りつぶす
        win.fill((135, 206, 235))

        # 画面を更新
        pg.display.flip()

if __name__ == '__main__':
    main()
