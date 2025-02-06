import pygame as pg

from models.objects.items.item import Item


class Coin(Item):
    ''' コインのクラス '''
    def __init__(self, x, y, player):
        # コイン用の画像
        images = [pg.image.load('images/coin_001.png')]
        # 初期位置、速度を設定して親クラスを初期化
        super().__init__(images, x, y, -10, 'coin', player)

        self.initial_top = 0  # アイテム生成時の初期高さ格納用

    def update(self, dt=0):
        if self.active:
            # 上昇するアニメーション
            self.rect.y += self.vy
            if self.rect.bottom <= self.initial_top - 50:
                self.vy = 0
                self.active = False

        if not self.active:
            self.vy += 1
            self.rect.y += self.vy
            if self.rect.bottom >= self.initial_top:
                self.kill()
