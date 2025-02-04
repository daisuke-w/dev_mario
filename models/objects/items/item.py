import pygame as pg

from configs.config_manager import ConfigManager as cm
from utils.debug import debug_log


class Item(pg.sprite.Sprite):
    ''' アイテムの基底クラス '''
    def __init__(self, images, x, y, vy, item_type, player):
        super().__init__()
        self.dc = cm.get_display()
        self.gc = cm.get_game()

        self.item_type = item_type                      # アイテム種別
        self.player = player                            # プレイヤーの参照を保持
        self.imgs = images                              # 画像をリストで保持
        self.image = self.imgs[0]                       # 初期画像
        self.rect = pg.Rect(x, y, 20, 20)               # 位置を設定
        self.rect.topleft = (x, y)                      # 位置を設定
        self.vy = vy                                    # アイテムが出現するときの上方向の速度
        self.active = True                              # アイテムが動作中か
        self.on_ground = False                          # アイテムが地上にあるか
        self.on_block = True                            # アイテムがブロックの上にあるか
        self.appear_distance = self.gc.appear_distance  # アイテムがブロックから上に出現する幅

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
