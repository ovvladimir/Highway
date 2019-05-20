import pygame as pg
import sys
import random
import math

import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

W = 800
H = 600
BG = (100, 100, 100)
WHITE = (255, 255, 255)
car_accident = 0
drove_cars = 0
speed = 2
acceleration = 0.05
fscreen = [1, 2]
level = 40
R, G, B = 0, 255, 0
radius = 140
stop = 1
start = 1
game = True

image_btn1 = pg.image.load('img/btn_play.png')
image_btn2 = pg.image.load('img/btn_exit.png')
player_image = pg.image.load('img/Car.png')
fuel_image = pg.image.load('img/fuel.png')
canister_image = pg.image.load('img/canister.png')
tree_image = pg.image.load('img/d.png')
CARS = [pg.image.load('img/car1.png'), pg.image.load('img/car2.png'),
        pg.image.load('img/car3.png')]
n = len(CARS)
COLOR = ['red3', 'dark green', 'navy', 'orange']
imgColor = pg.image.load('img/car4.png')
originalColor = imgColor.get_at((imgColor.get_width()//2, imgColor.get_height()//2))
ar = pg.PixelArray(imgColor)
ar.replace(originalColor, pg.Color(COLOR[random.randint(0, len(COLOR)-1)]), 0.1)
del ar
CARS.append(imgColor)

FPS = 120
clock = pg.time.Clock()

pg.init()
u1_event = pg.USEREVENT + 1
pg.time.set_timer(u1_event, 350)
u2_event = pg.USEREVENT + 2
pg.time.set_timer(u2_event, 27000)

text1 = pg.font.SysFont('Arial', 24, True, True)
text2 = pg.font.SysFont('Arial', 16, True, False)
text3 = pg.font.SysFont('Arial', 50, True, True)
txt = text3.render('GAME OVER', True, pg.Color('red'), None)
txt_w, txt_h = text3.size('GAME OVER')
txt_pos = ((W - txt_w) / 2, (H - txt_h) / 2)
txt2 = text3.render('MOTORWAY', True, pg.Color('blue'), None)
txt2_w, txt2_h = text3.size('MOTORWAY')
txt2_pos = ((W - txt2_w) / 2, (H - txt2_h) / 2)
txt_km = text2.render('km/h', True, WHITE, None)
txt_km_pos = (745, 550)

pg.display.set_icon(pg.image.load('img/car.png'))
pg.display.set_caption('Motorway')
pg.mouse.set_visible(True)
screen = pg.display.set_mode((W, H))

pg.mixer.pre_init(44100, -16, 2, 1024)
tick = pg.mixer.Sound('sound/ticking.wav')
sound_car_accident = pg.mixer.Sound('sound/accident.wav')
sound_canister = pg.mixer.Sound('sound/canister.wav')
sound_length = sound_canister.get_length() * 1000
sound_start = pg.mixer.Sound('sound/Car Vroom.wav')
sound_start.play()
if os.name is 'nt':
    pg.mixer.music.load('sound/fon.mp3')
    pg.mixer.music.play(-1)
else:
    pg.mixer.music.load('sound/motorway.wav')
    pg.mixer.music.play(-1)


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, angle, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.orig_image = self.image
        self.angle = angle
        self.speed = speed
        self.rect = self.image.get_rect()
        self.position = pg.math.Vector2(x, y)
        self.velocity = pg.math.Vector2()

    def update(self):
        self.image = pg.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.position += self.velocity
        self.rect.center = self.position


class Car(pg.sprite.Sprite):
    def __init__(self, x, y, image, dy, group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.flip(image, False, dy)
        self.x = x
        self.y = y
        self.h = image.get_height()
        self.w = image.get_width() // 2
        self.rect = self.image.get_rect(center=(self.x, self.y))
        group.add(self)
        self.speed = random.randint(3, 5)

    def render(self):
        global car_x, car_y, car_dy
        block = 0
        direction = random.randint(0, 1)
        if direction == 0:
            car_y = - self.h
            car_dy = True
            car_x = random.randrange(80, W/2, 80)
        elif direction == 1:
            car_y = H + self.h
            car_dy = False
            car_x = random.randrange(W/2+80, W, 80)
        for img in cars:
            if car_x == img.rect.x + img.w:
                block = 1
        if block == 0:
            num = random.randint(0, n)
            if num == 3:
                original_Color = CARS[num].get_at((CARS[num].get_width()//2, CARS[num].get_height()//2))
                arr = pg.PixelArray(CARS[num])
                arr.replace(original_Color, pg.Color(COLOR[random.randint(0, len(COLOR)-1)]), 0.1)
                del arr
            car_new = Car(car_x, car_y, CARS[num], car_dy, cars)
            all_sprites.add(car_new, layer=2)

    def update(self):
        global drove_cars
        if self.x < W / 2:
            self.rect.y += self.speed
            if self.rect.y > H + self.h:
                self.kill()
                drove_cars += 1
        if self.x > W / 2:
            self.rect.y -= self.speed - 1
            if self.rect.y < 0 - self.h:
                self.kill()
                drove_cars += 1


class Background(pg.sprite.Sprite):
    def __init__(self, x, y, group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((W, H), pg.SRCALPHA)
        pg.draw.line(self.image, (0, 128, 0), [20, 0], [20, 600], 40)
        pg.draw.line(self.image, (0, 128, 0), [780, 0], [780, 600], 40)
        pg.draw.line(self.image, (0, 128, 0), [400, 0], [400, 600], 80)
        for xx in range(10):
            for yy in range(10):
                pg.draw.line(self.image, (200, 200, 200),
                             [40+xx*80, 0 if xx == 0 or xx == 4 or xx == 5 or xx == 9 else 10+yy*60],
                             [40+xx*80, 600 if xx == 0 or xx == 4 or xx == 5 or xx == 9 else 50+yy*60], 5)
        self.speed = speed
        group.add(self)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= H:
            self.rect.y = - H


class Varia(pg.sprite.Sprite):
    def __init__(self, x, y, image, h):
        self.h = h
        pg.sprite.Sprite.__init__(self)
        if image is tree_image:
            self.image = pg.transform.scale(image, (image.get_width()//2, h//2))
        else:
            self.image = image
        self.speed = speed
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= H:
            self.rect.y = - H
            if self is canister:
                self.kill()


cars = pg.sprite.Group()
roads = pg.sprite.Group()
trees = pg.sprite.Group()

player = Player(x=W/2+80, y=H/2, angle=0, image=player_image)
car = Car(random.randrange(0, W/2, 80), 0, CARS[random.randint(0, n)], True, cars)
for i in range(2):
    bg = Background(x=0, y=0 if i == 0 else -H, group=roads)
for ix in range(3):
    for iy in range(6):
        tree = Varia(x=ix*380, y=-H+iy*200, image=tree_image, h=tree_image.get_height())
        trees.add(tree)
canister = Varia(x=random.randrange(W/2+80, W, 80)-canister_image.get_width()/2,
                 y=-canister_image.get_height(), image=canister_image,
                 h=canister_image.get_height())

canisters = pg.sprite.Group(canister)
all_sprites = pg.sprite.LayeredUpdates()
all_sprites.add(roads, layer=0)
all_sprites.add(cars, layer=2)
all_sprites.add(trees, layer=4)


def speedometer():
    value = 0
    for deg in range(5, 84, 6):
        length = 20 if deg == 5 or deg == 23 or deg == 41 or deg == 59 or deg == 77 else 10
        cos = math.cos(math.radians(deg))
        sin = math.sin(math.radians(deg))
        pg.draw.line(screen, WHITE,
                     [W - radius * cos, H - radius * sin],
                     [W - (radius - length) * cos, H - (radius - length) * sin], 2)
    for deg in range(9, 78, 17):
        cos = math.cos(math.radians(deg))
        sin = math.sin(math.radians(deg))
        screen.blit(text2.render(str(value), True, WHITE, None),
                    (W - (radius - 30) * cos, H - (radius - 30) * sin))
        value += 100
    screen.blit(txt_km, txt_km_pos)
    s = abs(30 - player.velocity.y * 14 if player.velocity.y <= 0 else 24 - player.velocity.y * 14)
    cos = math.cos(math.radians(s))
    sin = math.sin(math.radians(s))
    pg.draw.line(screen, (255, 0, 0),  [W, H],
                 [W - (radius - 10) * cos, H - (radius - 10) * sin], 4)
    pg.draw.circle(screen, WHITE, [W, H], 25, 0)


def game_over():
    global play, out
    pg.draw.ellipse(screen, pg.Color('lime green'), (100, 50, 600, 500), 0)
    if start == 1:
        screen.blit(txt2, txt2_pos)
    else:
        screen.blit(txt, txt_pos)
    play = screen.blit(image_btn1, ((W-image_btn1.get_width())/2, (H-image_btn1.get_height())/2-100))
    out = screen.blit(image_btn2, ((W-image_btn2.get_width())/2, (H-image_btn2.get_height())/2+100))

game_over()
while game:
    clock.tick(FPS)
    if pg.event.get(pg.QUIT):
        break
    for e in pg.event.get():
        if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            game = False
        elif e.type == u1_event and stop == 0:
            car.render()
        elif e.type == u2_event and stop == 0:
            canisters.add(canister)
            all_sprites.add(canister, layer=1)
            canister.rect.center = random.randrange(W/2+80, W, 80), - canister.h
            pg.time.set_timer(u2_event, random.randrange(7000, 27001, 5000))
        elif e.type == pg.KEYDOWN and e.key == pg.K_f:
            fscreen.reverse()
            if fscreen[0] == 1:
                screen = pg.display.set_mode((W, H))
            elif fscreen[0] == 2:
                screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        elif e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                if play.collidepoint(e.pos):
                    all_sprites.add(player, layer=3)
                    pg.mouse.set_visible(False)
                    car_accident = 0
                    drove_cars = 0
                    level = 40
                    stop = 0
                    start = 0
                elif out.collidepoint(e.pos):
                    game = False

    keys = pg.key.get_pressed()
    if keys[pg.K_RIGHT]:
        player.velocity.x = speed
        player.angle -= 1
        if player.angle < -20:
            player.angle = -20
    elif keys[pg.K_LEFT]:
        player.velocity.x = -speed
        player.angle += 1
        if player.angle > 20:
            player.angle = 20
    else:
        player.velocity.x = 0
        if player.angle < 0:
            player.angle += 1
        elif player.angle > 0:
            player.angle -= 1
    if keys[pg.K_UP]:
        player.velocity.y -= acceleration
        if player.velocity.y < -speed * 2:
            player.velocity.y = -speed * 2
    elif keys[pg.K_DOWN]:
        player.velocity.y += acceleration
        if player.velocity.y > speed + 1:
            player.velocity.y = speed + 1
    else:
        if player.velocity.y < 0:
            player.velocity.y += acceleration
            if player.velocity.y > 0:
                player.velocity.y = 0
        elif player.velocity.y > 0:
            player.velocity.y -= acceleration
            if player.velocity.y < 0:
                player.velocity.y = 0

    if player.position.x > W - 40:
        player.position.x = W - 40
    elif player.position.x < 40:
        player.position.x = 40
    elif player.position.y > H:
        player.position.y = H
    elif player.position.y < 0:
        player.position.y = 0

    if pg.sprite.spritecollide(player, cars, True):
        tick.stop()
        sound_car_accident.play()
        player.angle = random.randrange(-65, 65, 25)
        car_accident += 1
    elif pg.sprite.spritecollideany(player, trees):
        player.angle = -60
        player.velocity.y = speed
    elif pg.sprite.spritecollide(player, canisters, True):
        tick.stop()
        sound_canister.play(maxtime=int(sound_length-level*40))
        level = 40

    if player.position.x > W / 2:
        level -= round(0.01 + abs(player.velocity.y) / 1000.0, 3)
    else:
        level -= 0.02
    if level < 0 or car_accident >= 10:
        all_sprites.remove(player)
        pg.mouse.set_visible(True)
        stop = 1
        game_over()
        tick.stop()
    if level <= 10:
        R, G = 255, 0
        if stop == 0:
            tick.play()
    elif 10 < level < 15:
        R, G = 255, 255
    else:
        R, G = 0, 255

    if stop == 0:
        screen.fill(BG)
        all_sprites.update()
        all_sprites.draw(screen)
        pg.draw.rect(screen, (R, G, B), (730, 55, -20, -level))
        speedometer()
        screen.blit(fuel_image, (700, 5))
        screen.blit(text2.render(f'FPS: {int(clock.get_fps())}', True, WHITE, None), (367, 10))
    screen.blit(text1.render(f'Car accident: {car_accident}  Drove cars: {drove_cars}',
                             True, pg.Color('lime green'), None if start == 1 else BG), (50, 570))
    pg.display.update()

print(f'car accident: {car_accident}\ndrove cars: {drove_cars}')
sys.exit(0)
