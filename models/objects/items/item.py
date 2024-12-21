import pygame as pg

from utils.status import PlayerStatus as ps


class Item(pg.sprite.Sprite):
    ''' アイテムの基底クラス '''
    def __init__(self, images, x, y, vy, item_type, player):
        super().__init__()
        self.item_type = item_type
        # 画像をリストで保持
        self.imgs = images
        self.image = self.imgs[0]
        # 位置を設定
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        # アイテムが出現するときの上方向の速度
        self.vy = vy
        # アイテムが動作中か
        self.active = True
        # プレイヤーの参照を保持
        self.player = player

    def update(self, dt=0):
        # Game Over時は動かない
        if self.player.status in { ps.DYING, ps.GAME_OVER }:
            return

        if self.active:
            # 上方向に移動
            self.rect.y += self.vy
            # 上方向の移動が終わったら停止
            if self.vy < 0:
                self.vy = 0
                self.active = False
