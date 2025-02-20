import pygame as pg

import utils.collision as col

from models.objects.items.item import Item
from utils.debug import debug_log
from utils.settings import BLOCK_MAP
from utils.status import PlayerStatus as ps


class Kinoko(Item):
    ''' キノコのクラス '''
    def __init__(self, x, y, player):
        # キノコ用の画像
        images = [pg.image.load('images/kinoko_001.png')]
        # 初期位置、速度を設定して親クラスを初期化
        super().__init__(images, x, y, 2, 'kinoko', player)

        self.vx = 2             # 横方向の速度
        self.initial_top = 0    # アイテム生成時の初期高さ格納用

    def update(self, dt=0):
        if self.player.status in { ps.GROWING, ps.SHRINKING, ps.DYING, ps.GAME_OVER }:
            return

        if self.active:
            # 上昇して出現するアニメーション
            self.rect.y -= self.vy
            if self.initial_top - self.rect.y == self.appear_distance:
                self.vy = 0
                self.active = False

        # 出現アニメーション終了後の動作
        if not self.active:
            self.rect.x += self.vx
            result = col.is_touching_item_block_below(self, self.dc.tile_size, BLOCK_MAP)
            if not result and not self.on_ground:
                self.apply_gravity()
                self.on_block = False
                if self.rect.y > self.dc.height:
                    self.kill()
