import pygame
from pygame.locals import *
import math
import random
import pyautogui
import keyboard
import time

global points

# Window Initialisation
pygame.init()
screen = pygame.display.set_mode((0, 0), FULLSCREEN)
pygame.display.set_caption("Fullscreen Window")
point_colour = (0, 255, 0)  # Green (RGB values)
font = pygame.font.Font(None, 36)  # Choose a font and size
pygame.mouse.set_visible(False)

# Get Screen Size
info = pygame.display.Info()
centre_w = info.current_w / 2
centre_h = info.current_h / 2
aspect_ratio = info.current_w / info.current_h

# Project 3D point onto 2D plane wikipedia.org/wiki/3D_projection
def project(pp, cp, co, plnp):
    global x, y, z, sx, sy, sz, cx, cy, cz, ex, ey, ez, dx, dy, dz, bx, by, aspect_ratio, shading, render_distance
    x = pp[0] - cp[0]
    y = pp[1] - cp[1]
    z = pp[2] - cp[2]
    if (abs(x) + abs(y) + abs(z)) < render_distance:
        sx = math.sin(co[0])
        sy = math.sin(co[1])
        sz = math.sin(co[2])
        cx = math.cos(co[0])
        cy = math.cos(co[1])
        cz = math.cos(co[2])
        ex = plnp[0]
        ey = plnp[1]
        ez = plnp[2]
        dx = cy*(sz*y+cz*x)-sy*z
        dy = sx*(cy*z+sy*(sz*y+cx*x))+cx*(cz*y-sz*x)
        dz = cx*(cy*z+sy*(sz*y+cz*x))-sx*(cz*y-sz*x)
        bx = (ez/dz)*dx+ex
        by = (ez/dz)*dy+ey
        # NOTE TO MAKE BELOW WORK BETTER (THE CONSTANT OF 3K DOESNT SCALE CORRECTLY)!
        shading = 255 - round(math.sqrt((abs(dx)**2 + abs(dy)**2 + abs(dz)**2))/(9*(render_distance/3000))) # FIX ASAP THIS IS BROKEN
        if shading < 0:
            shading = 0

        if dz < 0:  # Check if point is in front of the camera
            bx = (ez / dz) * dx + ex
            by = (ez / dz) * dy + ey
            # Aspect ratio fix
            if aspect_ratio > 1:
                bx *= aspect_ratio
            else:
                by /= aspect_ratio
            return bx, by
        else:
            # Return a point outside the screen bounds if behind the camera (unless you have a 20k monitor I suppose)
            return "na", "na"
    else:
        return "na", "na"

#sort points from furthest to closest

