import pygame as pg


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

    def __right(self):
        self.rect.x += 5
        self.__isLeft = False
        self.__walkIndex += 1

    def __left(self):
        self.rect.x -= 5
        self.__isLeft = True
        self.__walkIndex += 1

    def __jump(self):
        if self.__on_ground:
            # ジャンプ速度をリセット
            self.__vy = self.__jump_speed
            self.__on_ground = False

    def set_game_over(self):
        self.__game_over = True
        self.image = self.__imgs[4]

    def is_falling(self):
        return self.__vy > 0

    def update(self):
        # Game Over時は動かない
        if self.__game_over:
            return

        # キーボードの状態を取得
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.__right()
        if keys[pg.K_LEFT]:
            self.__left()
        if keys[pg.K_SPACE]:
            self.__jump()

        # Y軸方向に移動
        if not self.__on_ground:
            self.rect.y += self.__vy
            self.__vy += 1
            if self.rect.y > 200:
                self.rect.y = 200
                self.__on_ground = True

        # ジャンプ中はジャンプ画像を表示、それ以外は歩行アニメーションを表示
        if not self.__on_ground:
            # ジャンプ中の画像
            self.image = pg.transform.flip(self.__imgs[3], self.__isLeft, False)
        else:
            # 歩行アニメーションの画像
            self.image = pg.transform.flip(
                self.__imgs[self.WALK_ANIME_INDEX[self.__walkIndex % 9]],
                self.__isLeft,
                False)
