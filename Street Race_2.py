import pygame as pg
import random
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
path = os.path.dirname(os.path.abspath(__file__))
record_file = os.path.join(path, 'record.txt')
try:
    with open(record_file, 'x') as f:
        f.write(str(0))
except BaseException:
    pass

SIZE = WIDTH, HEIGHT = 800, 600
GREY = (128, 128, 128)
GREEN = (0, 128, 0)
WHITE = (200, 200, 200)
rgb = [0, 250, 0]
block = False
pause = [False, True]
car_accident = 0
level = 40
count = [0]
start = 255
hit_old = None

pg.init()
pg.display.set_caption('Rally')
screen = pg.display.set_mode(SIZE)

FPS = 120
clock = pg.time.Clock()
font = pg.font.Font(None, 32)

cars = [pg.image.load(os.path.join(path, 'img', 'car1.png')),
        pg.image.load(os.path.join(path, 'img', 'car2.png')),
        pg.image.load(os.path.join(path, 'img', 'car3.png'))]
alarm = [pg.image.load(os.path.join(path, 'alarm', '1.png')),
         pg.image.load(os.path.join(path, 'alarm', '2.png'))]
sound_car_accident = pg.mixer.Sound(os.path.join(path, 'sound', 'udar.wav'))
sound_canister = pg.mixer.Sound(os.path.join(path, 'sound', 'canister.wav'))
sound_accident = pg.mixer.Sound(os.path.join(path, 'sound', 'accident.wav'))

button_start = pg.image.load(os.path.join(path, 'img', 'btn_play.png'))
button_start_rect = button_start.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
button_stop = pg.image.load(os.path.join(path, 'img', 'btn_exit.png'))
button_stop_rect = button_stop.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

fuel_image = pg.image.load(os.path.join(path, 'img', 'fuel.png'))
canister_image = pg.image.load(os.path.join(path, 'img', 'canister.png'))
water_image = pg.image.load(os.path.join(path, 'img', 'water.png'))

u1_event = pg.USEREVENT + 1
pg.time.set_timer(u1_event, random.randrange(6000, 26001, 4000))
u2_event = pg.USEREVENT + 2
pg.time.set_timer(u2_event, random.randrange(7000, 27001, 5000))


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pg.image.load(os.path.join(path, 'img', 'car4.png'))
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


