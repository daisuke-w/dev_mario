import pygame as pg
from utils.settings import WIDTH


class Nokonoko(pg.sprite.Sprite):
    ''' ノコノコのクラス '''
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        # 画像をリストで保持
        self.__imgs = [
            pg.image.load('images/nokonoko_001.png'),
            pg.image.load('images/nokonoko_002.png'),
            pg.image.load('images/nokonoko_003.png')
        ]

        self.image = self.__imgs[0]
        self.rect = pg.Rect(200, 200, 20, 20)

        # 左右フラグ
        self.__isLeft = True
        # 横方向の速度
        self.__vx = -2
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
        ''' 進行方向と画像の向きを反転する '''
        self.__vx *= -1
        # 左右フラグを反転
        self.__isLeft = not self.__isLeft
        # 現在の画像フレームに基づいて画像を更新
        current_img = self.__frame_counter // 10 % 2
        self.image = pg.transform.flip(self.__imgs[current_img], not self.__isLeft, False)

    def update(self, dt=0):
        # 踏まれた後の処理
        # TODO ノコノコも一旦消える形にするが将来的には甲羅を蹴れるようにする
        if self.__stomped:
            self.__stomped_timer += 1
            if self.__stomped_timer >= self.__disappear_delay:
                # 一定時間経過後に削除
                self.kill()
            return

        # フレームカウンターを増加
        self.__frame_counter += 1
        # X方向に移動
        self.rect.x += self.__vx

        # 画面端で反転
        if self.rect.x <= 0 or self.rect.x >= WIDTH - self.rect.width:
            # 方向を反転
            self.__vx = -self.__vx
            self.__isLeft = not self.__isLeft

            # 即座に反転した画像を設定
            current_img = self.__frame_counter // 10 % 2
            self.image = pg.transform.flip(self.__imgs[current_img], not self.__isLeft, False)

            # 反転後すぐに処理を終了する
            return

        # 一定フレームごとにアニメーション
        if self.__frame_counter % 10 == 0:
            current_img = self.__frame_counter // 10 % 2
            self.image = pg.transform.flip(self.__imgs[current_img], not self.__isLeft, False)
