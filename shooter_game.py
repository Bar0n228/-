from typing import Any
from pygame import *
from random import randint

class Game(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, hight):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width,hight))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
bullets = sprite.Group()

class Player(Game):
    def update(self, speed):
        key_pressed = key.get_pressed()
        if key_pressed[K_RIGHT] and self.rect.x < 795:
            self.rect.x += speed
        if  key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= speed
        '''if key_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= speed
        if key_pressed[K_DOWN] and self.rect.y < 595:
            self.rect.y += speed'''
    def fire(self):
        bullet = Bullet('bullet.png', player.rect.centerx, player.rect.top, 6, 20, 25)
        bullets.add(bullet)

class Bullet(Game):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
    def boss_bullets(self):
        pass
        
lost = 0
winn = 0
class Enemy(Game):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 600:
            self.rect.x = randint(0, 810)
            self.rect.y = 0
            lost += 1
class Boss(Game):
    def update(self):
        if self.rect.y < 30:
            self.rect.y += self.speed
    """def run(self):
        if self.rect.x < 650:
            righ_run = False
        if self.rect.x == 100 :
            righ_run = True
        if righ_run == True:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed"""

window = display.set_mode((900, 700))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'),(900,700))
player = Player('rocket.png', 400, 560, 5, 80, 130)

enemys = sprite.Group()
for i in range(1, 6):
    enemy = Enemy('asteroid.png', 0, randint(1, 810), randint(1, 4), 90, 90)
    enemys.add(enemy)  

boss2 = Boss('ufo.png', 260, 0, 3, 350, 200)
boss = sprite.Group()
boss.add(boss2)
boss_kill = 0

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 35)
font2 = font.SysFont('Arial', 60)
font3 = font.SysFont('Arial', 35)
font4 = font.SysFont('Arial', 60)

game = True
finish = False
finish2 = False
clock = time.Clock()
FPS = 60
abc1 = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()
    if finish != True: 
        window.blit(background, (0, 0))
        player.reset()
        player.update(5)

        enemys.update()
        enemys.draw(window)

        bullets.update()
        bullets.draw(window)

        text_lost = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lost, (10,40))

        count = font3.render('Счёт:' + str(winn), 1, (255, 255, 255))
        window.blit(count, (10, 10))

        if sprite.spritecollide(player, enemys, False):
            finish = True
            lose = font2.render('YOU LOSE' , 1, (255, 255, 255))
            window.blit(lose, (350, 250))

        if sprite.groupcollide(bullets, enemys, True, True):
            winn += 1
            enemy = Enemy('asteroid.png', 0, randint(0, 810), randint(1, 3), 100, 70)
            enemys.add(enemy)
            

            if int(winn) >= 15 :
                finish2 = True
                finish = True

    if finish2 == True:
        window.blit(background, (0, 0))
        player.reset()
        player.update(5)

        enemys.update()
        enemys.draw(window)

        bullets.update()
        bullets.draw(window)

        text_lost = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lost, (10,40))

        count = font3.render('Счёт:' + str(winn), 1, (255, 255, 255))
        window.blit(count, (10, 10))
        enemys.empty()
        boss.draw(window)
        boss.update()

        if sprite.groupcollide(bullets, boss, True, False):
            boss_kill += 1

        if boss_kill == 15:
            win = font4.render('YOU WIN!!', 1, (255, 255, 255))
            window.blit(win, (350, 250))
            finish2 = False
        print('Выстрел', winn)
        print('boss_kill', boss_kill)
    display.update()
    clock.tick(FPS)