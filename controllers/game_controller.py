import sys
import pygame as pg
import time

import utils.collision as col
import views.render as ren

from utils.debug import debug_log
from utils.settings import BACKGROUND, FRAME_RATE
from utils.status import PlayerStatus as ps
from controllers.game_init import game_init


class GameController():
    ''' Gameのイベントを管理するコントローラークラス '''
    def __init__(self):
        self.__init_game()

    def __init_game(self):
        # Pygameの初期化
        pg.init()
        # イベント実行フラグ
        self.__running = True
        # 各種オブジェクトを生成
        self.win, self.clock, self.mario, self.group, self.enemies, self.blocks, self.items = game_init()

    def __handle_events(self):
        # イベント処理
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.__running = False

    def __handle_collision(self):
        # 以下ステータス時は衝突判定をスキップ
        if self.mario.status in { ps.GROWING, ps.SHRINKING, ps.DYING, ps.GAME_OVER }:
            return

        # 判定したペアを管理する為のSET
        processed = set()
        for enemy in self.enemies:
            # プレイヤーと敵キャラクターの衝突判定
            col.player_enemy_collision(self.mario, enemy)

            # 敵キャラクター同士の衝突判定
            col.enemies_collision(processed, enemy, self.enemies)

            # 敵キャラクターと壁の衝突判定
            col.enemy_block_collision(enemy, self.blocks)

        # プレイヤーとブロックの衝突判定
        col.player_block_collision(self.group, self.mario, self.blocks, self.items)

        # アイテムとブロックの衝突判定
        col.item_block_collision(self.items, self.blocks)

        # プレイヤーとアイテムの衝突判定
        col.player_item_collision(self.mario, self.items)

    def reset_game(self):
        self.__init_game()

    def execute(self):
        while self.__running:
            # ゲーム画面が閉じられたかどうかを判定
            self.__handle_events()

            if self.mario.status == ps.GAME_OVER:
                time.sleep(2)
                self.reset_game()
                continue

            # 背景を水色に塗りつぶす
            ren.render_background(self.win, BACKGROUND)
            # 衝突判定
            self.__handle_collision()
            # フレームレートを設定
            dt = self.clock.tick(FRAME_RATE)
            # グループの更新
            self.group.update(dt)
            # 描画、画面更新
            ren.render_display(self.group, self.win)

        pg.quit()
        sys.exit()
