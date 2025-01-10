import pygame as pg
from striker import Striker
from ball import Ball
from powerup_manager import PowerUpManager

## --- Setup --- ##
pg.init()

w, h = 1020, 920

font20 = pg.font.Font('freesansbold.ttf', 20)

screen = pg.display.set_mode((w, h))
pg.display.set_caption('Pong')

clock = pg.time.Clock()
fps = 60

player_w = 15
player_h = 110
player_speed = 10

ball_radius = 15
ball_speed = 6

background = 'black'

player_space_from_edge = 40

p1 = Striker(player_space_from_edge, screen.get_height() // 2, player_w, player_h, player_speed, 'white', screen, [pg.K_w, pg.K_s])
p2 = Striker(screen.get_width() - (player_space_from_edge + 10), screen.get_height() // 2, player_w, player_h, player_speed, 'white', screen, [pg.K_UP, pg.K_DOWN])

players = [p1, p2]

ball = Ball(screen.get_width() // 2, screen.get_height() // 2, ball_radius, ball_speed, screen)

def divider():
  for i in range(0, screen.get_height(), 21):
    if i % 42 == 0:
      pg.draw.rect(screen, 'white', (screen.get_width() // 2 - 2, i, 4, 21))

def listener(flags, players):
  for event in pg.event.get():
    if event.type == pg.QUIT:
      flags['running'] = False

    if event.type == pg.KEYDOWN:
      for player in players:
        player.keydown(event.key)

      if event.key == pg.K_SPACE:
        flags['start'] = not flags['start']
        flags['started'] = True

    if event.type == pg.KEYUP:
      for player in players:
        player.keyup(event.key)

def pvp():
  flags = {
    'running': True,
    'start': False,
    'started': False
  }

  p1_score, p2_score = 0, 0
  last_striker = p1 if ball.x_fac > 0 else p2
  opposite_striker = p2 if last_striker == p1 else p1

  powerup_mngr = PowerUpManager(spawn_interval=15, max_spawns=3, screen=screen)

  while flags['running']:
    screen.fill(background)
    divider()
    listener(flags, players)

    if not flags['start'] and not flags['started']:
      text = font20.render('Press SPACE to start!', True, 'white')
      text_rect = text.get_rect()
      text_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
      screen.blit(text, text_rect)

      p1.show()
      p2.show()

      pg.display.update()
      clock.tick(fps)

      continue

    elif not flags['start']:
      text = font20.render('Press SPACE to resume!', True, 'white')
      text_rect = text.get_rect()
      text_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
      screen.blit(text, text_rect)

      powerup_mngr.paused()

      p1.show()
      p2.show()
      ball.show()

      pg.display.update()
      clock.tick(fps)

      continue

    for player in players:
      if pg.Rect.colliderect(ball.getRect(), player.getRect()):
        ball.hit(player)
        p1.speed += 0.4
        p2.speed += 0.4

        last_striker = player
        opposite_striker = p1 if last_striker == p2 else p2
        break

    powerup_mngr.resumed()
    powerup_mngr.update(ball, last_striker, opposite_striker)
    powerup_mngr.spawn()

    p1.update()
    p2.update()
    point = ball.update()

    if point == -1:
      p1_score += 1
      last_striker = p1
      opposite_striker = p2

    elif point == 1:
      p2_score += 1
      last_striker = p2
      opposite_striker = p1

    if point:
      ball.reset()
      powerup_mngr.reset()

      p1.reset()
      p2.reset()

    p1.show()
    p2.show()
    ball.show()

    p1.displayScore('Player 1:', p1_score, 100, 20, font20, 'white')
    p2.displayScore('Player 2:', p2_score, screen.get_width() - 100, 20, font20, 'white')

    clock.tick(fps)
    pg.display.update()

if __name__ == '__main__':
  pvp()
  pg.quit()
