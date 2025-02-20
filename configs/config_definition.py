from pydantic import BaseModel


class DisplayConfig(BaseModel):
    width: int
    height: int
    tile_x: int
    tile_y: int
    tile_size: int
    background: list[int]

class GameConfig(BaseModel):
    frame_rate: int
    hatena_interval: int
    coin_interval: int
    invincibility_duration: int
    gravity: int
    walk_speed: int
    jump_speed: int
    shell_speed: int
    dead_jump_height: int
    dead_anime_counter: int
    disappear_delay: int
    stomped_timer: int
    safe_timer: int
    appear_distance: int

class BlockTypesConfig(BaseModel):
    ground: int
    wall: int
    block: int
    released: int
    hatena_kinoko: int
    hatena_coin: int
    block_coin: int

class BlockFragmentsConfig(BaseModel):
    horizontal_speed_range: list[int]
    vertical_speed_range: list[int]

class BlockConfig(BaseModel):
    types: BlockTypesConfig
    block_fragments: BlockFragmentsConfig

class AllConfig(BaseModel):
    display: DisplayConfig
    game: GameConfig
    block: BlockConfig
