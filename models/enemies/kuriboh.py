import pygame as pg

from utils.debug import debug_log
from models.enemies.enemy import Enemy


class Kuriboh(Enemy):
    ''' クリボーのクラス '''
    def __init__(self, initial_x, initial_y, initial_vx, player, camera):
        # クリボー用の画像
        images = [pg.image.load(f'images/kuriboh_00{i}.png') for i in range(1, 4)]
        # 初期位置、速度を設定して親クラスを初期化
        super().__init__(images, initial_x, initial_y, initial_vx, player, camera)

    def update(self, dt=0):
        # 停止するステータスの確認
        if self.check_status():
            return

        super().update_common()

        # 踏まれた後の処理
        if self.stomped:
            self.stomped_timer += 1
            if self.stomped_timer >= self.disappear_delay:
                # 一定時間経過後に削除
                self.kill()
            return

        # 一定フレームごとに画像を切り替える
        if self.frame_counter % 10 == 0:
            self.image = self.imgs[self.frame_counter // 10 % 2]

