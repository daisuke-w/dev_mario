import pygame as pg


def render_background(win, color):
    ''' 背景を塗りつぶす '''
    win.fill(color)

def render_display(group, win):
    ''' 全てのスプライトを描画し画面を更新 '''
    group.draw(win)
    pg.display.flip()
