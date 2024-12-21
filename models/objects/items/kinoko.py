import pygame as pg

from models.objects.items.item import Item


class Kinoko(Item):
    ''' キノコのクラス '''
    def __init__(self, x, y, player):
        # キノコ用の画像、初期位置、速度を設定して親クラスを初期化
        images = [
            pg.image.load('images/kinoko_001.png')
        ]
        super().__init__(images, x, y, -2, 'kinoko', player)
        self.vx = 2

    def update(self, dt=0):
        super().update()
        # 出現アニメーション終了後の動作
        if not self.active:
            self.rect.x += self.vx
