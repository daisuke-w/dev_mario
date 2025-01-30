import pygame as pg
import random

from utils.debug import debug_log
from utils.settings import HEIGHT, GROUND, WALL, BLOCK, HATENA_BLOCK, HATENA_BLOCK_RELEASED, ANIMATION_INTERVAL, GRAVITY, HORIZONTAL_SPEED_RANGE, VERTICAL_SPEED_RANGE
from models.objects.items.kinoko import Kinoko

class Block(pg.sprite.Sprite):
    # クラス変数として画像を保持
    __imgs = {}
    __animated_imgs = {}
    __fragment_img = None
    __block_dict = {}

    def __init__(self, x, y, cell_type, item_type=None):
        super().__init__()
        self.cell_type = cell_type
        # アイテムの種類
        self.item_type = item_type
        # アイテムがすでに生成されたかどうか
        self.item_released = False
        # ブロックが破壊されたかどうか
        self.is_destroyed = False

        # セルの種類に応じて画像を設定
        if cell_type in Block.__animated_imgs:
            self.frames = Block.__animated_imgs[cell_type]
            self.image = self.frames[0]
            # アニメーションフレーム
            self.current_frame = 0
            # アニメーションのタイマー
            self.animation_timer = 0
            # アニメーションフレームの切り替え間隔（ミリ秒）
            self.animation_interval = ANIMATION_INTERVAL
        elif cell_type in Block.__imgs:
            self.image = Block.__imgs[cell_type]
        else:
            raise ValueError(f"Invalid cell type: {cell_type}")

        # 位置を設定
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def release_item(self, group, items, player):
        ''' ブロックを叩いてアイテムを生成 '''
        if not self.item_released and self.item_type is not None:
            if self.item_type == 'kinoko':
                item = Kinoko(self.rect.left, self.rect.top, player)
                item.initial_top = self.rect.top
                items.add(item)
                group.add(items, layer=0)

            self.item_released = True
            # ブロックのタイプを変更し画像をアイテムリリース後にする
            self.cell_type = HATENA_BLOCK_RELEASED
            self.image = Block.__imgs[HATENA_BLOCK_RELEASED]

    def break_into_fragments(self, group):
        # Blockを削除
        self.kill()
        self.is_destroyed = True
        fragments = pg.sprite.Group()
        for _ in range(4):
            vx = random.uniform(*HORIZONTAL_SPEED_RANGE)
            vy = random.uniform(*VERTICAL_SPEED_RANGE)
            fragment = Fragment(Block.__fragment_img, self.rect.centerx, self.rect.centery, vx, vy)
            fragments.add(fragment)
            group.add(fragments, layer=3)

        # 破片を削除
        fragments.empty()

    def update(self, dt=0):
        ''' アニメーションの更新処理 '''
        if self.cell_type in Block.__animated_imgs:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_interval:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]

    @classmethod
    def load_images(cls, tile_size):
        ''' ブロック画像を読み込んでクラス変数に設定 '''
        def load_and_scale(file_path):
            return pg.transform.scale(pg.image.load(file_path).convert_alpha(), (tile_size, tile_size))

        cls.__imgs = {
            GROUND: load_and_scale('images/ground_001.png'),
            WALL: load_and_scale('images/wall_001.png'),
            BLOCK: load_and_scale('images/block_001.png'),
            HATENA_BLOCK_RELEASED: load_and_scale('images/hatena_004.png')
        }
        cls.__animated_imgs = {
            HATENA_BLOCK: [load_and_scale(f'images/hatena_{i:03d}.png') for i in range(1, 4)]
        }
        cls.__fragment_img = load_and_scale('images/block_002.png')

    @classmethod
    def create_blocks(cls, block_map, tile_size):
        ''' ブロックを配置するクラスメソッド '''
        blocks = pg.sprite.Group()
        cls.__block_dict = {}
        for y, row in enumerate(block_map):
            for x, cell in enumerate(row):
                # 画像が定義されているセル値のみ追加
                if cell in cls.__imgs or cell in cls.__animated_imgs:
                    if cell == HATENA_BLOCK:
                        block = cls(x * tile_size, y * tile_size, cell, item_type='kinoko')
                    else:
                        block = cls(x * tile_size, y * tile_size, cell)
                    blocks.add(block)
                    cls.__block_dict[(x, y)] = block
        return blocks

    @classmethod
    def get_block(cls, x, y):
        ''' 指定した座標にあるブロックを取得 '''
        return cls.__block_dict.get((x, y))

class Fragment(pg.sprite.Sprite):
    def __init__(self, image, x, y, vx, vy):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = vx
        self.vy = vy
        self.gravity = GRAVITY

    def update(self, dt=0):
        self.vy += self.gravity
        self.rect.x += self.vx
        self.rect.y += self.vy

        # 画面の高さを超えたら削除
        if self.rect.top > HEIGHT:
            self.kill()
