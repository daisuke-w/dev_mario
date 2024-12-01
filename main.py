import sys
import pygame as pg

# 画面サイズ
WIDTH = 320
HEIGHT = 270

# タイル数
TILE_X = 16
TILE_Y = 14

class Mario(pg.sprite.Sprite):
    ''' マリオのクラス '''
    WALK_ANIME_INDEX = [0, 0, 0, 1, 1, 1, 2, 2, 2]
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

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

        # マリオ画像読み込み
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


class Kuriboh(pg.sprite.Sprite):
    ''' クリボーのクラス '''
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        # 画像をリストで保持
        self.__imgs = [
            pg.image.load('images/kuriboh_001.png'),
            pg.image.load('images/kuriboh_002.png'),
            pg.image.load('images/kuriboh_003.png')
        ]

        self.image = self.__imgs[0]
        self.rect = pg.Rect(180, 200, 20, 20)

        # 横方向の速度
        self.__vx = 2
        # フレームカウンター
        self.__frame_counter = 0
        # 踏まれたかどうか
        self.__stomped = False
        # 踏まれた後の経過フレーム
        self.__stomped_timer = 0
        # 踏まれた後消えるまでの時間（フレーム数）
        self.__disappear_delay = 15

    def is_stomped(self):
        return self.__stomped

    def stomp(self):
        self.__stomped = True
        self.image = self.__imgs[2]

    def reverse_direction(self):
        self.__vx *= -1

    def update(self):
        # 踏まれた後の処理
        if self.__stomped:
            self.__stomped_timer += 1
            if self.__stomped_timer >= self.__disappear_delay:
                # 一定時間経過後に削除
                self.kill()
            return

        # フレームカウンターを増加
        self.__frame_counter += 1

        # 一定フレームごとに画像を切り替える
        if self.__frame_counter % 10 == 0:
            self.image = self.__imgs[self.__frame_counter // 10 % 2]

        # X方向に移動
        self.rect.x += self.__vx

        # 画面端で反転
        if self.rect.x <= 0 or self.rect.x >= WIDTH - self.rect.width:
            # 方向を反転
            self.__vx = -self.__vx


class Nokonoko(pg.sprite.Sprite):
    ''' ノコノコのクラス '''
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        # 画像をリストで保持
        self.__imgs = [
            pg.image.load('images/nokonoko_001.png'),
            pg.image.load('images/nokonoko_002.png'),
            pg.image.load('images/nokonoko_003.png')
        ]

        self.image = self.__imgs[0]
        self.rect = pg.Rect(200, 200, 20, 20)

        # 左右フラグ
        self.__isLeft = True
        # 横方向の速度
        self.__vx = -2
        # フレームカウンター
        self.__frame_counter = 0
        # 踏まれたかどうか
        self.__stomped = False

    def is_stomped(self):
        return self.__stomped

    def stomp(self):
        self.__stomped = True
        self.image = self.__imgs[2]

    def reverse_direction(self):
        """ 進行方向と画像の向きを反転する"""
        self.__vx *= -1
        # 左右フラグを反転
        self.__isLeft = not self.__isLeft
        # 現在の画像フレームに基づいて画像を更新
        current_img = self.__frame_counter // 10 % 2
        self.image = pg.transform.flip(self.__imgs[current_img], not self.__isLeft, False)

    def update(self):
        # 踏まれたら動かない
        if self.__stomped:
            return

        # フレームカウンターを増加
        self.__frame_counter += 1
        # X方向に移動
        self.rect.x += self.__vx

        # 画面端で反転
        if self.rect.x <= 0 or self.rect.x >= WIDTH - self.rect.width:
            # 方向を反転
            self.__vx = -self.__vx
            self.__isLeft = not self.__isLeft

            # 即座に反転した画像を設定
            current_img = self.__frame_counter // 10 % 2
            self.image = pg.transform.flip(self.__imgs[current_img], not self.__isLeft, False)

            # 反転後すぐに処理を終了する
            return

        # 一定フレームごとにアニメーション
        if self.__frame_counter % 10 == 0:
            current_img = self.__frame_counter // 10 % 2
            self.image = pg.transform.flip(self.__imgs[current_img], not self.__isLeft, False)


def main():
    ''' メイン関数 '''
    # Pygameの初期化
    pg.init()
    # イベント実行フラグ
    running = True

    # 画面作成
    win = pg.display.set_mode((WIDTH, HEIGHT))

    # クロックを生成
    clock = pg.time.Clock()

    # スプライトグループを定義
    group = pg.sprite.RenderUpdates()
    # 敵キャラクターグループを定義
    enemies = pg.sprite.Group()
    # 各スプライトを構築してグループに追加
    mario = Mario()
    kuriboh = Kuriboh()
    nokonoko = Nokonoko()
    group.add(mario, kuriboh, nokonoko)
    enemies.add(kuriboh, nokonoko)

    # イベントループ
    while running:
        # イベント処理
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

        # 背景を水色に塗りつぶす
        win.fill((135, 206, 235))

        # クリボー衝突判定
        if pg.sprite.collide_rect(mario, kuriboh):
            if not kuriboh.is_stomped():
                # マリオの底辺がクリボーの上辺に触れているかを確認
                if mario.is_falling() and mario.rect.bottom <= kuriboh.rect.top + 5:
                    kuriboh.stomp()
                else:
                    mario.set_game_over()

        # ノコノコ衝突判定
        if pg.sprite.collide_rect(mario, nokonoko):
            if not nokonoko.is_stomped():
                # マリオの底辺がノコノコの上辺に触れているかを確認
                if mario.is_falling() and mario.rect.bottom <= nokonoko.rect.top + 5:
                    nokonoko.stomp()
                else:
                    mario.set_game_over()

        # 敵キャラクター同士の衝突判定
        # 判定したペアを管理
        processed = set()
        for enemy in enemies:
            collided = pg.sprite.spritecollide(enemy, enemies, False)
            for other in collided:
                # 同じ衝突ペアが複数回処理されるのを回避（A が B と衝突）（B が A と衝突）
                if other != enemy and (enemy, other) not in processed and (other, enemy) not in processed:
                    if isinstance(enemy, (Kuriboh, Nokonoko)) and isinstance(other, (Kuriboh, Nokonoko)):
                        enemy.reverse_direction()
                        other.reverse_direction()
                        # 衝突判定したペアを記録
                        processed.add((enemy, other))

        # グループの更新
        group.update()

        # グループの描画
        group.draw(win)

        # 画面を更新
        pg.display.flip()

        # フレームレートを設定(1秒間に30フレーム)
        clock.tick(30)

    pg.quit()
    sys.exit()


if __name__ == '__main__':
    main()
