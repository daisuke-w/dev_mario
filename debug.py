import logging
import time

# ログ設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# ログ出力の間隔制御用
_last_log_times = {}

def debug_log(key, message, interval=1):
    '''
    指定した間隔でログを出力するデバッグ関数
    以下のような記述をログを出力したいか所に記述して使用する
    debug_log("log", f"Ground: {self.__on_ground}, Block: {self.__on_block}, vy: {self.__vy}", interval=2)

    Args:
        key (str): ログの識別子
        message (str): 出力するログメッセージ
        interval (float): ログを出力する最小間隔（秒）
    '''
    current_time = time.time()
    last_time = _last_log_times.get(key, 0)

    if current_time - last_time >= interval:
        logging.info(message)
        _last_log_times[key] = current_time
