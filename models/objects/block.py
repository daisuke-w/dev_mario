import pygame as pg

from models.objects.items.kinoko import Kinoko

class Block(pg.sprite.Sprite):
    # クラス変数として画像を保持
    __imgs = {}
    __animated_imgs = {}

    def __init__(self, x, y, cell_type, item_type=None):
        super().__init__()
        self.cell_type = cell_type
        # アイテムの種類
        self.item_type = item_type
        # アイテムがすでに生成されたかどうか
        self.item_released = False

        # セルの種類に応じて画像を設定
        if cell_type in Block.__animated_imgs:
            self.frames = Block.__animated_imgs[cell_type]
            self.image = self.frames[0]
            # アニメーションフレーム
            self.current_frame = 0
            # アニメーションのタイマー
            self.animation_timer = 0
            # アニメーションフレームの切り替え間隔（ミリ秒）
            self.animation_interval = 200
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
                item = Kinoko(self.rect.centerx, self.rect.top - 16, player)
                items.add(item)
                group.add(items, layer=2)

            self.item_released = True

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
            1: load_and_scale('images/wall_001.png'),
            2: load_and_scale('images/block_001.png')
        }
        cls.__animated_imgs = {
            3: [load_and_scale(f'images/hatena_{i:03d}.png') for i in range(1, 4)]
        }

    @classmethod
    def create_blocks(cls, block_map, tile_size):
        ''' ブロックを配置するクラスメソッド '''
        blocks = pg.sprite.Group()
        for y, row in enumerate(block_map):
            for x, cell in enumerate(row):
                # 画像が定義されているセル値のみ追加
                if cell in cls.__imgs or cell in cls.__animated_imgs:
                    if cell == 3:
                        block = cls(x * tile_size, y * tile_size, cell, item_type='kinoko')
                    else:
                        block = cls(x * tile_size, y * tile_size, cell)
                    blocks.add(block)
        return blocks
