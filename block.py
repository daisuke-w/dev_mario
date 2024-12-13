import pygame as pg


class Block(pg.sprite.Sprite):
    # クラス変数として画像を保持
    __imgs = {}

    def __init__(self, x, y, cell_type):
        super().__init__()
        # セルの種類に応じて画像を設定
        self.image = Block.__imgs.get(cell_type)
        if self.image is None:
            raise ValueError(f"Invalid cell type: {cell_type}")
        # 位置を設定
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    @classmethod
    def load_images(cls, tile_size):
        ''' ブロック画像を読み込んでクラス変数に設定 '''
        cls.__imgs = {
            1: pg.transform.scale(pg.image.load('images/wall_001.png').convert_alpha(), (tile_size, tile_size)),
            2: pg.transform.scale(pg.image.load('images/block_001.png').convert_alpha(), (tile_size, tile_size)),
            3: pg.transform.scale(pg.image.load('images/hatena_001.png').convert_alpha(), (tile_size, tile_size))
        }

    @classmethod
    def create_blocks(cls, block_map, tile_size):
        ''' ブロックを配置するクラスメソッド '''
        blocks = pg.sprite.Group()
        for y, row in enumerate(block_map):
            for x, cell in enumerate(row):
                if cell in cls.__imgs:  # 画像が定義されているセル値のみ追加
                    block = cls(x * tile_size, y * tile_size, cell)
                    blocks.add(block)
        return blocks
