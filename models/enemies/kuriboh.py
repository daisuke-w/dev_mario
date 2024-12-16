import pygame as pg

from utils.settings import WIDTH
from models.enemies.enemy import Enemy


class Kuriboh(Enemy):
    ''' クリボーのクラス '''
    def __init__(self):
        # クリボー用の画像、初期位置、速度を設定して親クラスを初期化
        images = [
            pg.image.load('images/kuriboh_001.png'),
            pg.image.load('images/kuriboh_002.png'),
            pg.image.load('images/kuriboh_003.png')
        ]
        super().__init__(images, 180, 200, 2)

    def update(self, dt=0):
        # 踏まれた後の処理
        if self.stomped:
            self.stomped_timer += 1
            if self.stomped_timer >= self.disappear_delay:
                # 一定時間経過後に削除
                self.kill()
            return

        # フレームカウンターを増加
        self.frame_counter += 1

        # 一定フレームごとに画像を切り替える
        if self.frame_counter % 10 == 0:
            self.image = self.imgs[self.frame_counter // 10 % 2]

        # X方向に移動
        self.rect.x += self.vx

        # 画面端で反転
        if self.rect.x <= 0 or self.rect.x >= WIDTH - self.rect.width:
            # 方向を反転
            self.vx = -self.vx
