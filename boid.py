import random
import math

width, height = 1600, 900
bounce = False

class Boid:
    def __init__(self, w):
        self.r = 10
        self.speed = 4 + random.random() * 2 - 1
        # self.speed = 4
        self.pos = (random.randint(0, width), random.randint(0, height))
        vx = random.random() * self.speed * 2 - self.speed
        vy = math.sqrt(self.speed**2 - vx * vx)
        if random.random() >= 0.5:
            vy = -vy
        self.vel = (vx, vy)
        self.acc = (0, 0)
        self.obj = w.create_oval(
            self.pos[0] - self.r,
            self.pos[1] - self.r,
            self.pos[0] + self.r,
            self.pos[1] + self.r,
            fill="blue",
            outline="white",
            width=4,
        )

    def look(self, flock, w):

        # Move with vel
        self.pos = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])

        if not bounce:
            # Join the walls
            flg = False
            if self.pos[0] <= 0:
                self.pos = (width + self.pos[0], self.pos[1])
                flg = True
            elif self.pos[0] >= width:
                self.pos = (self.pos[0] - width, self.pos[1])
                flg = True
            if self.pos[1] <= 0:
                self.pos = (self.pos[0], height + self.pos[1])
                flg = True
            elif self.pos[1] >= height:
                self.pos = (self.pos[0], self.pos[1] - height)
                flg = True

            if flg:
                w.coords(
                    self.obj,
                    self.pos[0] - self.r,
                    self.pos[1] - self.r,
                    self.pos[0] + self.r,
                    self.pos[1] + self.r,
                )
        else:
            # Bounce off the walls
            if self.pos[0] <= self.r or self.pos[0] + self.r >= width:
                self.vel = (-self.vel[0], self.vel[1])
            if self.pos[1] <= self.r or self.pos[1] + self.r >= height:
                self.vel = (self.vel[0], -self.vel[1])

        # Steering along other close boids
        avgvel, avgpos, avgdis = (0, 0), (0, 0), (0, 0)
        num = 0
        for i in flock:
            if i == self:
                continue
            distance = math.sqrt(
                (self.pos[0] - i.pos[0]) ** 2 + (self.pos[1] - i.pos[1]) ** 2
            )
            if distance < 100:
                avgvel = (avgvel[0] + i.vel[0], avgvel[1] + i.vel[1])
                avgpos = (avgpos[0] + i.pos[0], avgpos[1] + i.pos[1])
                dis = ((self.pos[0] - i.pos[0]), (self.pos[1] - i.pos[1]))
                madis = math.sqrt(dis[0] ** 2 + dis[1] ** 2)
                dis = (dis[0] / madis * 100 / distance, dis[1] / madis * 100 / distance)
                avgdis = (avgdis[0] + dis[0], avgdis[1] + dis[1])
                num += 1
        if num == 0:
            return

        avgvel = (avgvel[0] / num - self.vel[0], avgvel[1] / num - self.vel[1])

        avgpos = (avgpos[0] / num - self.pos[0], avgpos[1] / num - self.pos[0])
        mapos = math.sqrt(avgpos[0] ** 2 + avgpos[1] ** 2)
        avgpos = (avgpos[0] / mapos * 4, avgpos[1] / mapos * 4)

        self.acc = (
            self.acc[0] + avgvel[0] + avgpos[0] + avgdis[0] * 2,
            self.acc[1] + avgvel[1] + avgpos[1] + avgdis[1] * 2,
        )
