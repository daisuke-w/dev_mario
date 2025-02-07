class Camera:
    '''
        カメラのクラス
        オフセットを利用して描画位置を調整する
    '''
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__offset_x = 0
        self.__offset_y = 0
        self.__max_offset_x = 0

    @property
    def offset_x(self):
        return self.__offset_x
    
    def get_viewport_bounds(self):
        # 画面の左端と右端を取得
        return self.__offset_x, self.__offset_x + self.__width

    def apply(self, object):
        # 各オブジェクトをオフセット値分ずらして描画する
        return object.rect.move(-self.__offset_x, -self.__offset_y)

    def update(self, player):
        # プレイヤーの中心位置が画面の中央より右ならオフセットを計算
        new_offset_x = player.rect.centerx - self.__width // 2

        # オフセット値を現在到達した最右端と比較し、最大値を更新
        self.__max_offset_x = max(self.__max_offset_x, new_offset_x)

        # 現在のオフセットを最大値（右方向）に制限する
        self.__offset_x = max(0, self.__max_offset_x)
