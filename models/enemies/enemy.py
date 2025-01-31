import pygame as pg

from configs.config_manager import ConfigManager as cm


class Enemy(pg.sprite.Sprite):
    ''' 敵キャラクターの基底クラス '''
    def __init__(self, images, initial_x, initial_y, initial_vx, player):
        super().__init__()
        # 設定ファイル読み込み
        self.dis_conf = cm.get_display()
        self.game_conf = cm.get_game()

        self.vx = initial_vx                                   # 横方向の速度
        self.facing_left = True                                # 左向きかどうか
        self.frame_counter = 0                                 # フレームカウンター
        self.stomped = False                                   # 踏まれたかどうか
        self.stomped_timer = 0                                 # 踏まれた後の経過フレーム
        self.safe_timer = 0                                    # 衝突無効化の安全時間
        self.disappear_delay = self.game_conf.disappear_delay  # 踏まれた後消えるまでの時間（フレーム数）
        self.player = player                                   # プレイヤーの参照を保持

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
