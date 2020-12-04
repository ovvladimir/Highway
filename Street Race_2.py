import pygame as pg
import random
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
try:
    with open('record.txt', 'x') as f:
        f.write(str(0))
except BaseException:
    pass

SIZE = WIDTH, HEIGHT = 800, 600
GREY = (128, 128, 128)
GREEN = (0, 128, 0)
WHITE = (200, 200, 200)
block = False
block2 = False
car_accident = 0
scr1 = True
level = 40
rgb = [0, 250, 0]
count = [0]

pg.init()
pg.display.set_caption('Rally')
screen = pg.display.set_mode(SIZE)
pg.mouse.set_visible(True)

FPS = 120
clock = pg.time.Clock()

cars = [pg.image.load('img/car1.png'), pg.image.load('img/car2.png'),
        pg.image.load('img/car3.png')]
sound_car_accident = pg.mixer.Sound('sound/udar.wav')
sound_canister = pg.mixer.Sound('sound/canister.wav')
sound_accident = pg.mixer.Sound('sound/accident.wav')
font = pg.font.Font(None, 32)

button_start = pg.image.load('img/btn_play.png')
button_start_rect = button_start.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
button_stop = pg.image.load('img/btn_exit.png')
button_stop_rect = button_stop.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

fuel_image = pg.image.load('img/fuel.png')
canister_image = pg.image.load('img/canister.png')
water_image = pg.image.load('img/water.png')

u1_event = pg.USEREVENT + 1
pg.time.set_timer(u1_event, random.randrange(6000, 26001, 4000))
u2_event = pg.USEREVENT + 2
pg.time.set_timer(u2_event, random.randrange(7000, 27001, 5000))


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pg.image.load('img/car4.png')
        self.orig_image = self.image
        self.angle = 0
        self.speed = 2
        self.acceleration = 0.02
        self.rect = self.image.get_rect()
        self.x, self.y = WIDTH - self.rect.w // 2, HEIGHT - self.rect.h
        self.position = pg.math.Vector2(self.x, self.y)
        self.velocity = pg.math.Vector2()

    def update(self):
        self.image = pg.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.position += self.velocity
        self.rect.center = int(self.position.x), int(self.position.y)

        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.velocity.x = self.speed
            self.angle -= 1
            if self.angle < -25:
                self.angle = -25
        elif keys[pg.K_LEFT]:
            self.velocity.x = -self.speed
            self.angle += 1
            if self.angle > 25:
                self.angle = 25
        else:
            self.velocity.x = 0
            if self.angle < 0:
                self.angle += 1
            elif self.angle > 0:
                self.angle -= 1
        if keys[pg.K_UP]:
            self.velocity.y -= self.acceleration
            if self.velocity.y < -self.speed:
                self.velocity.y = -self.speed
        elif keys[pg.K_DOWN]:
            self.velocity.y += self.acceleration
            if self.velocity.y > self.speed:
                self.velocity.y = self.speed
        else:
            if self.velocity.y < 0:
                self.velocity.y += self.acceleration
                if self.velocity.y > 0:
                    self.velocity.y = 0
            elif self.velocity.y > 0:
                self.velocity.y -= self.acceleration
                if self.velocity.y < 0:
                    self.velocity.y = 0


class Car(pg.sprite.Sprite):
    def __init__(self, x, y, img):
        pg.sprite.Sprite.__init__(self)

        if img == fuel_image:
            self.image = img
            self.speed = 0
        elif img == canister_image or img == water_image:
            self.image = img
            self.speed = 1
        else:
            self.image = pg.transform.flip(img, False, True)
            self.speed = random.randint(2, 3)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += self.speed
        if self.rect.top >= HEIGHT:
            if self == canister or self == water:
                self.kill()
            else:
                count[0] += 1
                list_x.remove(self.rect.centerx)
                while True:
                    self.rect.centerx = random.randrange(80, WIDTH, 80)
                    if self.rect.centerx in list_x:
                        continue
                    else:
                        list_x.append(self.rect.centerx)
                        self.speed = random.randint(2, 3)
                        self.rect.bottom = 0
                        break