# Handle Inputs
pygame.mouse.set_pos([centre_w, centre_h])
def handle_inputs():
    global camera_pos, camera_orient, points, filter_points, j, render_distance, dot_size
    keys = pygame.key.get_pressed()
    # Update camera orientation based on mouse movement
    if abs(centre_w - pyautogui.position()[0]) != 0 or abs(centre_h - pyautogui.position()[1]) != 0:
        camera_orient[1] += (centre_w - pyautogui.position()[0])/200  # Yaw
        # camera_orient[0] -= (centre_h - pyautogui.position()[1]) / 200  # PITCH BROKEN
        pygame.mouse.set_pos([centre_w, centre_h])
    # movement
    if keys[K_w]:
        camera_pos[0] += math.sin(camera_orient[1]) * (150/fps)
        camera_pos[2] += math.cos(camera_orient[1]) * (150/fps)
    if keys[K_s]:
        camera_pos[0] -= math.sin(camera_orient[1]) * (150/fps)
        camera_pos[2] -= math.cos(camera_orient[1]) * (150/fps)
    if keys[K_a]:
        camera_pos[0] += math.sin(camera_orient[1] + math.radians(90)) * (150/fps)
        camera_pos[2] += math.cos(camera_orient[1] + math.radians(90)) * (150/fps)
    if keys[K_d]:
        camera_pos[0] -= math.sin(camera_orient[1] + math.radians(90)) * (150/fps)
        camera_pos[2] -= math.cos(camera_orient[1] + math.radians(90)) * (150/fps)
    # movement with bearings NESW
    if keys[K_h]:
        camera_pos[2] -= 1  # Move camera forward (decrease z-coordinate)
    if keys[K_n]:
        camera_pos[2] += 1  # Move camera backward (increase z-coordinate)
    if keys[K_b]:
        camera_pos[0] -= 1  # Move camera left (decrease x-coordinate)
    if keys[K_m]:
        camera_pos[0] += 1  # Move camera right (increase x-coordinate)
    if keys[K_LSHIFT]:
        camera_pos[1] -= 1 * (150/fps)  # Move camera down (decrease y-coordinate)
    if keys[K_SPACE]:
        camera_pos[1] += 1 * (150/fps)  # Move camera up (increase y-coordinate)
    # rotation
    if keys[K_LEFT]:
        camera_orient[0] += 0.001  # Rotate camera left (increase yaw angle)
    if keys[K_RIGHT]:
        camera_orient[0] -= 0.001  # Rotate camera right (decrease yaw angle)
    # plane debug
    if keys[K_i]:
        plane_pos[2] -= 1  # Move camera forward (decrease z-coordinate)
    if keys[K_k]:
        plane_pos[2] += 1  # Move camera backward (increase z-coordinate)
    if keys[K_9]:
        render_distance -= 500  # Move camera forward (decrease z-coordinate)
        filter_points = filter_points_by_distance(points, camera_pos, render_distance)
        # make async
        time.sleep(0.2)
    if keys[K_0]:
        render_distance += 500  # Move camera forward (decrease z-coordinate)
        filter_points = filter_points_by_distance(points, camera_pos, render_distance)
        # make async
        time.sleep(0.2)
    if keys[K_7]:
        if dot_size > 1:
            dot_size -= 1  # Move camera forward (decrease z-coordinate)
            time.sleep(0.1)
    if keys[K_8]:
        dot_size += 1  # Move camera forward (decrease z-coordinate)
        time.sleep(0.1)
    if keys[K_f]:
        points = []
        filter_points = []

    # point gen
    if keys[K_g]:
        i = 0
        while i < 1000:
            points.append([random.randrange(-10000, 10000), random.randrange(-10000, 10000), random.randrange(-10000, 10000)])
            i += 1
        filter_points = filter_points_by_distance(points, camera_pos, render_distance)
    j -= 0.8  * (150/fps)
    if j > 750:
        j = 0
        filter_points = filter_points_by_distance(points, camera_pos, render_distance)

# the 3D position of points to be projected.
points = []
i = 0
while i < 2000:
    points.append([random.randrange(-1500, 1500), random.randrange(-1500, 1500), random.randrange(-1500, 1500)])
    i += 1
# camera_pos: the 3D position of a point C representing the camera.
camera_pos = [0, 0, 300]
# camera_orient: the orientation of the camera (represented by Tait–Bryan angles).
camera_orient = [0, 0.001, 0]
# plane_pos: the display surface's position relative to the camera pinhole C.
plane_pos = [0, 0, -300]

dot_size = 1
# fps
last_time = time.time()
frame_times = []

j = 0

render_distance = 3000
# MAKE THIS ASYNCED
def filter_points_by_distance(points, camera_pos, max_distance):
    fp = []
    for point in points:
        distance = math.sqrt(
            (point[0] - camera_pos[0]) ** 2 + (point[1] - camera_pos[1]) ** 2 + (point[2] - camera_pos[2]) ** 2)
        if distance <= max_distance:
            fp.append(point)

    sp = sorted(fp, key=lambda p: math.sqrt((p[0] - camera_pos[0]) ** 2 + (p[1] - camera_pos[1]) ** 2 + (p[2] - camera_pos[2]) ** 2), reverse=True)

    return sp

for _ in range(1000):
    radius = 200
    theta = random.uniform(0, 2 * math.pi)
    phi = random.uniform(0, math.pi)

    # Convert spherical coordinates to Cartesian coordinates
    x = radius * math.sin(phi) * math.cos(theta)
    y = radius * math.sin(phi) * math.sin(theta)
    z = radius * math.cos(phi)
    points.append([x, y, z])

