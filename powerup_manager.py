import time
import random
from powerups import PowerUps
import pygame as pg
from uuid import uuid4

class PowerUpManager:

  def __init__(self, spawn_interval, max_spawns, screen):
    self.spawn_interval = spawn_interval
    self.max_spawns = max_spawns

    self.last_spawn_time = spawn_interval - 1

    self.active_powerups = {}
    self.powerup_types = [PowerUps.STRIKER_SPEED_BOOST, PowerUps.STRIKER_SMASH_HIT, PowerUps.STRIKER_LENGTH_UP, PowerUps.ENEMY_STRIKER_LENGTH_DOWN]

    self.screen = screen

    self.paused_start = None
    self.paused_duration = 0
    self.was_paused = False

  def paused(self):
    if self.paused_start:
      return

    self.paused_start = time.time()

  def resumed(self):
    if not self.paused_start:
      return

    self.paused_duration = time.time() - self.paused_start
    self.paused_start = None

    for powerup in self.active_powerups.values():
      powerup['power'].duration += self.paused_duration
      powerup['power'].timeout += self.paused_duration

  def spawn(self):
    if len(self.active_powerups) >= self.max_spawns:
      return

    now = time.time()
    if now - self.last_spawn_time >= self.spawn_interval:
      posx = random.randint(50, self.screen.get_width() - 50)
      posy = random.randint(150, self.screen.get_height() - 50)

      powerup_type = random.choice(self.powerup_types)
      powerup_id = uuid4()
      new_powerup = {
        'power': powerup_type.power(posx, posy, duration=powerup_type.duration, timeout=powerup_type.timeout, radius=powerup_type.radius, color=powerup_type.color, screen=self.screen),
        'affects_enemy': powerup_type.affects_enemy,
        'id': powerup_id
      }

      self.active_powerups[powerup_id] = new_powerup
      self.last_spawn_time = now

  def update(self, ball, last_striker, opposite_striker):
    disposed_id = None

    for powerup in self.active_powerups.values():
      powerup['power'].update()
      powerup['power'].show()

      if powerup['power'].died or powerup['power'].expired:
        if powerup['id'] in self.active_powerups:
          disposed_id = powerup['id']

      if not powerup['power'].acquired and pg.Rect.colliderect(ball.getRect(), powerup['power'].getRect()):
        powerup['power'].collected(opposite_striker if powerup['affects_enemy'] else last_striker)

    if disposed_id:
      del self.active_powerups[disposed_id]

  def reset(self):
    self.last_spawn_time = self.spawn_interval - 1
    self.active_powerups = {}
