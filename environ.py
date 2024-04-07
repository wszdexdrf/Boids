import tkinter
import boid
import math

boid.width = 1920
boid.height = 1080
boid.bounce = False

master = tkinter.Tk()
w = tkinter.Canvas(master, bg='gray15', width=boid.width, height=boid.height)
w.pack()
boids = []
for _ in range(100):
    boids.append(boid.Boid(w))
while True:
    for bd in boids:
        w.move(bd.obj, bd.vel[0], bd.vel[1])
        bd.vel = (bd.vel[0] + bd.acc[0] * 0.1, bd.vel[1] + bd.acc[1] * 0.1)
        magn = math.sqrt(bd.vel[0] ** 2 + bd.vel[1] ** 2)
        bd.vel = (bd.vel[0] / magn * bd.speed, bd.vel[1] / magn * bd.speed)
        bd.acc = (0, 0)
        bd.look(boids, w)
    master.update()
