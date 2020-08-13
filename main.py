import pygame
pygame.init()

win = pygame.display.set_mode((500, 480))
pygame.display.set_caption("First Game")

bg = pygame.image.load('images/bg.jpg')

clock = pygame.time.Clock()

score = 0


class player(object):
    walkRight = [pygame.image.load('images/R1.png'), pygame.image.load('images/R2.png'), pygame.image.load('images/R3.png'),
                 pygame.image.load('images/R4.png'), pygame.image.load('images/R5.png'), pygame.image.load('images/R6.png'),
                 pygame.image.load('images/R7.png'), pygame.image.load('images/R8.png'), pygame.image.load('images/R9.png')]
    walkLeft = [pygame.image.load('images/L1.png'), pygame.image.load('images/L2.png'), pygame.image.load('images/L3.png'),
                pygame.image.load('images/L4.png'), pygame.image.load('images/L5.png'), pygame.image.load('images/L6.png'),
                pygame.image.load('images/L7.png'), pygame.image.load('images/L8.png'), pygame.image.load('images/L9.png')]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.val = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitBox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, w):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                w.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                w.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                w.blit(self.walkRight[0], (self.x, self.y))
            else:
                w.blit(self.walkLeft[0], (self.x, self.y))
        self.hitBox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(w, (255, 0, 0), self.hitBox, 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (250 - (text.get_width() / 2), 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, w):
        pygame.draw.circle(w, self.color, (self.x, self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load('images/R1E.png'), pygame.image.load('images/R2E.png'), pygame.image.load('images/R3E.png'),
                 pygame.image.load('images/R4E.png'), pygame.image.load('images/R5E.png'), pygame.image.load('images/R6E.png'),
                 pygame.image.load('images/R7E.png'), pygame.image.load('images/R8E.png'), pygame.image.load('images/R9E.png'),
                 pygame.image.load('images/R10E.png'), pygame.image.load('images/R11E.png')]
    walkLeft = [pygame.image.load('images/L1E.png'), pygame.image.load('images/L2E.png'), pygame.image.load('images/L3E.png'),
                pygame.image.load('images/L4E.png'), pygame.image.load('images/L5E.png'), pygame.image.load('images/L6E.png'),
                pygame.image.load('images/L7E.png'), pygame.image.load('images/L8E.png'), pygame.image.load('images/L9E.png'),
                pygame.image.load('images/L10E.png'), pygame.image.load('images/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitBox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 9
        self.visible = True

    def draw(self, w):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                w.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                w.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            pygame.draw.rect(w, (255, 0, 0), (self.hitBox[0], self.hitBox[1] - 20, 50, 10))
            pygame.draw.rect(w, (0, 128, 0), (self.hitBox[0], self.hitBox[1] - 20, 50 - (4.75 * (9 - self.health)), 10))
            self.hitBox = (self.x + 17, self.y + 2, 31, 57)
            # pygame.draw.rect(w, (255, 0, 0), self.hitBox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('goblin hit')


def redrawGameWindow():
    win.blit(bg, (0, 0))
    text = font.render('Score ' + str(score), 1, (0, 0, 0))
    win.blit(text, (10, 10))
    man.draw(win)
    goblin.draw(win)
    for b in bullets:
        b.draw(win)
    pygame.display.update()


# main loop
font = pygame.font.SysFont('comicsans', 30, True)
man = player(400, 410, 64, 64)
goblin = enemy(0, 415, 64, 64, 450)
shootLoop = 0
bullets = []
run = True
while run:
    clock.tick(27)

    if goblin.visible:
        if man.hitBox[1] < goblin.hitBox[1] + goblin.hitBox[3] and man.hitBox[1] + man.hitBox[3] > goblin.hitBox[1]:
            if man.hitBox[0] + man.hitBox[2] > goblin.hitBox[0] and man.hitBox[0] < goblin.hitBox[0] + goblin.hitBox[2]:
                man.hit()
                score -= 5
                man = player(400, 410, 64, 64)
                goblin = enemy(0, 415, 64, 64, 450)

    else:
        goblin = enemy(0, 415, 64, 64, 450)

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 5:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if goblin.visible:
            if bullet.y - bullet.radius < goblin.hitBox[1] + goblin.hitBox[3] and bullet.y + bullet.radius > goblin.hitBox[1]:
                if bullet.x + bullet.radius > goblin.hitBox[0] and bullet.x - bullet.radius < goblin.hitBox[0] + goblin.hitBox[2]:
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))

        if 500 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            f = -1
        else:
            f = 1
        if len(bullets) < 10:
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 3, (0, 0, 0), f))
        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > man.val:
        man.x -= man.val
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.val:
        man.x += man.val
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
    if not man.isJump:
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
    redrawGameWindow()

pygame.quit()
