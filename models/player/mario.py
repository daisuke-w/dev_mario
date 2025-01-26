import pygame as pg

import utils.collision as col

from utils.debug import debug_log
from utils.settings import HEIGHT, INVINCIBILITY_DURATION, TILE_SIZE, BLOCK_MAP
from utils.status import PlayerStatus as ps


class Mario(pg.sprite.Sprite):
    ''' マリオのクラス '''
    WALK_ANIME_INDEX = [0, 0, 0, 1, 1, 1, 2, 2, 2]

    def __init__(self):
        super().__init__()
        # 左右の向きフラグ
        self.__isLeft = False
        # 無敵状態のフラグ
        self.__is_invincible = False
        # 無敵状態のタイマー
        self.__invincibility_timer = 0
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
        # マリオの状態管理
        self.__status = ps.NORMAL
        # マリオGameOver時のアニメカウンター
        self.__dead_animeCounter = 0
        # 成長段階を管理
        self.__growth_stage = 0
        # フレームカウンタを増加
        self.__growth_frame_counter = 0
        # 縮小段階を管理
        self.__shrink_stage = 0
        # フレームカウンタを増加
        self.__shrink_frame_counter = 0

        # 画像をリストで保持
        self.__imgs = [
            pg.image.load('images/mario_001.png'),
            pg.image.load('images/mario_002.png'),
            pg.image.load('images/mario_003.png'),
            pg.image.load('images/mario_004.png'),
            pg.image.load('images/mario_005.png')
        ]

        self.__middle_imgs = [
            pg.image.load('images/middle_mario_001.png')
        ]

        self.__big_imgs = [
            pg.image.load('images/big_mario_001.png'),
            pg.image.load('images/big_mario_002.png'),
            pg.image.load('images/big_mario_003.png'),
            pg.image.load('images/big_mario_004.png'),
            pg.image.load('images/big_mario_005.png'),
            pg.image.load('images/big_mario_006.png')
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
    def on_ground(self):
        return self.__on_ground
    
    @on_ground.setter
    def on_ground(self, value):
        self.__on_ground = value

    @property
    def on_block(self):
        return self.__on_block
    
    @on_block.setter
    def on_block(self, value):
        self.__on_block = value
    
    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def is_invincible(self):
        return self.__is_invincible
    
    @is_invincible.setter
    def is_invincible(self, value):
        self.__is_invincible = value

    def __right(self):
        self.rect.x += 5
        self.__isLeft = False
        self.__walkIndex += 1

    def __left(self):
        self.rect.x -= 5
        self.__isLeft = True
        self.__walkIndex += 1

    def __jump(self):
        if self.on_ground or self.on_block:
            # ジャンプ速度をリセット
            self.vy = self.__jump_speed
            self.on_ground = False
            self.leave_block()

    def __dying(self):
        # Game Overになったら飛び上がる
        if self.__dead_animeCounter == 0:
            self.vy = -12
        
        if self.__dead_animeCounter > 12:
            self.__apply_gravity()

        # ゲーム画面を超えたら終了
        if self.rect.y > HEIGHT:
            self.status = ps.GAME_OVER
            return

        self.__dead_animeCounter +=1

    def __apply_gravity(self):
        self.rect.y += self.vy
        self.vy += 1

    def __handle_horizontal_movement(self, keys):
        if keys[pg.K_RIGHT]:
            self.__right()
        if keys[pg.K_LEFT]:
            self.__left()

    def __handle_jump(self, keys):
        if keys[pg.K_SPACE]:
            self.__jump()

    def __handle_growth(self):
            ''' 成長アニメーションをハンドリング '''
            growth_sequence = [
                self.__imgs[0],
                self.__middle_imgs[0],
                self.__imgs[0],
                self.__middle_imgs[0],
                self.__big_imgs[0],
                self.__imgs[0],
                self.__big_imgs[4],
                self.__big_imgs[0]
            ]
            self.__growth_frame_counter += 1
            # 4フレームごとに画像を切り替え
            if self.__growth_frame_counter >= 4:
                if self.__growth_stage < len(growth_sequence):
                    self.image = growth_sequence[self.__growth_stage]
                    self.__growth_stage += 1
                    self.__growth_frame_counter = 0
                    # 大きくなった時点でサイズ変更
                    if self.__growth_stage == 1:
                        self.__resize_image(20, 32)
                        # 大きくなったサイズ分引いて調整
                        self.rect.bottom -= 12
                else:
                    self.status = ps.BIG
                    self.image = self.__big_imgs[0]
                    self.__growth_frame_counter = 0

    def __handle_shrink(self):
        ''' 縮小アニメーションをハンドリング '''
        shrink_sequence = [
            self.__big_imgs[0],
            self.__middle_imgs[0],
            self.__big_imgs[0],
            self.__middle_imgs[0],
            self.__imgs[0],
            self.__big_imgs[0],
            self.__imgs[0]
        ]
        self.__shrink_frame_counter += 1
        # 2フレームごとに画像を切り替え
        if self.__shrink_frame_counter >= 2:
            if self.__shrink_stage < len(shrink_sequence):
                self.image = shrink_sequence[self.__shrink_stage]
                self.__shrink_stage += 1
                self.__shrink_frame_counter = 0
                # 小さくなった時点でサイズ変更
                if self.__shrink_stage == 6:
                    self.__resize_image(20, 20)
                    # 大きくなっていた分足して調整
                    self.rect.bottom += 12
            else:
                self.status = ps.NORMAL
                self.image = self.__imgs[0]
                self.__shrink_frame_counter = 0

    def __update_vertical_position(self, value=0):
        result = col.is_touching_block_below(self.rect, TILE_SIZE, BLOCK_MAP)
        if not result:
            self.on_ground = False
        if not self.on_ground:
            self.__apply_gravity()
            # 画面外に落下した場合
            if not result:
                if self.rect.y > HEIGHT:
                    self.__dying()
                return
            # 地面に着地した場合
            elif self.rect.y > 200 - value:
                self.vy = 0
                self.rect.y = 200 - value
                self.on_ground = True
                self.leave_block()
            # ブロックに着地した場合
            elif self.on_block:
                self.vy = 0
                # ブロックの上にいるが、地面ではない
                self.on_ground = False
            else:
                self.leave_block()

    def __resize_image(self, width, height):
        self.rect.width = width
        self.rect.height = height

    def __opacity_image(self):
        if self.is_invincible:
            new_image = self.image.copy()
            new_image.set_alpha(128)
            self.image = new_image

    def __change_image(self):
        if self.is_big():
            # ジャンプ中はジャンプ画像を表示、それ以外は歩行アニメーションを表示
            if not self.on_ground and not self.on_block:
                # ジャンプ中の画像
                self.image = pg.transform.flip(self.__big_imgs[3], self.__isLeft, False)
            else:
                # 歩行アニメーションの画像
                self.image = pg.transform.flip(
                    self.__big_imgs[self.WALK_ANIME_INDEX[self.__walkIndex % 9]],
                    self.__isLeft,
                    False)
        else:
            # ジャンプ中はジャンプ画像を表示、それ以外は歩行アニメーションを表示
            if not self.on_ground and not self.on_block:
                # ジャンプ中の画像
                self.image = pg.transform.flip(self.__imgs[3], self.__isLeft, False)
            else:
                # 歩行アニメーションの画像
                self.image = pg.transform.flip(
                    self.__imgs[self.WALK_ANIME_INDEX[self.__walkIndex % 9]],
                    self.__isLeft,
                    False)

    def set_game_over(self):
        self.status = ps.DYING
        self.image = self.__imgs[4]

    def is_game_over(self):
        return self.status == ps.GAME_OVER

    def is_dying(self):
        return self.status == ps.DYING

    def is_big(self):
        return self.status == ps.BIG

    def is_growing(self):
        return self.status == ps.GROWING

    def is_shrink(self):
        return self.status == ps.SHRINKING

    def is_falling(self):
        return self.vy > 0

    def land_on_block(self, top):
        # ブロックの上に乗る
        self.rect.bottom = top
        # 垂直速度をリセット
        self.vy = 0
        self.on_ground = False
        self.on_block = True

    def leave_block(self):
        # ブロックから離れる
        self.on_block = False

    def grow(self):
        if self.status != ps.GROWING:
            self.status = ps.GROWING
            self.__growth_stage = 0

    def shrink(self):
        if self.status != ps.SHRINKING:
            self.status = ps.SHRINKING
            self.__shrink_stage = 0

    def update(self, dt=0):
        # 無敵状態の処理
        if self.is_invincible:
            # 縮小中に透明化させるため呼び出し
            self.__opacity_image()
            self.__invincibility_timer += dt
            if self.__invincibility_timer >= INVINCIBILITY_DURATION:
                self.is_invincible = False
                self.__invincibility_timer = 0

        # Game Over時は動かない
        if self.is_game_over():
            return

        # Game Over中にアニメーションを実行
        if self.is_dying():
            self.__dying()
            return

        if self.is_growing():
            self.__handle_growth()
            return

        if self.is_shrink():
            self.__handle_shrink()
            return

        # キーボードの状態を取得
        keys = pg.key.get_pressed()
        self.__handle_horizontal_movement(keys)
        self.__handle_jump(keys)

        # Y軸方向に移動
        if self.is_big():
            self.__update_vertical_position(12)
        else:
            self.__update_vertical_position()

        # 動作に応じた画像に変換
        self.__change_image()

        if self.is_invincible:
            # 縮小が終わり、インターバル期間中も透明化させるため呼び出し
            self.__opacity_image()
