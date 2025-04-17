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
        if key_pressed[K_RIGHT] and self.rect.x < 1200:
            self.rect.x += speed
        if  key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= speed
        '''if key_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= speed
        if key_pressed[K_DOWN] and self.rect.y < 595:
            self.rect.y += speed'''
    def fire(self):
        bullet = Bullet('bullet.png', player.rect.centerx, player.rect.top, 8, 15, 30)
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
        if self.rect.y > 900:
            self.rect.x = randint(0, 1250)
            self.rect.y = 0
            lost += 1

class Boss(Game):
    def __init__(self, player_image, player_x, player_y, player_speed, width, hight, direct):
        super().__init__(player_image, player_x, player_y, player_speed, width, hight)
        self.direct = direct
    def update(self):
        if self.rect.y < 10:
            self.rect.y += 3
    def run(self):
        if self.rect.x <= 0:
            self.direct = 'right'
        if self.rect.x >= 1040:
            self.direct = 'left'
        
        if self.direct == 'right':
            self.rect.x += self.speed
        if self.direct == 'left':
            self.rect.x -= self.speed


window = display.set_mode((1300, 1000))
display.set_caption('Шутер')
background = transform.scale(image.load('background.png'),(1300, 1000))
player = Player('yellow_soul.png', 600, 900, 5, 80, 80)

enemys = sprite.Group()
for i in range(1, 6):
    enemy = Enemy('muttaton_bullet.png', randint(0, 1200), 0, randint(2, 6), 145, 145)
    enemys.add(enemy)

boss = Boss('2_.png', 450, -350, 5, 350, 300, 'left')

game_over = Game('game_over.png', 370, 280, 0, 530, 250)
game_win = Game('fonts.png', 260, 350, 0, 700, 150)

hearts = sprite.Group()
for i in range(1, 7):
    heart = Enemy('heart.png', randint(0, 1270), 0, randint(3, 9), 85, 85)
    hearts.add(heart)

mixer.init()
mixer.music.load('crush_metal.ogg')
mixer.music.play()
mixer.music.set_volume(0.5)

fire_sound = mixer.Sound('bullet.ogg')
fire_sound.set_volume(0.2)

death_sound = mixer.Sound('game_over.ogg')
boss_music = mixer.Sound('Mettaton_EX.ogg')
win_music = mixer.Sound('sound_win.ogg')
damage_sound = mixer.Sound('damage_taken.ogg')
damage_sound.set_volume(0.3)

font.init()
font1 = font.SysFont('Arial', 35)
font2 = font.SysFont('Arial', 35)
font3 = font.SysFont('Arial', 35)
font4 = font.SysFont('Arial', 35)

health = 5
boss_kill = 15
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

        text_lost = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lost, (10,40))

        count = font3.render('Счёт: ' + str(winn), 1, (255, 255, 255))
        window.blit(count, (10, 70))

        text_health = font3.render('Здоровье: ' + str(health), 1, (255, 255, 255))
        window.blit(text_health, (10, 10))

        if sprite.spritecollide(player, enemys, True):
            health = health - 1
            damage_sound.play()
            text_health = font3.render('Здоровье: ' + str(health), 1, (255, 255, 255))
            window.blit(text_health, (10, 70))
            enemy = Enemy('muttaton_bullet.png', randint(0, 1200), 0, randint(1, 6), 150, 150)
            enemys.add(enemy)

        if health == 0:
            finish = True
            game_over.reset()
            mixer.music.stop()
            death_sound.play()

        if sprite.groupcollide(bullets, enemys, True, True):
            winn += 1
            enemy = Enemy('muttaton_bullet.png', randint(0, 1200), 0, randint(1, 6), 150, 150)
            enemys.add(enemy)
            
            if int(winn) >= 15 :
                finish2 = True
                finish = True
                mixer.music.stop()
                boss_music.play()

    if finish2 == True:
        window.blit(background, (0, 0))
        player.reset()
        player.update(5)

        enemys.update()
        enemys.draw(window)

        bullets.update()
        bullets.draw(window)

        text_health = font3.render('Здоровье: ' + str(health), 1, (255, 255, 255))
        window.blit(text_health, (10, 10))

        boss_health_text = font4.render('Здоровье босса: ' + str(boss_kill), 1, (255, 255, 255))
        window.blit(boss_health_text, (10, 40))

        enemys.empty()
        boss.reset()
        boss.update()
        if boss.rect.y >= 10:
            boss.run()
            hearts.update()
            hearts.draw(window)
            if sprite.spritecollide(boss, bullets, True):
                boss_kill -= 1
                damage_sound.play()
                boss_health_text = font4.render('Здоровье босса: ' + str(boss_kill), 1, (255, 255, 255))
                window.blit(boss_health_text, (10, 40))

        if sprite.spritecollide(player, hearts, True):
            health = health - 1
            damage_sound.play()
            text_health = font3.render('Здоровье: ' + str(health), 1, (255, 255, 255))
            window.blit(text_health, (10, 10))
            heart = Enemy('heart.png', randint(0, 1210), 0, randint(3, 9), 85, 85)
            hearts.add(heart)

        if health == 0:
            finish2 = False
            game_over.reset()
            boss_music.stop()
            death_sound.play()

        if boss_kill == 0 :
            game_win.reset()
            boss_music.stop()
            win_music.play()
            finish2 = False
        print('Выстрел', winn)
        print('boss_kill', boss_kill)
    display.update()
    clock.tick(FPS)