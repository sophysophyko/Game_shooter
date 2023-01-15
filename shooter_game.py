#Создай собственный Шутер!
from time import time as timer
from pygame import *
from random import randint

window = display.set_mode((1000,800))
display.set_caption('Вау, просто космос')
background = transform.scale(image.load('galaxy.jpg'),(1000,800))
window.blit(background,(0,0))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)
fire = mixer.Sound('fire.ogg')


lifes = 0

rel_time = False
nu_fire = 0


game = True
finish = False
FPS = 60
clock = time.Clock()

class Game_sprite(sprite.Sprite):
    def __init__(self, p_image, player_speed, player_x, player_y, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(p_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
    
bullets = sprite.Group()
class Player(Game_sprite):
    def __init__(self, p_image, player_speed, player_x, player_y, size_x, size_y):
        super().__init__(p_image, player_speed, player_x, player_y, size_x, size_y)
    def update_(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x < 900:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', -8, self.rect.centerx, self.rect.top, 25, 30)
        bullets.add(bullet)
missed = 0
class Enemy(Game_sprite):
    def __init__(self, p_image, player_speed, player_x, player_y, size_x, size_y):
        super().__init__(p_image, player_speed, player_x, player_y, size_x, size_y)
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y > 800:
            self.rect.y = 0
            self.rect.x = randint(150,850)
            missed += 1

class Bullet(Game_sprite):
    def __init__(self, p_image, player_speed, player_x, player_y, size_x, size_y):
        super().__init__(p_image, player_speed, player_x,player_y, size_x, size_y)
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()


player_person = Player('rocket.png', 10, 500,650, 110,130)
u_f_o = sprite.Group()
for i in range(6):
    ufo1 = Enemy('ufo.png', randint(2,4), randint(150,850), randint(-200,0), 110,80)
    u_f_o.add(ufo1)

asteroids = sprite.Group()
for i in range(2):
    asteroid1 = Enemy('asteroid.png', 3, randint(150,850), -400, 110, 80)
    asteroids.add(asteroid1)
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 140)



text3 = font2.render('YOU LOSE!', True, (255,255,255))
text4 = font2.render('YOU WON!', True, (255,255,255))
score = 0
while game:


    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if nu_fire < 11 and rel_time==False:
                    player_person.fire()
                    fire.play()
                    nu_fire += 1
                if nu_fire >= 10 and rel_time == False:
                    rel_time == True
                    last_time = timer()



    if not finish:
        window.blit(background, (0,0))
        player_person.update_()
        player_person.reset()
        u_f_o.update()
        u_f_o.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)

        if rel_time==True:
            real_time = timer()
            if real_time - last_time < 1:
                text6 = font1.render('Reload bullets...', 1, (255,0,0))
                window.blit(text6, (300,700))
            else:
                rel_time = False
                nu_fire = 0

        plus_collide = sprite.groupcollide(u_f_o, bullets, True, True)
        for collide1 in plus_collide:
            ufo2 = Enemy('ufo.png', randint(1,3), randint(150,850), randint(-200,0), 110,80)
            u_f_o.add(ufo2)
            score +=1

        minus_collide = sprite.spritecollide(player_person, u_f_o, True)
        minus_collide2 = sprite.spritecollide(player_person, asteroids, True)
        if minus_collide or minus_collide2:
            lifes += 1
           # missed = 0
            
        if score == 10:
            finish = True
            window.blit(text4, (250,200))
        if lifes == 4:
            finish = True
            window.blit(text3, (250, 200))



        text1 = font1.render('Счет: '+str(score), 1, (255,255,255))
        text2 = font1.render('Пропущено: '+str(missed), 1, (255,255,255))
        text5 = font1.render('Жизни:'+str(100-lifes*25)+'%', 1, (255,255,255))
        window.blit(text1, (5,5))
        window.blit(text2,(5, 41))
        window.blit(text5,(5,77))


    display.update()
    clock.tick(FPS)