class Alarm(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.images = alarm
        self.index = 0
        self.range = len(self.images)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.speed = 1

    def update(self):
        self.index += 0.02
        self.image = self.images[int(self.index % self.range)]
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()
        if start == 255:
            for s in all_sprite:
                if s == self:
                    s.kill()


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
                if 40 < player.rect.centerx < WIDTH - 40 \
                        and player.rect.top < HEIGHT and player.rect.bottom > 0:
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


class Volume(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((20, 140), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.radius = 10
        self.alpha = 70
        self.x = self.y = self.radius
        self.image.fill((0, 180, 0))

    def update(self):
        self.image.set_alpha(self.alpha)
        pg.draw.circle(self.image, (0, 255, 0), (self.x, self.y), self.radius)


all_sprite = pg.sprite.LayeredUpdates()
cars_group = pg.sprite.Group()
canister_group = pg.sprite.Group()
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
vol = Volume(20, HEIGHT - 80)

all_sprite.add(cars_group, layer=1)
all_sprite.add(player, layer=2)
all_sprite.add(fuel, layer=3)
all_sprite.add(vol, layer=4)


def my_record():
    with open(record_file, 'r+') as d:
        record = d.read()
        if count[0] > int(record):
            record = str(count[0])
            d.seek(0)
            d.truncate()
            d.write(record)
    return record


def home_screen():
    sc = pg.Surface(screen.get_size())
    sc.fill(pg.Color('navy'))
    button_start.set_alpha(start)
    sc.blit(button_start, button_start_rect)
    sc.blit(button_stop, button_stop_rect)
    screen.blit(sc, (0, 0))
    screen.blit(font.render(f'Record: {int(rec)}', 1, GREEN), (10, 10))
    screen.blit(font.render(f'Points: {count[0]}', 1, GREEN), (10, 40))
    screen.blit(font.render(f'Accidents: {car_accident}', 1, GREEN), (10, 70))


rec = my_record()
game = True
while game:
    for e in pg.event.get():
        if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            game = False
        elif e.type == pg.KEYDOWN and e.key == pg.K_p:
            pause.reverse()
        elif e.type == pg.MOUSEMOTION and start == 0:
            if e.pos[0] < 40 and e.pos[1] > vol.rect.top:
                pg.mouse.set_visible(True)
                vol.alpha = 70
                if vol.rect.left < e.pos[0] < vol.rect.right and \
                        vol.rect.top < e.pos[1] < vol.rect.bottom and \
                        e.buttons[0]:
                    vol.image.fill((0, 180, 0))
                    vol.y = abs(vol.rect.top - e.pos[1])
                    if vol.y > vol.rect.h - vol.radius:
                        vol.y = vol.rect.h - vol.radius
                    elif vol.y < vol.radius:
                        vol.y = vol.radius
                    volume = 1 - vol.y / float(vol.rect.h - vol.radius)
                    sound_car_accident.set_volume(volume)
                    sound_canister.set_volume(volume)
                    sound_accident.set_volume(volume)
            else:
                vol.alpha -= 1
                pg.mouse.set_visible(False)
        elif e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                if button_start_rect.collidepoint(e.pos):
                    player.angle = 0
                    player.position = WIDTH - 20, HEIGHT - 70
                    player.update()
                    for cr in cars_group:
                        cr.speed = random.randint(2, 3)
                        cr.rect.bottom = 0
                    level = 40
                    car_accident = 0
                    count[0] = 0
                    start -= 1
                    pause[:] = False, True
                    pg.mouse.set_visible(False)
                elif button_stop_rect.collidepoint(e.pos):
                    game = False
        elif not pause[0]:
            if e.type == u1_event:
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

    hit = pg.sprite.spritecollideany(player, cars_group)  # hit -> sprite car
    if hit and hit.speed != 1:
        player.position.x += 50 * random.randrange(-1, 2, 2)
        player.angle = 50 * random.randrange(-1, 2, 2)
        hit.speed = 1
        car_alarm = Alarm()
        all_sprite.add(car_alarm, layer=1)
        car_alarm.rect.center = hit.rect.center
        car_accident += 1
        if car_accident > 10:
            car_accident = 10
        sound_car_accident.play()
    if pg.sprite.spritecollide(player, canister_group, True):
        level = 40
        sound_canister.play()
    if pg.sprite.collide_rect(player, water):
        if not block:
            player.angle = random.randint(60, 90) * random.randrange(-1, 2, 2)
            sound_accident.play()
            block = True
    else:
        block = False

    if vol.alpha < 70:
        vol.alpha = 0 if vol.alpha <= 0 else vol.alpha - 1
    if start > 0:
        home_screen()
        if start != 255:
            start -= 1
    else:
        if not pause[0]:
            level -= .01
            if level < 0 or car_accident > 9:
                start = 255
                rec = my_record()
                pg.mouse.set_visible(True)
            elif level < 10:
                rgb[:2] = 250, 0
            elif level < 20:
                rgb[0] = 250
            else:
                rgb[:2] = 0, 250

            all_sprite.update()
        else:
            vol.update()
        all_sprite.draw(screen)
        pg.draw.rect(
            screen, rgb,
            (fuel.rect.left + 10, fuel.rect.bottom - level - 8, 21, level))
        screen.blit(font.render(f'accidents: {car_accident}', 1, GREEN), (46, 10))
        screen.blit(font.render(f'{count[0]}', 1, GREEN), (46, HEIGHT - 30))

    pg.display.update()
    clock.tick(FPS)
    pg.display.set_caption(f'Rally      FPS: {int(clock.get_fps())}')

# pg.image.save(screen, 'road.jpg')
