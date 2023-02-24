import os


__KV_DIR = os.path.join(os.getcwd(), 'kv')

# Screens paths
__SCREENS_DIR = os.path.join(__KV_DIR, 'screens')

BASE_SCREEN = os.path.join(__SCREENS_DIR, 'base_screen.kv')

# Frames paths
__FRAMES_DIR = os.path.join(__KV_DIR, 'frames')

SCROLLED_FRAME = os.path.join(__FRAMES_DIR, 'scrolled_frame.kv')

# Fields paths
__FIELDS_DIR = os.path.join(__KV_DIR, 'fields')

TEXT_INPUT_FIELD = os.path.join(__FIELDS_DIR, 'entry.kv')
SELECTED_LIST_FIELD = os.path.join(__FIELDS_DIR, 'select_list.kv')
SWITCH_FIELD = os.path.join(__FIELDS_DIR, 'switch.kv')