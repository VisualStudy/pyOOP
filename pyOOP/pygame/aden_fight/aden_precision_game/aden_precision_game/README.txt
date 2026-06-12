Aden's Needle Trial
===================

An original precision platformer made with pygame.

Main features
-------------
- Main character "aden" as a pixel character based on the uploaded photo
- 20 stages loaded from text map files
- Enemies: walker slime / shooter drone
- Attack slash, dash, jump, checkpoints, crumble blocks, spikes, goal
- Easy to extend by editing or adding text files in the levels folder

How to run
----------
1. Install Python 3.10+ (or newer)
2. Install pygame:
   python -m pip install pygame
3. Run the game:
   python main.py

Controls
--------
- Move: Left / Right or A / D
- Jump: Z / Space / W / Up
- Dash: Shift or C
- Attack: X or J
- Respawn: R
- Quit: ESC

Map format
----------
Each stage is a text file in the levels folder.
The game automatically loads files named like:
  level_01.txt
  level_02.txt
  ...

Legend
------
. = empty
# = solid block
B = crumble block
^ = spike
P = player start
G = goal
C = checkpoint
E = walker enemy
S = shooter enemy

To add more maps
----------------
1. Copy an existing level file.
2. Rename it, for example level_21.txt
3. Edit the text map with the symbols above.
4. The game will load all level_*.txt files in order.

Notes
-----
- Each text character is 1 tile (32x32 pixels).
- It is recommended to keep all stage lines the same length.
- You can make larger stages than the screen; the camera will follow the player.
