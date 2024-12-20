import pygame as pg
from utils.debug import debug_log


class Mario(pg.sprite.Sprite):
    ''' マリオのクラス '''
    WALK_ANIME_INDEX = [0, 0, 0, 1, 1, 1, 2, 2, 2]

    def __init__(self):
        super().__init__()
        # 左右の向きフラグ
        self.__isLeft = False
        # 歩くインデックス
        self.__walkIndex = 0
        # 初期ジャンプ速度
        self.__jump_speed = -10
        # Y軸方向移動距離
        self.__vy = 0
        # マリオが地面にいるかどうか
        self.__on_ground = True
        # マリオがブロックの上にいるかどうか
        self.__on_block = False
        # Game Overフラグ
        self.__game_over = False

        # 画像をリストで保持
        self.__imgs = [
            pg.image.load('images/mario_001.png'),
            pg.image.load('images/mario_002.png'),
            pg.image.load('images/mario_003.png'),
            pg.image.load('images/mario_004.png'),
            pg.image.load('images/mario_005.png')
        ]

        self.image = self.__imgs[0]
        self.rect = pg.Rect(50, 200, 20, 20)

    @property
    def vy(self):
        return self.__vy

    @vy.setter
    def vy(self, value):
        self.__vy = value

    @property
    def on_block(self):
        return self.__on_block

    def __right(self):
        self.rect.x += 5
        self.__isLeft = False
        self.__walkIndex += 1

    def __left(self):
        self.rect.x -= 5
        self.__isLeft = True
        self.__walkIndex += 1

    def __jump(self):
        if self.__on_ground or self.__on_block:
            # ジャンプ速度をリセット
            self.__vy = self.__jump_speed
            self.__on_ground = False
            self.leave_block()

    def __handle_horizontal_movement(self, keys):
        if keys[pg.K_RIGHT]:
            self.__right()
        if keys[pg.K_LEFT]:
            self.__left()

    def __handle_jump(self, keys):
        if keys[pg.K_SPACE]:
            self.__jump()

    def __update_vertical_position(self):
        if not self.__on_ground:
            self.rect.y += self.__vy
            self.__vy += 1
            # 地面に着地した場合
            if self.rect.y > 200:
                self.__vy = 0
                self.rect.y = 200
                self.__on_ground = True
                self.leave_block()
            # ブロックに着地した場合
            elif self.__on_block:
                self.__vy = 0
                # ブロックの上にいるが、地面ではない
                self.__on_ground = False
            else:
                self.leave_block()

    def __change_image(self):
        # ジャンプ中はジャンプ画像を表示、それ以外は歩行アニメーションを表示
        if not self.__on_ground and not self.__on_block:
            # ジャンプ中の画像
            self.image = pg.transform.flip(self.__imgs[3], self.__isLeft, False)
        else:
            # 歩行アニメーションの画像
            self.image = pg.transform.flip(
                self.__imgs[self.WALK_ANIME_INDEX[self.__walkIndex % 9]],
                self.__isLeft,
                False)

    def set_game_over(self):
        self.__game_over = True
        self.image = self.__imgs[4]

    def is_falling(self):
        return self.__vy > 0

    def land_on_block(self, top):
        # ブロックの上に乗る
        self.rect.bottom = top
        # 垂直速度をリセット
        self.__vy = 0
        self.__on_ground = False
        self.__on_block = True

    def leave_block(self):
        # ブロックから離れる
        self.__on_block = False

    def update(self, dt=0):
        # Game Over時は動かない
        if self.__game_over:
            return

        # キーボードの状態を取得
        keys = pg.key.get_pressed()
        self.__handle_horizontal_movement(keys)
        self.__handle_jump(keys)

        # Y軸方向に移動
        self.__update_vertical_position()

        # 動作に応じた画像に変換
        self.__change_image()
