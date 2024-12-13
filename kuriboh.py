import pygame as pg
from settings import WIDTH


class Kuriboh(pg.sprite.Sprite):
    ''' クリボーのクラス '''
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        # 画像をリストで保持
        self.__imgs = [
            pg.image.load('images/kuriboh_001.png'),
            pg.image.load('images/kuriboh_002.png'),
            pg.image.load('images/kuriboh_003.png')
        ]

        self.image = self.__imgs[0]
        self.rect = pg.Rect(180, 200, 20, 20)

        # 横方向の速度
        self.__vx = 2
        # フレームカウンター
        self.__frame_counter = 0
        # 踏まれたかどうか
        self.__stomped = False
        # 踏まれた後の経過フレーム
        self.__stomped_timer = 0
        # 踏まれた後消えるまでの時間（フレーム数）
        self.__disappear_delay = 15

    @property
    def vx(self):
        return self.__vx

    def is_stomped(self):
        return self.__stomped

    def stomp(self):
        self.__stomped = True
        self.image = self.__imgs[2]

    def reverse_direction(self):
        self.__vx *= -1

    def update(self, dt=0):
        # 踏まれた後の処理
        if self.__stomped:
            self.__stomped_timer += 1
            if self.__stomped_timer >= self.__disappear_delay:
                # 一定時間経過後に削除
                self.kill()
            return

        # フレームカウンターを増加
        self.__frame_counter += 1

        # 一定フレームごとに画像を切り替える
        if self.__frame_counter % 10 == 0:
            self.image = self.__imgs[self.__frame_counter // 10 % 2]

        # X方向に移動
        self.rect.x += self.__vx

        # 画面端で反転
        if self.rect.x <= 0 or self.rect.x >= WIDTH - self.rect.width:
            # 方向を反転
            self.__vx = -self.__vx
