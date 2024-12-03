import pygame as pg


class Block(pg.sprite.Sprite):
    # クラス変数として画像を保持
    block_image = None

    def __init__(self, x, y):
        super().__init__()
        # ブロックの画像を設定
        self.image = Block.block_image
        # 位置を設定
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    @classmethod
    def load_image(cls, tile_size):
        ''' ブロック画像を読み込んでクラス変数に設定 '''
        image = pg.image.load('images/block_001.png').convert_alpha()
        cls.block_image = pg.transform.scale(image, (tile_size, tile_size))

    @classmethod
    def create_blocks(cls, block_map, tile_size):
        ''' ブロックを配置するクラスメソッド '''
        blocks = pg.sprite.Group()
        for y, row in enumerate(block_map):
            for x, cell in enumerate(row):
                if cell == 1:
                    # 新しいブロックを作成してグループに追加
                    block = cls(x * tile_size, y * tile_size)
                    blocks.add(block)
        return blocks
