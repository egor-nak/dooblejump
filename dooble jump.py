import pygame
import sys
import sqlite3
import os
from datetime import datetime
pygame.init()
W = 400
H = 700
WHITE = (255, 255, 255)


# класс инопланетянина
class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.jump_sound = pygame.mixer.Sound("jumpsound.mp3")
        self.image = pygame.image.load(
            'mainplayer2.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.direction = 'l'
        self.rect.x = W // 2 - 50
        self.rect.y = H - 150
        self.fall = True
        self.jump = False
        self.counter = 0
        self.speed = 20
        self.coinscounter = 0
        self.counterofshooting = 0

    # движение вправо
    def move_right(self):
        if self.direction == 'l':
            self.image = pygame.transform.flip(self.image, True, False)
            self.direction = 'r'
        if self.rect.x <= W - 100 - 20:
            self.rect.x += 20

    # движение влево
    def move_left(self):
        if self.direction == 'r':
            self.image = pygame.transform.flip(self.image, True, False)
            self.direction = 'l'
        if self.rect.x >= 20:
            self.rect.x -= 20

    def update(self):
        if not self.jump:
            self.rect.y += self.speed - self.counter
            if self.counter != 0:
                self.counter -= 1
        else:
            self.rect.y -= self.speed - self.counter
            self.counter += 1
            if self.counter == 20:
                self.jump = False
        if self.counterofshooting == 0:
            self.image = pygame.image.load(
                'mainplayer2.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (100, 100))
            coords = (self.rect.x, self.rect.y)
            self.rect = self.image.get_rect()
            self.rect.x = coords[0]
            self.rect.y = coords[1]
            if self.direction == 'r':
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.counterofshooting -= 1

    # смена спрайта при стрельбе
    def shooting(self):
        self.image = pygame.image.load('shooting_mainplayer.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 120))
        coords = (self.rect.x, self.rect.y)
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.counterofshooting = 10

    # движение камеры
    def update2(self, sprites, coins):
        if self.rect.y < (H // 2):
            for coin in coins:
                coin.rect.y -= self.rect.y - 350
            for sprite in sprites:
                sprite.rect.y -= self.rect.y - 350

    # определение столкновений
    def collidedetection(self, ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
        ax2 = ax1 + ax2
        ay2 = ay1 + ay2
        bx2 = bx1 + bx2
        by2 = by1 + by2
        s1 = (ax1 >= bx1 and ax1 <= bx2) or (ax2 >= bx1 and ax2 <= bx2)
        s2 = (ay1 >= by1 and ay1 <= by2) or (ay2 >= by1 and ay2 <= by2)
        s3 = (bx1 >= ax1 and bx1 <= ax2) or (bx2 >= ax1 and bx2 <= ax2)
        s4 = (by1 >= ay1 and by1 <= ay2) or (by2 >= ay1 and by2 <= ay2)
        return "YES" if ((s1 and s2) or (s3 and s4)) or ((s1 and s4) or (s3 and s2)) else "NO"

    # определение столкновений
    def collide(self, platforms, coins, finish):
        for plat in platforms:
            if self.counterofshooting == 0:
                if self.direction == 'l':
                    if self.collidedetection(self.rect.x + 30, self.rect.y + 95, 90 - 30, 10, plat.rect.x, plat.rect.y,
                                             plat.rect.width, plat.rect.height) == 'YES':
                        if self.jump is False:
                            self.jump = True
                            self.counter = 0
                            self.jump_sound.play()
                if self.direction == 'r':
                    if self.collidedetection(self.rect.x, self.rect.y + 95, 90 - 30, 10, plat.rect.x, plat.rect.y,
                                             plat.rect.width, plat.rect.height) == 'YES':
                        if self.jump is False:
                            self.jump = True
                            self.counter = 0
                            self.jump_sound.play()
            else:
                if self.collidedetection(self.rect.x, self.rect.y + 95, 90, 10, plat.rect.x, plat.rect.y,
                                         plat.rect.width, plat.rect.height) == 'YES':
                    if self.jump is False:
                        self.jump = True
                        self.counter = 0
                        self.jump_sound.play()
        for coin in coins:
            if self.collidedetection(self.rect.x, self.rect.y, 100, 100, coin.rect.x, coin.rect.y,
                                     coin.rect.width, coin.rect.height) == 'YES':
                self.coinscounter += 1
                coin.rect.x += 500
        if self.collidedetection(self.rect.x, self.rect.y, 100, 100, finish.rect.x, finish.rect.y,
                                 finish.rect.width, finish.rect.height) == 'YES':
            return True

    # перезапуск
    def restart(self):
        self.rect.x = W // 2 - 50
        self.rect.y = H - 150
        self.fall = True
        self.jump = False
        self.counter = 0
        self.speed = 20
        self.coinscounter = 0

    def stop(self):
        self.rect.x = -100000

    def hide(self):
        self.rect.x = -100000


# класс первого фона
class background1(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'background.jpg').convert_alpha()
        self.image = pygame.transform.scale(self.image, (W, H))
        self.rect = self.image.get_rect()

    # движение камеры
    def move_right(self):
        self.rect.x += 1

    def move_left(self):
        self.rect.x -= 1

    def move_up(self):
        self.rect.y -= 20

    def move_down(self):
        self.rect.y += 20

    def update(self):
        if self.rect.y <= -700:
            self.rect.x = 700
        if self.rect.x > 700:
            self.rect.x = -700

    def hide(self):
        pass


# класс второго фона
class background2(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'background.jpg').convert_alpha()
        self.image = pygame.transform.scale(self.image, (W, H))
        self.rect = self.image.get_rect()
        self.rect.y -= H

    # движение камеры
    def move_up(self):
        self.rect.y -= 20

    def move_down(self):
        self.rect.y += 20

    def update(self):
        if self.rect.y <= -700:
            self.rect.y = 700

    def hide(self):
        pass


# класс платформ
class Platform(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'platforma.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 20))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        pass

    def restart(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def stop(self):
        self.rect.x = -10000

    def hide(self):
        self.rect.x = -10000


# класс монет
class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'coin.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.counter = 0

    # движение манет вверх вниз
    def update(self):
        if self.counter <= 10:
            self.rect.y -= 1
            self.counter += 1
        elif self.counter > 10:
            self.rect.y += 1
            self.counter += 1
            if self.counter == 20:
                self.counter = 0

    def restart(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.counter = 0

    def stop(self):
        self.rect.x = -10000

    def hide(self):
        self.rect.x = -10000


# класс паузы
class Pause(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'pause.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = W - 70
        self.rect.y = 0

    # проверка на нажатие
    def click_detection(self, x, y):
        if x in range(self.rect.x, self.rect.x + self.rect.width) and y in range(self.rect.y,
                                                                                 self.rect.y + self.rect.height):
            return True
        else:
            return False

    def stop(self):
        self.rect.x = -10000

    def hide(self):
        self.rect.x = -10000

    def show(self):
        self.rect.x = W - 70
        self.rect.y = 0


# класс кнопки продолжить
class Continuebutton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'countinue.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = -100

    def show(self):
        self.rect.x = W // 2 - (self.rect.width // 2)
        self.rect.y = H // 2 - self.rect.height

    def hide(self):
        self.rect.x = -100
        self.rect.y = -100

    # проверка нажатия
    def click_detection(self, x, y):
        if x in range(self.rect.x, self.rect.x + self.rect.width) and y in range(self.rect.y,
                                                                                 self.rect.y + self.rect.height):
            return True
        else:
            return False

    def hide(self):
        self.rect.x = -10000


# класс кнопки рестарт во время паузы
class Restart(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'restart.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = -100

    def show(self):
        self.rect.x = W // 2 - (self.rect.width // 2)
        self.rect.y = H // 2 + self.rect.height

    def hide(self):
        self.rect.x = -100
        self.rect.y = -100

    #  проверка нажатия
    def click_detection(self, x, y):
        if x in range(self.rect.x, self.rect.x + self.rect.width) and y in range(self.rect.y,
                                                                                 self.rect.y + self.rect.height):
            return True
        else:
            return False

    def hide(self):
        self.rect.x = -10000


# класс кнопки начала игры
class Startbutton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'start_button.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = -100

    def show(self):
        self.rect.x = W // 2 - (self.rect.width // 2)
        self.rect.y = H // 2 - (self.rect.height // 2)

    def hide(self):
        self.rect.x = -100
        self.rect.y = -100

    # проверка нажатия
    def click_detection(self, x, y):
        if x in range(self.rect.x, self.rect.x + self.rect.width) and y in range(self.rect.y,
                                                                                 self.rect.y + self.rect.height):
            return True
        else:
            return False

    def hide(self):
        self.rect.x = -10000


# класс логотипа
class Logo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'logo.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 150))
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = -100

    def show(self):
        self.rect.x = W // 2 - (self.rect.width // 2)
        self.rect.y = 50

    def hide(self):
        self.rect.x = -100
        self.rect.y = -100

    def hide(self):
        self.rect.x = -10000


# класс финишной черты
class Finishline(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'finish_line.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (W, 50))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.counter = 0

    def update(self):
        pass

    # перезапуск
    def restart(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.counter = 0

    def stop(self):
        self.rect.x = -10000

    def hide(self):
        self.rect.x = -10000


# класс пуль
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        radius = 5
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("brown"), (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.rect.x += 20
        self.shooting_sound = pygame.mixer.Sound("shootingsound.mp3")
        self.shooting_sound.play()

    def update(self):
        self.rect.y -= 50

    def hide(self):
        self.rect.x = -10000


# класс еадписи Game Over
class Gameover(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'game_over.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (W, 300))
        self.rect = self.image.get_rect()
        self.rect.x = -W
        self.rect.y = 400

    def hide(self):
        self.rect.x = -W
        self.rect.y = 400

    def show(self):
        self.rect.x = 0
        self.rect.y = 150


# класс монстра
class Monster(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'monster.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 150))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.counter = 0

    # движение монстра вверх-вниз
    def update(self):
        if self.counter <= 15:
            self.rect.y -= 1
            self.counter += 1
        elif self.counter > 10:
            self.rect.y += 1
            self.counter += 1
            if self.counter == 30:
                self.counter = 0

    # проверка соприкосновения
    def collidedetection(self, ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
        ax2 = ax1 + ax2
        ay2 = ay1 + ay2
        bx2 = bx1 + bx2
        by2 = by1 + by2
        s1 = (ax1 >= bx1 and ax1 <= bx2) or (ax2 >= bx1 and ax2 <= bx2)
        s2 = (ay1 >= by1 and ay1 <= by2) or (ay2 >= by1 and ay2 <= by2)
        s3 = (bx1 >= ax1 and bx1 <= ax2) or (bx2 >= ax1 and bx2 <= ax2)
        s4 = (by1 >= ay1 and by1 <= ay2) or (by2 >= ay1 and by2 <= ay2)
        return True if ((s1 and s2) or (s3 and s4)) or ((s1 and s4) or (s3 and s2)) else False

    def collide(self, bullets, alien):
        for bul in bullets:
            if self.collidedetection(self.rect.x, self.rect.y, 100, 150, bul.rect.x, bul.rect.y,
                                     bul.rect.width, bul.rect.height):
                if self.rect.y >= 0 and 0 <= self.rect.x <= W + 100:
                    self.hide()
                    alien.coinscounter += 50
        if self.collidedetection(self.rect.x, self.rect.y, 100, 150, alien.rect.x, alien.rect.y,
                                 alien.rect.width, alien.rect.height):
            alien.rect.y = H

    def restart(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.counter = 0

    def hide(self):
        self.rect.x = -500


#  класс кнопки рестарта после конца игры
class Restartaftergmovr(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'restart.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = -100

    def show(self):
        self.rect.x = W // 2 - (self.rect.width // 2)
        self.rect.y = H // 2 + self.rect.height

    def hide(self):
        self.rect.x = -100
        self.rect.y = -100

    def click_detection(self, x, y):
        if x in range(self.rect.x, self.rect.x + self.rect.width) and y in range(self.rect.y,
                                                                                 self.rect.y + self.rect.height):
            return True
        else:
            return False


# класс поздравляющей надписи
class Win(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'win.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (W, 300))
        self.rect = self.image.get_rect()
        self.rect.x = -W
        self.rect.y = 400

    def hide(self):
        self.rect.x = -W
        self.rect.y = 200

    def show(self):
        self.rect.x = 0
        self.rect.y = 150


# класс кнопки рейтинга
class Rating(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'reit.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = -100

    def show(self):
        self.rect.x = W // 2 - (self.rect.width // 2)
        self.rect.y = 500

    def hide(self):
        self.rect.x = -100
        self.rect.y = -100

    def click_detection(self, x, y):
        if x in range(self.rect.x, self.rect.x + self.rect.width) and y in range(self.rect.y,
                                                                                 self.rect.y + self.rect.height):
            return True
        else:
            return False


# класс кнопки перехода на стартовое окно
class Homebutton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'homeutton.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = -100

    def show(self):
        self.rect.x = W // 2 - (self.rect.width // 2)
        self.rect.y = 600

    def hide(self):
        self.rect.x = -100
        self.rect.y = -100

    def click_detection(self, x, y):
        if x in range(self.rect.x, self.rect.x + self.rect.width) and y in range(self.rect.y,
                                                                                 self.rect.y + self.rect.height):
            return True
        else:
            return False


# функция сохранения результатов
def saveresult():
    b = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(b, "Рейтинг.db")
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    result = cur.execute("""SELECT score FROM r
                    WHERE name=?""", (str(datetime.now()),)).fetchall()
    if len(result) == 0:
        result = cur.execute("""INSERT INTO r(Name,Score) VALUES(?, ?)""",
                             (str(datetime.now()), alien.coinscounter,)).fetchall()
    elif result[0][0] < alien.coinscounter:
        result = cur.execute("""UPDATE r
                                SET Score=?
                                WHERE Name=?""", (alien.coinscounter, 'you')).fetchall()

    result = cur.execute("""SELECT score FROM r
                            WHERE name=?""", (str(datetime.now()),)).fetchall()
    con.commit()
    con.close()


# функция показа рейтинга
def show_rating():
    startbutton.hide()
    logo.hide()
    b = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(b, "Рейтинг.db")
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    result = cur.execute("""Select * FROM r""").fetchall()
    result.sort(key=lambda x: int(x[-1]), reverse=True)
    texts = []
    font = pygame.font.Font(None, 36)
    for i in range(len(result[:10])):
        data = str(result[i][0][:-7]) + '          ' + str(result[i][1])
        txt = font.render(data, True, (0, 0, 0))
        txtpos = txt.get_rect()
        txtpos.x = 0
        txtpos.y = i * (W // 10)
        texts.append((txt, txtpos))
    return texts


# функция скрытия рейтинга
def hide_rating(texts):
    startbutton.show()
    logo.show()
    rating.show()
    for i in texts:
        i[1].x = -10000
    texts = []
    return texts


# основной цикл игры

sc = pygame.display.set_mode((W, H))
alien = Alien()
pause = Pause()
logo = Logo()
continuebutton = Continuebutton()
restart = Restart()
homebutton = Homebutton()
startbutton = Startbutton()
sprite_group = pygame.sprite.Group()
sprite_group.add(alien)
sprite_group.add(pause)
sprite_group.add(logo)
sprite_group.add(continuebutton)
sprite_group.add(restart)
sprite_group.add(startbutton)
sprite_group.add(homebutton)
background = background1('f')
background2 = background2('f')
clock = pygame.time.Clock()
sprite_group.add(background)
sprite_group.add(background2)
platforms_cords = [(W // 2 - 80, H - 30)]
coin_cords = []
pygame.font.init()
font = pygame.font.Font(None, 36)
text = font.render("Score " + str(alien.coinscounter), True, (0, 0, 0))
textpos = text.get_rect()
textpos.x = W // 2 - 30
textpos.y = 30
rating = Rating()
monsters = []
monsterscords = []
with open('level.txt', 'r') as file:
    file = file.read().split('\n')
    k = len(file) * 50
    for i in range(len(file)):
        for j in range(len(file[i])):
            if file[i][j] == '-':
                platforms_cords.append((j * 80, H - i * 50))
            if file[i][j] == 'k':
                coin_cords.append((j * 80, H - i * 50))
            if file[i][j] == 'f':
                finishline = Finishline((0, H - i * 50))
                finish_cords = (0, H - i * 50)
            if file[i][j] == 'm':
                monster = Monster((j * 80, H - i * 50))
                sprite_group.add(monster)
                monsters.append(monster)
                monsterscords.append((j * 80, H - i * 50))

platforms = []
bullets = []
for cords in platforms_cords:
    platform = Platform(cords)
    sprite_group.add(platform)
    platforms.append(platform)
allsprites = platforms + [finishline] + monsters + [alien]
coins = []
for cords in coin_cords:
    coin = Coin(cords)
    sprite_group.add(coin)
    coins.append(coin)
pygame.event.pump()
allsprites += coins
is_pause = False
run = True
startbutton.show()
logo.show()
rating.show()
runcicle = True
raitwindow = False
texts = []
while runcicle:
    sc.blit(background.image, background.rect)
    sc.blit(background2.image, background2.rect)
    sc.blit(startbutton.image, startbutton.rect)
    sc.blit(logo.image, logo.rect)
    sc.blit(rating.image, rating.rect)
    for txt, txtpos in texts:
        sc.blit(txt, txtpos)
    pygame.display.update()
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        if i.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if startbutton.click_detection(pos[0], pos[1]):
                startbutton.hide()
                logo.hide()
                rating.hide()
                runcicle = False
            if rating.click_detection(pos[0], pos[1]):
                if raitwindow is False:
                    texts = show_rating()
                    raitwindow = True
                else:
                    texts = hide_rating(texts)
                    raitwindow = False
gameoverflag = False
gameover = Gameover()
restartaftergmvr = Restartaftergmovr()
win = Win()
winflag = False
startwindowflag = False
while 1:
    sc.blit(background.image, background.rect)
    sc.blit(background2.image, background2.rect)
    sc.blit(startbutton.image, startbutton.rect)
    sc.blit(logo.image, logo.rect)
    sc.blit(rating.image, rating.rect)
    for txt, txtpos in texts:
        sc.blit(txt, txtpos)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        if i.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if startbutton.click_detection(pos[0], pos[1]):
                startbutton.hide()
                logo.hide()
                rating.hide()
                runcicle = False
                startwindowflag = False
                logo.hide()
                startbutton.hide()
                rating.hide()
                gameoverflag = False
                winflag = False
                restartaftergmvr.hide()
                gameover.hide()
                is_pause = False
                continuebutton.hide()
                restart.hide()
                homebutton.hide()
                for j in range(len(coins)):
                    coins[j].restart(coin_cords[j])
                for j in range(len(platforms)):
                    platforms[j].restart(platforms_cords[j])
                alien.restart()
                finishline.restart(finish_cords)
                textpos.x = W // 2 - 30
                pause.show()
                win.hide()
            if rating.click_detection(pos[0], pos[1]):
                if raitwindow is False:
                    texts = show_rating()
                    raitwindow = True
                else:
                    texts = hide_rating(texts)
                    raitwindow = False
            if continuebutton.click_detection(pos[0], pos[1]):
                is_pause = False
                continuebutton.hide()
                restart.hide()
            if restart.click_detection(pos[0], pos[1]):
                is_pause = False
                continuebutton.hide()
                restart.hide()
                for j in range(len(coins)):
                    coins[j].restart(coin_cords[j])
                for j in range(len(platforms)):
                    platforms[j].restart(platforms_cords[j])
                for j in range(len(monsters)):
                    monsters[j].restart(monsterscords[j])
                alien.restart()
                finishline.restart(finish_cords)
            if pause.click_detection(pos[0], pos[1]):
                is_pause = True
                continuebutton.show()
                restart.show()
                key = pygame.key.get_pressed()
                if key[pygame.K_RIGHT]:
                    alien.move_right()
                if key[pygame.K_LEFT]:
                    alien.move_left()
                for platform in platforms:
                    sc.blit(platform.image, platform.rect)
                for coin in coins:
                    sc.blit(coin.image, coin.rect)
                for monster in monsters:
                    monster.collide(bullets, alien)
                    sc.blit(monster.image, monster.rect)
                sc.blit(finishline.image, finishline.rect)
                sc.blit(alien.image, alien.rect)
                sc.blit(pause.image, pause.rect)
                sc.blit(continuebutton.image, continuebutton.rect)
                sc.blit(restart.image, restart.rect)
                sc.blit(text, textpos)
                sc.blit(homebutton.image, homebutton.rect)
                alien.collide(platforms, coins, finishline)
                alien.update2(allsprites, coins)
                pygame.display.update()
                sprite_group.update()
                sprite_group.draw(sc)
                text = font.render("Score " + str(alien.coinscounter), True, (0, 0, 0))
            if restartaftergmvr.click_detection(pos[0], pos[1]):
                gameoverflag = False
                winflag = False
                restartaftergmvr.hide()
                gameover.hide()
                is_pause = False
                continuebutton.hide()
                restart.hide()
                homebutton.hide()
                for j in range(len(platforms)):
                    platforms[j].restart(platforms_cords[j])
                for j in range(len(coins)):
                    coins[j].restart(coin_cords[j])
                for j in range(len(monsters)):
                    monsters[j].restart(monsterscords[j])
                alien.restart()
                finishline.restart(finish_cords)
                textpos.x = W // 2 - 30
                pause.show()
                win.hide()
            if homebutton.click_detection(pos[0], pos[1]):
                startwindowflag = True
                gameoverflag = False
                winflag = False
                restartaftergmvr.hide()
                gameover.hide()
                is_pause = False
                continuebutton.hide()
                restart.hide()
                homebutton.hide()
                logo.show()
                startbutton.show()
                rating.show()
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE and is_pause is False and gameoverflag is False and winflag is False \
                    and startwindowflag is False:
                bul = Bullet(alien.rect.x, alien.rect.y)
                sprite_group.add(bul)
                bullets.append(bul)
                alien.shooting()
    if is_pause is False and gameoverflag is False and winflag is False and startwindowflag is False:
        if alien.rect.y >= H - alien.rect.height:
            gameoverflag = True
            saveresult()
            for platform in platforms:
                platform.hide()
            for bul in bullets:
                bul.hide()
            for coin in coins:
                coin.hide()
            for monster in monsters:
                monster.collide(bullets, alien)
                monster.hide()
            finishline.hide()
            alien.hide()
            pause.hide()
            continuebutton.hide()
            gameover.show()
            homebutton.show()
            restartaftergmvr.show()
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            alien.move_right()
        if key[pygame.K_LEFT]:
            alien.move_left()
        for platform in platforms:
            sc.blit(platform.image, platform.rect)
        for bul in bullets:
            sc.blit(bul.image, bul.rect)
        for coin in coins:
            sc.blit(coin.image, coin.rect)
        for monster in monsters:
            monster.collide(bullets, alien)
            sc.blit(monster.image, monster.rect)

        sc.blit(finishline.image, finishline.rect)
        sc.blit(alien.image, alien.rect)
        sc.blit(pause.image, pause.rect)
        sc.blit(continuebutton.image, continuebutton.rect)
        sc.blit(text, textpos)
        flag = alien.collide(platforms, coins, finishline)
        alien.update2(allsprites, coins)
        pygame.display.update()
        sprite_group.update()
        sprite_group.draw(sc)
        text = font.render("Score " + str(alien.coinscounter), True, (0, 0, 0))
        sc.blit(gameover.image, gameover.rect)
        sc.blit(restartaftergmvr.image, restartaftergmvr.rect)
        sc.blit(homebutton.image, homebutton.rect)
        sc.blit(win.image, win.rect)
        if flag is True:
            saveresult()
            winflag = True
            for platform in platforms:
                platform.hide()
            for bul in bullets:
                bul.hide()
            for coin in coins:
                coin.hide()
            for monster in monsters:
                monster.collide(bullets, alien)
                monster.hide()
            finishline.hide()
            alien.hide()
            pause.hide()
            continuebutton.hide()
            win.show()
            restartaftergmvr.show()
            for platform in platforms:
                sc.blit(platform.image, platform.rect)
            for bul in bullets:
                sc.blit(bul.image, bul.rect)
            for coin in coins:
                sc.blit(coin.image, coin.rect)
            for monster in monsters:
                monster.collide(bullets, alien)
                sc.blit(monster.image, monster.rect)
            sc.blit(finishline.image, finishline.rect)
            sc.blit(alien.image, alien.rect)
            sc.blit(pause.image, pause.rect)
            sc.blit(continuebutton.image, continuebutton.rect)
            sc.blit(text, textpos)
            pygame.display.update()
            sprite_group.update()
            sprite_group.draw(sc)
            text = font.render("Score: " + str(alien.coinscounter), True, (0, 0, 0))
            sc.blit(gameover.image, gameover.rect)
            sc.blit(restartaftergmvr.image, restartaftergmvr.rect)
            sc.blit(win.image, win.rect)
            sc.blit(homebutton.image, homebutton.rect)
            homebutton.show()
    # if gameoverflag:
    #     sc.blit(gameover.image, gameover.rect)
    #     sc.blit(restartaftergmvr.image, restartaftergmvr.rect)
    #     text = font.render("Score: " + str(alien.coinscounter), True, (0, 0, 0))
    #     sc.blit(text, textpos)
    #     sc.blit(homebutton.image, homebutton.rect)
    #     pygame.display.update()
    # if winflag:
    #     sc.blit(win.image, win.rect)
    #     sc.blit(restartaftergmvr.image, restartaftergmvr.rect)
    #     text = font.render("Score: " + str(alien.coinscounter), True, (0, 0, 0))
    #     sc.blit(text, textpos)
    #     sc.blit(homebutton.image, homebutton.rect)
    #     pygame.display.update()
    # if startwindowflag:
    #     pygame.display.update()
    # clock.tick(30)