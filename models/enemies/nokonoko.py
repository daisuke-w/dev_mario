import pygame as pg

from utils.settings import WIDTH
from models.enemies.enemy import Enemy


class Nokonoko(Enemy):
    ''' ノコノコのクラス '''
    def __init__(self):
        # ノコノコ用の画像、初期位置、速度を設定して親クラスを初期化
        images = [
            pg.image.load('images/nokonoko_001.png'),
            pg.image.load('images/nokonoko_002.png'),
            pg.image.load('images/nokonoko_003.png')
        ]
        super().__init__(images, 200, 200, -2)

    def reverse_direction(self):
        ''' 進行方向と画像の向きを反転する '''
        super().reverse_direction()
        # 左右フラグを反転
        self.isLeft = not self.isLeft
        # 現在の画像フレームに基づいて画像を更新
        current_img = self.frame_counter // 10 % 2
        self.image = pg.transform.flip(self.imgs[current_img], not self.isLeft, False)

    def update(self, dt=0):
        # 踏まれた後の処理
        # TODO ノコノコも一旦消える形にするが将来的には甲羅を蹴れるようにする
        if self.stomped:
            self.stomped_timer += 1
            if self.stomped_timer >= self.disappear_delay:
                # 一定時間経過後に削除
                self.kill()
            return

        # フレームカウンターを増加
        self.frame_counter += 1

         # 一定フレームごとにアニメーション
        if self.frame_counter % 10 == 0:
            current_img = self.frame_counter // 10 % 2
            self.image = pg.transform.flip(self.imgs[current_img], not self.isLeft, False)

        # X方向に移動
        self.rect.x += self.vx

        # 画面端で反転
        if self.rect.x <= 0 or self.rect.x >= WIDTH - self.rect.width:
            # 方向を反転
            self.vx = -self.vx
            self.isLeft = not self.isLeft

            # 即座に反転した画像を設定
            current_img = self.frame_counter // 10 % 2
            self.image = pg.transform.flip(self.imgs[current_img], not self.isLeft, False)
