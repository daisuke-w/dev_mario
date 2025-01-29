import pygame as pg

from utils.debug import debug_log
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
        self.rect = pg.Rect(x, y, 20, 20)
        self.rect.topleft = (x, y)
        # アイテムが出現するときの上方向の速度
        self.vy = vy
        # アイテムが動作中か
        self.active = True
        # プレイヤーの参照を保持
        self.player = player
        # アイテムが地上にあるか
        self.on_ground = False
        # アイテムがブロックの上にあるか
        self.on_block = True
        # 出現する距離
        self.appear_distance = 20

    def apply_gravity(self):
        self.rect.y += self.vy
        self.vy += 1

    def is_falling(self):
        return self.vy > 0

    def land_on_block(self, top):
        # ブロックの上に乗る
        self.rect.bottom = top
        # 垂直速度をリセット
        self.vy = 0
        self.on_ground = False
        self.on_block = True

    def update(self, dt=0):
        # Game Over時は動かない
        if self.player.status in { ps.DYING, ps.GAME_OVER }:
            return
