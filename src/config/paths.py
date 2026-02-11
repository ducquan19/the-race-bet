"""Resource paths for the game."""

import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENT_DIR = os.path.dirname(BASE_DIR)

# Database
DATABASE_PATH = os.path.join(PARENT_DIR, 'database.csv')

# Resources
IMG_DIR = os.path.join(PARENT_DIR, 'img')
SOUND_DIR = os.path.join(PARENT_DIR, 'sound')

# Login screen images
LOGIN_IMG_DIR = os.path.join(IMG_DIR, 'loginscreen')

# Menu images
MENU_IMG_DIR = os.path.join(IMG_DIR, 'menu')

# Face recognition
FACE_CASCADE = os.path.join(PARENT_DIR, 'haarcascade_frontalface_default.xml')
FACEID_DIR = os.path.join(PARENT_DIR, 'faceid')

# History
HISTORY_DIR = os.path.join(PARENT_DIR, 'History')

# Results
RESULTS_DIR = os.path.join(IMG_DIR, 'Results')

# Minigame
MINIGAME_DIR = os.path.join(IMG_DIR, 'minigame')

# Race
RACE_DIR = os.path.join(IMG_DIR, 'race')

# Sounds
SOUND_FILES = {
    'start': os.path.join(SOUND_DIR, 'startgame.mp3'),
    'click': os.path.join(SOUND_DIR, 'mouseclick.mp3'),
    'ingame': os.path.join(SOUND_DIR, 'ingame.mp3'),
    'inrace': os.path.join(SOUND_DIR, 'inrace.mp3'),
    'clap': os.path.join(SOUND_DIR, 'clap.mp3'),
    'item1': os.path.join(SOUND_DIR, 'item1.mp3'),
    'item2': os.path.join(SOUND_DIR, 'item2.mp3'),
    'item3': os.path.join(SOUND_DIR, 'item3.mp3'),
    'item4': os.path.join(SOUND_DIR, 'item4.mp3'),
    'item5': os.path.join(SOUND_DIR, 'item5.mp3'),
}

# Icon
ICON_PATH = os.path.join(MENU_IMG_DIR, 'Car_icon.jpg')
