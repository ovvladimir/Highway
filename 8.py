import pygame as pg
import sys
import random

W = 800
H = 600
BG = (100, 100, 100)
car_accident = 0
drove_cars = 0

player_image = pg.image.load('img/Car.png')
CARS = [pg.image.load('img/car1.png'), pg.image.load('img/car2.png'),
        pg.image.load('img/car3.png'), pg.image.load('img/car4.png')]
n = len(CARS) - 1

FPS = 120
clock = pg.time.Clock()

pg.init()
pg.time.set_timer(pg.USEREVENT, 300)

screen = pg.display.set_mode((W, H))
pg.display.set_caption('Автомагистраль')
pg.display.set_icon(pg.image.load('img/car.png'))
pg.mouse.set_visible(False)

text = pg.font.SysFont('Arial', 24, True, True)


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, angle, speed, image):
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
        self.position += self.velocity
        self.rect.center = self.position
        self.rect = self.image.get_rect(center=self.rect.center)


class Car(pg.sprite.Sprite):
    def __init__(self, x, image, group):
        pg.sprite.Sprite.__init__(self)
        # self.image = image
        self.image = pg.transform.flip(image, False, True)
        self.h = image.get_height()
        self.w = image.get_width() // 2
        self.rect = self.image.get_rect(center=(x, -self.h))
        self.add(group)
        self.speed = random.randint(3, 5)
        self.block = 0

    def render(self):
        car_x = random.randrange(80, W, 80)
        for img in cars:
            if car_x == img.rect.x + img.w:
                self.block = 1
        if self.block == 0:
            car_new = Car(car_x, CARS[random.randint(0, n)], cars)
            all_sprites.add(car_new, layer=2)
        else:
            self.block = 0

    def update(self):
        global drove_cars
        if self.rect.y < H + self.h:
            self.rect.y += self.speed
        else:
            self.kill()
            drove_cars += 1


class Background(pg.sprite.Sprite):
    def __init__(self, x, y, group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((W, H), pg.SRCALPHA)
        pg.draw.line(self.image, (0, 128, 0), [20, 0], [20, 600], 40)
        pg.draw.line(self.image, (0, 128, 0), [780, 0], [780, 600], 40)
        for xx in range(10):
            for yy in range(10):
                pg.draw.line(self.image, (200, 200, 200),
                             [40+xx*80, 0 if xx == 0 or xx == 9 else 10+yy*60],
                             [40+xx*80, 600 if xx == 0 or xx == 9 else 50+yy*60], 5)
        self.x = x
        self.y = y - 2
        self.speed = 2
        self.add(group)
        self.rect = self.image.get_rect()

    def update(self):
        self.y += self.speed
        if self.y >= H:
            self.y = - H
        self.rect.y = self.y


cars = pg.sprite.Group()
roads = pg.sprite.Group()

player = Player(x=W/2, y=H/2, angle=0, speed=2, image=player_image)
car = Car(random.randrange(80, W, 80), CARS[random.randint(0, n)], cars)
for i in range(2):
    bg = Background(x=0, y=0 if i == 0 else H, group=roads)

all_sprites = pg.sprite.LayeredUpdates()
all_sprites.add(roads, layer=1)
all_sprites.add(cars, layer=2)
all_sprites.add(player, layer=3)

game = True
while game:
    clock.tick(FPS)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            game = False
            print(f'car accident: {car_accident}\ndrove cars: {drove_cars}')
            sys.exit(0)
        elif e.type == pg.USEREVENT:
            car.render()
        '''elif e.type == pg.KEYDOWN:
            if e.key == pg.K_RIGHT:
                player.angle -= 15
                player.velocity.x = player.speed
            elif e.key == pg.K_LEFT:
                player.angle += 15
                player.velocity.x = -player.speed
            elif e.key == pg.K_DOWN:
                player.velocity.y = player.speed + 1
            elif e.key == pg.K_UP:
                player.velocity.y = -player.speed
        elif e.type == pg.KEYUP:
            if e.key == pg.K_RIGHT or e.key == pg.K_LEFT:
                player.velocity.x = 0
                player.angle = 0
            elif e.key == pg.K_DOWN or e.key == pg.K_UP:
                player.velocity.y = 0'''

    keys = pg.key.get_pressed()
    if keys[pg.K_RIGHT]:
        player.velocity.x = player.speed
        player.angle -= 1
        if player.angle < -20:
            player.angle = -20
    elif keys[pg.K_LEFT]:
        player.velocity.x = -player.speed
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
        player.velocity.y = -player.speed
    elif keys[pg.K_DOWN]:
        player.velocity.y = player.speed
    else:
        player.velocity.y = 0

    if player.position.x > 760:
        player.position.x = 760
    elif player.position.x < 40:
        player.position.x = 40
    elif player.position.y > 600:
        player.position.y = 600
    elif player.position.y < 0:
        player.position.y = 0

    if pg.sprite.spritecollide(player, cars, True):
        player.angle = random.randrange(-65, 65, 25)
        car_accident += 1

    screen.fill(BG)
    all_sprites.update()
    all_sprites.draw(screen)
    screen.blit(text.render(f'Аварий: {car_accident} Проехало машин: {drove_cars}',
                            True, pg.Color('lime green'), BG), (50, 570))
    pg.display.update()
