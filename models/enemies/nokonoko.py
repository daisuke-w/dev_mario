import pygame as pg

from utils.debug import debug_log
from models.enemies.enemy import Enemy
from utils.status import NokonokoStatus as ns


class Nokonoko(Enemy):
    ''' ノコノコのクラス '''
    def __init__(self, initial_x, initial_y, initial_vx, player):
        # ノコノコ用の画像
        images = [pg.image.load(f'images/nokonoko_00{i}.png') for i in range(1, 4)]
        # 初期位置、速度を設定して親クラスを初期化
        super().__init__(images, initial_x, initial_y, initial_vx, player)

        # ノコノコの初期状態
        self.__status = ns.NORMAL

    def reverse_direction(self):
        ''' 進行方向と画像の向きを反転する '''
        super().reverse_direction()
        # 左右フラグを反転 
        self.facing_left = not self.facing_left
        # 現在の画像フレームに基づいて画像を更新
        current_img = self.frame_counter // 10 % 2
        self.image = pg.transform.flip(self.imgs[current_img], not self.facing_left, False)

    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, value):
        self.__status = value

    def stomp(self):
        super().stomp()
        self.vx = 0
        self.status = ns.SHELL
        self.stomped_timer = self.game_conf.stomped_timer

    def kicked(self, direction):
        shell_speed = self.game_conf.shell_speed
        self.vx = shell_speed if direction == 'right' else -shell_speed
        self.status = ns.SHELL_MOVING
        self.stomped_timer = 0
        self.safe_timer = self.game_conf.safe_timer

    def update(self, dt=0):
        # 停止するステータスの確認
        if self.check_status():
            return

        super().update_common()

        # ノコノコの状態に応じて分岐(通常、甲羅、蹴られた状態)
        if self.status == ns.SHELL:
            self.image = self.imgs[2]
            if self.stomped_timer > 0:
                self.stomped_timer -= 1
            return
        elif self.status == ns.SHELL_MOVING:
            self.image = self.imgs[2]
            self.rect.x += self.vx
            if self.safe_timer > 0:
                self.safe_timer -= 1
            return
        elif self.status == ns.NORMAL:
            # 一定フレームごとにアニメーション
            if self.frame_counter % 10 == 0:
                current_img = self.frame_counter // 10 % 2
                self.image = pg.transform.flip(self.imgs[current_img], not self.facing_left, False)
