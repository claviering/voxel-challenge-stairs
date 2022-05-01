from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=2)
scene.set_floor(0, vec3(1))
scene.set_background_color((0.2, 0.4, 1.0))
scene.set_directional_light((1, 1, -1), 0.2, (1,1,1))
z_len = 3
@ti.func
def create_step(y=0, z_start=0):
    for z in range(z_start, z_start + z_len):
        for x in range(10):
            scene.set_voxel(vec3(x, y, z), 1, vec3(1))

@ti.func
def create_cloud(pos, radius, color):
    for I in ti.grouped(
            ti.ndrange((-radius, radius), (-2, 2),
                       (-radius, radius))):
        f = I / radius
        d = vec2(f[0], f[2]).norm()
        prob = max(0, 1 - d)**2
        if ti.random() < prob:
            scene.set_voxel(pos + I, 1, color + (ti.random() - 0.5) * 0.2)

@ti.kernel
def initialize_voxels():
    for i in range(0, 42):
        create_step(i, 63-z_len*(i+1))
    create_cloud(vec3(-20, 10, 20), 10, vec3(1))
    create_cloud(vec3(-10, 20, -10), 15, vec3(0.9, 0.9, 0.9))
    create_cloud(vec3(-20, 30, -40), 18, vec3(0.8, 0.8, 0.8))
    create_cloud(vec3(25, 22, 0), 13, vec3(0.7, 0.7, 0.7))
    create_cloud(vec3(25, 40, -40), 23, vec3(1))
    create_cloud(vec3(10, 6, 45), 8, vec3(1))

initialize_voxels()

scene.finish()