import time
import pygame as pg
from enum import Enum

class PowerUp:

  def __init__(self, posx, posy, duration, timeout, radius, color, screen):
    self.posx = posx
    self.posy = posy

    self.duration = duration
    self.expired = False
    self.reverted = False

    self.timeout = timeout

    self.r = radius
    self.color = color

    self.born = False
    self.died = False

    self.acquired = False
    self.target = None

    self.sprite = pg.draw.circle(screen, self.color, (self.posx, self.posy), self.r)
    self.screen = screen

  def show(self):
    if self.acquired:
      self.sprite = None
      return

    if not self.born:
      self.birth = time.time()
      self.born = True

    self.sprite = pg.draw.circle(self.screen, self.color, (self.posx, self.posy), self.r)

  def collected(self, target):
    self.target = target
    self.target.color = self.color

    self.acquired = True
    self.effect_start = time.time()

  def update(self):
    if not self.acquired and self.born:
      age = time.time() - self.birth

      if age >= self.timeout:
        self.died = True

    elif self.acquired:
      effect_age = time.time() - self.effect_start

      if effect_age >= self.duration:
        self.target.color = self.target.base_color
        self.expired = True

  def getRect(self):
    return self.sprite

class StrikerSpeedBoost(PowerUp):

  def __init__(self, posx, posy, duration, timeout, radius, color, screen):
    super().__init__(posx, posy, duration, timeout, radius, color, screen)

  def collected(self, target):
    super().collected(target)
    self.target.speed *= 1.7

  def update(self):
    super().update()
    if self.expired and not self.reverted:
      self.target.speed /= 1.7
      self.reverted = True

class StrikerSmashHit(PowerUp):

  def __init__(self, posx, posy, duration, timeout, radius, color, screen):
    super().__init__(posx, posy, duration, timeout, radius, color, screen)

  def collected(self, target):
    super().collected(target)
    self.target.smash = True

  def update(self):
    super().update()
    if self.expired and not self.reverted:
      self.target.smash = False
      self.reverted = True

class StrikerLengthUp(PowerUp):

  def __init__(self, posx, posy, duration, timeout, radius, color, screen):
    super().__init__(posx, posy, duration, timeout, radius, color, screen)

  def collected(self, target):
    super().collected(target)
    self.target.h *= 2

  def update(self):
    super().update()
    if self.expired and not self.reverted:
      self.target.h /= 2
      self.reverted = True

class EnemyStrikerLengthDown(PowerUp):

  def __init__(self, posx, posy, duration, timeout, radius, color, screen):
    super().__init__(posx, posy, duration, timeout, radius, color, screen)

  def collected(self, target):
    super().collected(target)
    self.target.h /= 2

  def update(self):
    super().update()
    if self.expired and not self.reverted:
      self.target.h *= 2
      self.reverted = True

class EnemyInvertControls(PowerUp):

  def __init__(self, posx, posy, duration, timeout, radius, color, screen):
    super().__init__(posx, posy, duration, timeout, radius, color, screen)

  def collected(self, target):
    super().collected(target)
    [self.target.controls[0], self.target.controls[1]] = [self.target.controls[1], self.target.controls[0]]

  def update(self):
    super().update()
    if self.expired and not self.reverted:
      [self.target.controls[1], self.target.controls[0]] = [self.target.controls[0], self.target.controls[1]]
      self.reverted = True

class EnemySlowDown(PowerUp):

  def __init__(self, posx, posy, duration, timeout, radius, color, screen):
    super().__init__(posx, posy, duration, timeout, radius, color, screen)

  def collected(self, target):
    super().collected(target)
    self.target.speed /= 1.5

  def update(self):
    super().update()
    if self.expired and not self.reverted:
      self.target.speed *= 1.5
      self.reverted = True

class PowerUps(Enum):

  STRIKER_SPEED_BOOST = (StrikerSpeedBoost, 5, 10, 15, 'blue', False)
  STRIKER_SMASH_HIT = (StrikerSmashHit, 5, 5, 12, 'green', False)
  STRIKER_LENGTH_UP = (StrikerLengthUp, 7, 7, 15, 'purple', False)
  ENEMY_STRIKER_LENGTH_DOWN = (EnemyStrikerLengthDown, 7, 7, 15, 'orange', True)
  ENEMY_INVERT_CONTROLS = (EnemyInvertControls, 5, 5, 15, 'red', True)
  ENEMY_SLOW_DOWN = (EnemySlowDown, 5, 10, 15, 'cyan', True)

  def __init__(self, power, duration, timeout, radius, color, affects_enemy):
    self.power = power
    self.duration = duration
    self.timeout = timeout
    self.radius = radius
    self.color = color
    self.affects_enemy = affects_enemy
