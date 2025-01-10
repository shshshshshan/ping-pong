import pygame as pg

class Striker:

  def __init__(self, posx, posy, w, h, speed, color, screen, controls):
    self.posx = posx
    self.posy = posy

    self.base_w = w
    self.base_h = h
    self.w = w
    self.h = h

    self.base_speed = speed
    self.speed = speed

    self.base_color = color
    self.color = color

    self.smash = False

    self.rect = pg.Rect(self.posx, self.posy, self.w, self.h)
    self.sprite = pg.draw.rect(screen, self.color, self.rect)
    self.screen = screen

    self.y_fac = 0
    self.controls = controls

  def keydown(self, key):
    if key not in self.controls:
      return

    if key == self.controls[0]:
      self.y_fac = -1

    elif key == self.controls[1]:
      self.y_fac = 1

  def keyup(self, key):
    if key not in self.controls:
      return

    if key in self.controls:
      self.y_fac = 0

  def show(self):
    self.sprite = pg.draw.rect(self.screen, self.color, self.rect)

  def update(self):
    self.posy += self.speed * self.y_fac

    if self.posy <= 0:
      self.posy = 0

    elif self.posy + self.h >= self.screen.get_height():
      self.posy = self.screen.get_height() - self.h

    self.rect = pg.Rect(self.posx, self.posy, self.w, self.h)

  def displayScore(self, text, score, x, y, font, color):
    text = font.render(f'{text} {score}', True, color)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    self.screen.blit(text, text_rect)

  def getRect(self):
    return self.rect

  def reset(self):
    self.color = self.base_color
    self.smash = False
    self.speed = self.base_speed
    self.w = self.base_w
    self.h = self.base_h
