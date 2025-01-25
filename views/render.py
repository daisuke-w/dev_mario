import pygame as pg


def render_background(win, color):
    ''' 背景を塗りつぶす '''
    win.fill(color)

def render_display(group, win, camera):
    ''' 全てのスプライトを描画し画面を更新 '''
    for sprite in group:
        win.blit(sprite.image, camera.apply(sprite))
    pg.display.flip()
