import pygame as pg
import random

class Ball:

  def __init__(self, posx, posy, radius, speed, screen):
    self.posx = posx
    self.posy = posy
    self.r = radius
    self.base_speed = speed
    self.speed = speed
    self.color = 'white'

    self.x_fac = random.choice([-1, 1])
    self.y_fac = random.uniform(-2, 2)

    self.sprite = pg.draw.circle(screen, self.color, (self.posx, self.posy), self.r)
    self.first_time = 1

    self.screen = screen

    self.smashed = False

  def show(self):
    self.sprite = pg.draw.circle(self.screen, self.color, (self.posx, self.posy), self.r)

  def update(self):
    self.posx += self.speed * self.x_fac
    self.posy += self.speed * self.y_fac

    if (self.posy - self.r) <= 10 or \
       (self.posy + self.r) >= self.screen.get_height() - 10:
      self.y_fac *= -1

    if (self.posx - self.r) <= 0:
      return 1

    elif (self.posx + self.r) >= self.screen.get_width():
      return -1

    else:
      return 0

  def reset(self):
    self.posx = self.screen.get_width() // 2
    self.posy = self.screen.get_height() // 2
    self.speed = self.base_speed
    self.y_fac = random.uniform(-2, 2)

  def hit(self, striker):
    offset = (self.posy - (striker.posy + striker.h / 2)) / (striker.h / 2)
    self.y_fac = offset
    self.x_fac *= -1
    self.speed += 0.1

    if self.smashed:
      self.speed /= 1.7
      self.smashed = False

    if striker.smash:
      self.smashed = True
      self.speed *= 1.7

      striker.smash = False
      striker.color = striker.base_color

  def getRect(self):
    return self.sprite
