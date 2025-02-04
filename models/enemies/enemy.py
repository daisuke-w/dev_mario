import pygame as pg

from configs.config_manager import ConfigManager as cm
from utils.status import PlayerStatus as ps


class Enemy(pg.sprite.Sprite):
    ''' 敵キャラクターの基底クラス '''
    def __init__(self, images, initial_x, initial_y, initial_vx, player):
        super().__init__()
        self.dc = cm.get_display()
        self.gc = cm.get_game()

        self.vx = initial_vx                            # 横方向の速度
        self.facing_left = True                         # 左向きかどうか
        self.frame_counter = 0                          # フレームカウンター
        self.stomped = False                            # 踏まれたかどうか
        self.stomped_timer = 0                          # 踏まれた後の経過フレーム
        self.safe_timer = 0                             # 衝突無効化の安全時間
        self.disappear_delay = self.gc.disappear_delay  # 踏まれた後消えるまでの時間（フレーム数）
        self.player = player                            # プレイヤーの参照を保持

        # 画像をリストで保持
        self.imgs = images
        self.image = self.imgs[0]
        self.rect = pg.Rect(initial_x, initial_y, 20, 20)

    def is_stomped(self):
        return self.stomped

    def stomp(self):
        self.stomped = True
        self.image = self.imgs[2]

    def reverse_direction(self):
        self.vx *= -1

    def check_status(self):
        return self.player.status in {
            ps.GROWING,
            ps.SHRINKING,
            ps.DYING,
            ps.GAME_OVER
            }

    def check_screen_boundaries(self):
        if self.rect.x <= 0 or self.rect.x >= self.dc.width - self.rect.width:
            self.reverse_direction()

    def update_common(self):
        # 踏まれていない場合は横移動
        if not self.is_stomped():
            # X方向に移動
            self.rect.x += self.vx

        self.frame_counter += 1
        # 画面端にきたら反転
        self.check_screen_boundaries()
