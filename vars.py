from multiprocessing import Manager

def add(bds):
    global boids
    for boid in bds:
        boids.append(boid)
