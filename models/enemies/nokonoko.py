import pygame as pg

from utils.settings import WIDTH, SHELL_SPEED
from models.enemies.enemy import Enemy
from utils.status import PlayerStatus as ps
from utils.status import NokonokoStatus as ns


class Nokonoko(Enemy):
    ''' ノコノコのクラス '''
    def __init__(self, player):
        # ノコノコ用の画像、初期位置、速度を設定して親クラスを初期化
        images = [
            pg.image.load('images/nokonoko_001.png'),
            pg.image.load('images/nokonoko_002.png'),
            pg.image.load('images/nokonoko_003.png')
        ]
        super().__init__(images, 200, 200, -2, player)

        # ノコノコの状態
        self.__status = ns.NORMAL

    def reverse_direction(self):
        ''' 進行方向と画像の向きを反転する '''
        super().reverse_direction()
        # 左右フラグを反転
        self.isLeft = not self.isLeft
        # 現在の画像フレームに基づいて画像を更新
        current_img = self.frame_counter // 10 % 2
        self.image = pg.transform.flip(self.imgs[current_img], not self.isLeft, False)

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
        self.stomped_timer = 15

    def kicked(self, direction):
        self.vx = SHELL_SPEED if direction == 'right' else -SHELL_SPEED
        self.status = ns.SHELL_MOVING
        self.stomped_timer = 0
        self.safe_timer = 15

    def update(self, dt=0):
        # Game Over時は動かない
        if self.player.status in { ps.GROWING, ps.DYING, ps.GAME_OVER }:
            return

        # フレームカウンターを増加
        self.frame_counter += 1

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
        if self.status == ns.NORMAL:
            # 一定フレームごとにアニメーション
            if self.frame_counter % 10 == 0:
                current_img = self.frame_counter // 10 % 2
                self.image = pg.transform.flip(self.imgs[current_img], not self.isLeft, False)

        # X方向に移動
        self.rect.x += self.vx

        # 画面端で反転
        if self.rect.x <= 0 or self.rect.x >= WIDTH - self.rect.width:
            # 方向を反転
            self.reverse_direction()