filter_points = filter_points_by_distance(points, camera_pos, 3000)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
    screen.fill((0, 0, 0))
    # Project 3d point onto 3d plane
    for point in filter_points:
        point_x, point_y = project(point, camera_pos, camera_orient, plane_pos)
        if point_x != "na":
            pygame.draw.circle(screen, (0, shading, 0), (centre_w + point_x, centre_h + point_y), dot_size)
    # Render Variables
    screen.blit(font.render("position: " + str(round(camera_pos[0])) + ' ' + str(round(camera_pos[1])) + ' ' + str(round(camera_pos[2])), True, point_colour), (10, 10))
    screen.blit(font.render("orientation: " + str(camera_orient), True, point_colour), (10, 35))
    screen.blit(font.render("frustum near plane: " + str(plane_pos), True, point_colour), (10, 60))
    screen.blit(font.render("render distance: " + str(render_distance), True, point_colour), (10, 135))
    screen.blit(font.render("shading: " + str(shading), True, point_colour), (10, 85))
    screen.blit(font.render("distance: " + str(round(abs(x + y + z))), True, point_colour), (10, 110))
    screen.blit(font.render("time until next dot resort: " + str(round(750 - j)), True, point_colour), (10, 160))
    screen.blit(font.render("dot size: " + str(dot_size), True, point_colour), (10, 185))
    # fps
    frame_times.append(last_time - time.time())
    if len(frame_times) > 200:
        frame_times = frame_times[-200:]
    fps = 1.0 / (sum(frame_times) / len(frame_times))
    screen.blit(font.render("fps: " + str(round(abs(fps))), True, point_colour), (10, 210))
    last_time = time.time()

    screen.blit(font.render("Press G to add some more dots!", True, point_colour), (10, info.current_h - 75))
    screen.blit(font.render(("Controls: WASD, HBNM, SHIFT, SPACE, Mouse, 9 and 0 change render distance (dont go above 3k), K and I change fov, 7 and 8 change dot size"), True, point_colour), (10, info.current_h - 50))
    screen.blit(font.render("x: " + str(x), True, point_colour), (screen.get_width() - 200, 10))
    screen.blit(font.render("y: " + str(y), True, point_colour), (screen.get_width() - 200, 40))
    screen.blit(font.render("z: " + str(z), True, point_colour), (screen.get_width() - 200, 70))
    screen.blit(font.render("sx: " + str(sx), True, point_colour), (screen.get_width() - 200, 100))
    screen.blit(font.render("sy: " + str(sy), True, point_colour), (screen.get_width() - 200, 130))
    screen.blit(font.render("sz: " + str(sz), True, point_colour), (screen.get_width() - 200, 160))
    screen.blit(font.render("cx: " + str(cx), True, point_colour), (screen.get_width() - 200, 190))
    screen.blit(font.render("cy: " + str(cy), True, point_colour), (screen.get_width() - 200, 220))
    screen.blit(font.render("cz: " + str(cz), True, point_colour), (screen.get_width() - 200, 250))
    screen.blit(font.render("ex: " + str(ex), True, point_colour), (screen.get_width() - 200, 280))
    screen.blit(font.render("ey: " + str(ey), True, point_colour), (screen.get_width() - 200, 310))
    screen.blit(font.render("ez: " + str(ez), True, point_colour), (screen.get_width() - 200, 340))
    screen.blit(font.render("dx: " + str(dx), True, point_colour), (screen.get_width() - 200, 370))
    screen.blit(font.render("dy: " + str(dy), True, point_colour), (screen.get_width() - 200, 400))
    screen.blit(font.render("dz: " + str(dz), True, point_colour), (screen.get_width() - 200, 430))
    screen.blit(font.render("bx: " + str(bx), True, point_colour), (screen.get_width() - 200, 460))
    screen.blit(font.render("by: " + str(by), True, point_colour), (screen.get_width() - 200, 490))

    # Render
    pygame.display.update()
    handle_inputs()
pygame.quit()
