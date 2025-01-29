import pygame as pg

from models.player.mario import Mario
from models.enemies.kuriboh import Kuriboh
from models.enemies.nokonoko import Nokonoko
from models.objects.block import Block
from views.camera import Camera


class GameInit:
    def __init__(self, width, height, tile_size, block_map):
        self.__width = width
        self.__height = height
        self.__tile_size = tile_size
        self.__block_map = block_map
        self.__camera = None
        self.__win = None
        self.__clock = None

    def init_screen(self):
        ''' 画面、カメラ、クロックを初期化 '''
        self.__win = pg.display.set_mode((self.__width, self.__height))
        self.__clock = pg.time.Clock()
        self.__camera = Camera(self.__width, self.__height)

    def init_player(self):
        ''' プレイヤーを生成 '''
        player = Mario()
        return player

    def init_enemies(self, player):
        ''' 敵キャラクターを生成してグループに追加 '''
        kuriboh = Kuriboh(180, 200, 2, player)
        nokonoko = Nokonoko(200, 200, -2, player)
        enemies = pg.sprite.Group(kuriboh, nokonoko)

        return enemies

    def init_blocks(self):
        ''' ブロックを生成してグループに追加 '''
        Block.load_images(self.__tile_size)
        blocks = Block.create_blocks(self.__block_map, self.__tile_size)

        return blocks

    def init_game(self):
        # 画面とカメラとクロックの初期化
        self.init_screen()
        # プレイヤーの生成
        player = self.init_player()
        # 敵キャラクターの生成
        enemies = self.init_enemies(player)
        # ブロックの生成
        blocks = self.init_blocks()
        # 空のアイテムグループを定義
        items = pg.sprite.Group()

        return player, enemies, blocks, items

    def execute(self):
        player, enemies, blocks, items = self.init_game()
        group = pg.sprite.LayeredUpdates()
        group.add(player, layer=3)
        group.add(enemies, layer=2)
        group.add(blocks, layer=1)

        return (
            self.__win,
            self.__clock,
            self.__camera,
            group,
            player,
            enemies,
            blocks,
            items
        )