class Road(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface(screen.get_size())
        self.image.fill(GREY)
        pg.draw.line(self.image, GREEN, (20, 0), (20, 600), 40)
        pg.draw.line(self.image, GREEN, (780, 0), (780, 600), 40)
        for xx in range(10):
            for yy in range(10):
                pg.draw.line(
                    self.image, WHITE,
                    (40 + xx * 80, 0 if xx == 0 or xx == 9 else 10 + yy * 60),
                    (40 + xx * 80, 600 if xx == 0 or xx == 9 else 50 + yy * 60), 5)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 1

    def update(self):
        self.rect.y += self.speed
        if self.rect.top >= HEIGHT:
            self.rect.bottom = 0


all_sprite = pg.sprite.LayeredUpdates()
cars_group = pg.sprite.Group()
canister_group = pg.sprite.Group()
water_group = pg.sprite.Group()
for r in range(2):
    all_sprite.add(Road(0, 0 if r == 0 else -HEIGHT), layer=0)
player = Player()

list_x = []
n = 0
while n < 6:
    x = random.randrange(80, WIDTH, 80)
    if x in list_x:
        continue
    else:
        list_x.append(x)
        cars_group.add(
            Car(x, random.randint(-cars[0].get_height() * 3, -cars[0].get_height()),
                cars[n] if n < 3 else random.choice(cars)))
        n += 1

fuel = Car(WIDTH - 80, 40, fuel_image)
canister = Car(0, 0, canister_image)
water = Car(0, 0, water_image)

all_sprite.add(cars_group, layer=1)
all_sprite.add(player, layer=2)
all_sprite.add(fuel, layer=3)


def my_record():
    with open('record.txt', 'r+') as d:
        record = d.read()
        if count[0] > int(record):
            record = str(count[0])
            d.seek(0)
            d.truncate()
            d.write(record)
    return record


def screen1(rec):
    sc = pg.Surface(screen.get_size())
    sc.fill(pg.Color('navy'))
    sc.blit(button_start, button_start_rect)
    sc.blit(button_stop, button_stop_rect)
    screen.blit(sc, (0, 0))
    screen.blit(font.render(f'Record: {int(rec)}', 1, GREEN), (10, 10))


game = True
while game:
    for e in pg.event.get():
        if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            game = False
        elif e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                if button_start_rect.collidepoint(e.pos):
                    player.angle = 0
                    player.position = WIDTH - 20, HEIGHT - 70
                    scr1 = False
                    level = 40
                    car_accident = 0
                    count[0] = 0
                    pg.mouse.set_visible(False)
                elif button_stop_rect.collidepoint(e.pos):
                    game = False
        elif e.type == u1_event:
            water_group.add(water)
            all_sprite.add(water, layer=0)
            water.rect.center = \
                random.randrange(80, WIDTH, 80), -water.rect.h
            timer1 = random.randrange(6000, 26001, 4000)
            pg.time.set_timer(u1_event, timer1)
        elif e.type == u2_event:
            canister_group.add(canister)
            all_sprite.add(canister, layer=0)
            canister.rect.center = \
                random.randrange(80, WIDTH, 80), -canister.rect.h
            timer = random.randrange(7000, 27001, 5000)
            pg.time.set_timer(u2_event, timer)

    if pg.sprite.spritecollideany(player, cars_group):
        if not block:
            player.position.x += 50 * random.randrange(-1, 2, 2)
            player.angle = 50 * random.randrange(-1, 2, 2)
            sound_car_accident.play()
            car_accident += 1
            block = True
    else:
        block = False
    if pg.sprite.spritecollide(player, canister_group, True):
        level = 40
        sound_canister.play()
    if pg.sprite.spritecollideany(player, water_group):
        if not block2:
            player.angle = random.randint(60, 90) * random.randrange(-1, 2, 2)
            sound_accident.play()
            block2 = True
    else:
        block2 = False

    if scr1:
        screen1(my_record())
    else:
        level -= .01
        if level < 0 or car_accident > 9:
            scr1 = True
            pg.mouse.set_visible(True)
        elif level < 10:
            rgb[:2] = 250, 0
        elif level < 20:
            rgb[0] = 250
        else:
            rgb[:2] = 0, 250

        all_sprite.update()
        all_sprite.draw(screen)
        pg.draw.rect(
            screen, rgb,
            (fuel.rect.left + 10, fuel.rect.bottom - level - 8, 21, level))
        screen.blit(font.render(f'аварии: {car_accident}', 1, GREEN), (46, 10))
        screen.blit(font.render(f'{count[0]}', 1, GREEN), (46, HEIGHT - 30))

    pg.display.update()
    clock.tick(FPS)
    pg.display.set_caption(f'Rally      FPS: {int(clock.get_fps())}')

# pg.image.save(screen, 'road.jpg')
