from pygame import *
from random import randint

window = display.set_mode((1000, 700))
display.set_caption('Где')
background = transform.scale(image.load('galaxy.png'), (1000, 700))
window.blit(background, (0, 0))

game = True
finish = False

clock = time.Clock()
FPS = 60

winy = 700

font.init()
font1 = font.Font(None, 80)
win = font1.render('Победа', True, (255, 255, 255))
lose = font1.render('Поражение', True, (180, 0, 0))

font2 = font.Font(None, 36)

score = 0
lost = 0

mixer.init()
mixer.music.load('fon.mp3')
mixer.music.set_volume(0.2)
mixer.music.play()
bul = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, px, py, ps, h, w):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (h, w))
        self.speed = ps
        self.rect = self.image.get_rect()
        self.rect.x = px
        self.rect.y = py  

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Player(GameSprite):
    def __init__ (self, player_image, px, py, ps, h, w, hp):
        super().__init__(player_image, px, py, ps, h, w)
        self.hp = hp
    def update(self):
        keys = key.get_pressed()
        
        if keys[K_LEFT] and self.rect.x > 0: 
            self.rect.x -= self.speed
            
        if keys[K_RIGHT] and self.rect.x < 900: 
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, 549, 50, 50, 50)
        bul.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= winy:
            self.rect.y = 0
            self.rect.x = randint(0, 900)
            lost = lost + 1



enemy1 = Enemy('ufo.png', randint(0,850), -40, randint(1, 3), 100 , 100)
enemy2 = Enemy('ufo.png', randint(0,850), -40, randint(1, 3), 100 , 100)
enemy3 = Enemy('ufo.png', randint(0,850), -40, randint(1, 3), 100 , 100)
enemy4 = Enemy('ufo.png', randint(0,850), -40, randint(1, 3), 100 , 100)
enemy5 = Enemy('ufo.png', randint(0,850), -40, randint(1, 3), 100 , 100)

player = Player('rocket.png', 0, 549, 20, 100, 100, 3)

mons = sprite.Group()
mons.add(enemy1)
mons.add(enemy2)
mons.add(enemy3)
mons.add(enemy4)
mons.add(enemy5)

bonus = GameSprite('hp.png', randint(0, 900), randint(10, 400), 0,  80, 80)


while game:
    window.blit(background, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                
                player.fire()

    if  not finish:
        window.blit(background, (0,0))

        player.reset()
        player.update()
        mons.draw(window)
        mons.update()
        bul.update()
        bonus.update()
        bonus.reset()
        bul.draw(window)



        collides = sprite.groupcollide(mons, bul, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(0,850), -40, randint(1, 3), 100 , 100)
            mons.add(monster)
        
        if sprite.spritecollide(bonus, bul, True):
            player.hp += 1
            bonus.rect.x = randint(0, 900)
            bonus.rect.y = randint(10, 400)

        if sprite.spritecollide(player, mons, True):
            player.hp -= 1
            enemy1 = Enemy('ufo.png', randint(0,850), -40, randint(1, 3), 100 , 100)
            mons.add(enemy1)
            

        if sprite.spritecollide(player, mons, False) or lost >= 3 or player.hp == 0:
            finish = True
            window.blit(lose, (200, 200))

        if score >= 999:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render('Счет:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render('Пропущено:' + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10, 50))

        text_hp = font2.render('Здоровье:' + str(player.hp), 1, (255,255,255))
        window.blit(text_hp, (10, 80))

        display.update()
    clock.tick(FPS) 

