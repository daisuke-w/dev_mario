import pygame as pg


class Enemy(pg.sprite.Sprite):
    ''' 敵キャラクターの基底クラス '''
    def __init__(self, images, initial_x, initial_y, initial_vx):
        pg.sprite.Sprite.__init__(self)

        # 画像をリストで保持
        self.imgs = images
        self.image = self.imgs[0]
        self.rect = pg.Rect(initial_x, initial_y, 20, 20)

        # 横方向の速度
        self.vx = initial_vx
        # 左右フラグ
        self.isLeft = True
        # フレームカウンター
        self.frame_counter = 0
        # 踏まれたかどうか
        self.stomped = False
        # 踏まれた後の経過フレーム
        self.stomped_timer = 0
        # 踏まれた後消えるまでの時間（フレーム数）
        self.disappear_delay = 15

    def is_stomped(self):
        return self.stomped

    def stomp(self):
        self.stomped = True
        self.image = self.imgs[2]

    def reverse_direction(self):
        self.vx *= -1
