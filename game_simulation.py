import pygame
import random
import math

# An Evolving Ecosystem Game(Simulation)
# From Team 11- DAMN, all rights reserved
size = 60  # boxes per side of grid
pixels = 7  # pixels per side of box

genes = ["p", "q", "r", "s"]


def score(x, y):
    # returns your score
    # x = your move, y = the opponent
    # inputs are 'f' for Fight, 'c' for Cooperate
    if x == 'f':  # you Fight
        if y == 'f':  # they Fight
            return -1
        else:  # they Cooperate
            return 2
    else:  # you Cooperate
        if y == 'f':
            return -2
        else:
            return 1


def breed(a, b):
    r = random.random()
    if (r < 0.33):
        return (a + b) / 2
    elif (r < 0.66):
        return max(a, b)
    elif (r < 0.99):
        return min(a, b)
    else:
        return random.random()


class Agent:
    def choice(self, opp):  # 'f' or 'c'
        A = opp.uniqueId
        if random.random() < self.g['r']:
            # Myopic
            if random.random() < self.g['s']:
                ch = 'c'
            else:
                ch = 'f'
        else:
            # Memorizer
            # if first time for this opponent:
            if (A not in self.prevOutcome):
                self.prevOutcome[A] = random.choice([-2, -1, 1, 2])
                self.prevChoice[A] = random.choice(['f', 'c'])
            if self.prevOutcome[A] > 0:  # won last time
                if random.random() < self.g['p']:
                    ch = self.prevChoice[A]
                else:
                    ch = flip(self.prevChoice[A])
            else:  # lost last time
                if random.random() < self.g['q']:
                    ch = self.prevChoice[A]
                else:
                    ch = flip(self.prevChoice[A])
        self.prevChoice[A] = ch
        return ch

    def opponent(self):
        i = bound(self.i + random.choice([-1, 0, 1]))
        j = bound(self.j + random.choice([-1, 0, 1]))
        if i == self.i and j == self.j:  # cannot fight self
            return self.opponent()  # try again
        else:
            return sim[i][j]

    def battle(self, a):
        ch = self.choice(a)
        ach = a.choice(self)
        s = score(ch, ach)
        self.score += s
        self.prevOutcome[a.uniqueId] = s
        sa = score(ach, ch)
        a.score += sa
        a.prevOutcome[self.uniqueId] = sa

    def update(self):
        a = self.opponent()
        self.battle(a)
        if self.score <= 0:
            self.score = 10
            self.prevChoice = {}
            self.prevOutcome = {}
            b = self.opponent()
            for g in genes:
                self.g[g] = breed(a.g[g], b.g[g])
            self.draw()

    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.uniqueId = len(seq)
        self.score = 10
        self.prevChoice = {}
        self.prevOutcome = {}
        self.g = {}
        for g in genes:
            self.g[g] = random.random()
        self.draw()

    def draw(self):
        x = base + self.i * pixels
        y = base + self.j * pixels
        for g in genes:
            boxes.append([shift(x, y, g), color(self.g[g])])


def flip(ch):
    if ch == 'f':
        return 'c'
    else:
        return 'f'


def bound(x):
    return max(0, min(size - 1, x))


def color(x):
    z = pygame.Color(0, 0, 0, 0)
    z.hsva = [x * 250, 95, 95, 0]
    return z


def draw():
    global boxes
    rlist = []
    for b in boxes:
        R = pygame.Rect(b[0], (pixels, pixels))
        pygame.draw.rect(screen, b[1], R, 0)
        rlist.append(R)
    boxes = []
    pygame.display.update(rlist)


def legend():
    for g in genes:
        text = font.render(g, True, black)
        screen.blit(text, shift(nPix / 4, 0, g))
    pygame.display.flip()


def shift(x, y, g):
    if g == "p":
        return (x, y)
    elif g == "q":
        return (x + gap, y)
    elif g == "r":
        return (x, y + gap)
    else:
        return (x + gap, y + gap)


# initialize graphics window:
pygame.init()
base = 20
gap = int(base + math.ceil(pixels * size * 1.05))
nPix = int(base * 2 + gap + math.ceil(pixels * size))
screen = pygame.display.set_mode([nPix, nPix])
pygame.display.set_caption("An Evolving Ecosystem Game(Simulation)")
white = [255, 255, 255]
black = [0, 0, 0]
screen.fill(white)
pygame.display.flip()
font = pygame.font.Font(None, 25)

# initialize agents:
boxes = []  # only used in 'draw': tracks changed genes
seq = []  # one-dimensional list, permuted each turn
sim = []  # fixed two-dimensional grid for 'opponent' lookup
for i in range(0, size):
    row = []
    sim.append(row)
    for j in range(0, size):
        A = Agent(i, j)
        row.append(A)  # sim[i][j]
        seq.append(A)
legend()
draw()

# main animation loop:
done = False
clock = pygame.time.Clock()
while done == False:
    clock.tick(120)  # max frames per second
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    random.shuffle(seq)
    for a in seq:
        a.update()
    draw()
pygame.quit()

# print summary statistics:
avg = {}
for g in genes:
    avg[g] = 0
for a in seq:
    for g in genes:
        avg[g] += a.g[g]
N = len(seq)
for g in genes:
    print(g + "=" + str(round(100 * avg[g] / N) / 100))
