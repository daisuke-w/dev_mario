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

    def apply(self, object):
        # 各オブジェクトをオフセット値分ずらして描画する
        return object.rect.move(-self.__offset_x, -self.__offset_y)

    def update(self, player):
        # プレイヤーがカメラの中心未満の場合はオフセット値は0
        self.__offset_x = max(0, player.rect.centerx - self.__width // 2)
