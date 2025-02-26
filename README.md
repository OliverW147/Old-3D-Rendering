![1](https://github.com/OliverW147/Old-3D-Rendering/blob/main/image.png?raw=true)

# Python 3D Engine

A simple 3D engine built in Python using Pygame. This project renders 3D points onto a 2D screen using basic 3D projection math.

## Features
- **Full-Screen Mode:** Runs in full-screen for an immersive experience.
- **3D Projection:** Uses mathematical formulas to project 3D points onto a 2D plane.
- **Real-time Camera Movement:** Move freely in a 3D space using WASD and other controls.
- **Mouse Look:** Adjusts camera orientation based on mouse movement.
- **Dynamic Point Generation:** Generates and filters points based on distance.
- **Basic Shading System:** Calculates shading based on distance from the camera.
- **FPS Display:** Shows the current frames per second.

## Controls
- `W, A, S, D` - Move forward, left, backward, right.
- `H, N, B, M` - Move in North, South, West, East directions.
- `SHIFT` - Move down.
- `SPACE` - Move up.
- `Mouse` - Adjust camera orientation (Yaw).
- `LEFT / RIGHT Arrow` - Rotate camera.
- `9 / 0` - Decrease/Increase render distance.
- `7 / 8` - Decrease/Increase dot size.
- `I / K` - Adjust field of view.
- `G` - Generate 1000 new points.
- `F` - Clear all points.
- `ESC` - Quit.

## Installation & Running
1. **Install Dependencies:**  
   Ensure you have Python installed, then install the required modules:
   ```sh
   pip install pygame pyautogui keyboard
