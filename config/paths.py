import os


__KV_DIR = os.path.join(os.getcwd(), 'kv')

# Screens paths
__SCREENS_DIR = os.path.join(__KV_DIR, 'screens')

BASE_SCREEN = os.path.join(__SCREENS_DIR, 'base_screen.kv')

# Frames paths
__FRAMES_DIR = os.path.join(__KV_DIR, 'frames')

SCROLLED_FRAME = os.path.join(__FRAMES_DIR, 'scrolled_frame.kv')
SELECTION_FRAME = os.path.join(__FRAMES_DIR, 'selection_frame.kv')
BOTTOM_NAVIGATION_ITEMS = os.path.join(__FRAMES_DIR, 'bottom_navigation_items.kv')
LIST_ITEMS = os.path.join(__FRAMES_DIR, 'list_items.kv')

__DIALOGS_DIR = os.path.join(__FRAMES_DIR, 'dialogs')
MODEL_CONTENT_DIALOG = os.path.join(__DIALOGS_DIR, 'model_content.kv')

# Fields paths
__FIELDS_DIR = os.path.join(__KV_DIR, 'fields')

TEXT_INPUT_FIELD = os.path.join(__FIELDS_DIR, 'entry.kv')
SELECTED_LIST_FIELD = os.path.join(__FIELDS_DIR, 'select_list.kv')
SWITCH_FIELD = os.path.join(__FIELDS_DIR, 'switch.kv')
DATE_FIELD = os.path.join(__FIELDS_DIR, 'date.kv')
LABEL_FIELD = os.path.join(__FIELDS_DIR, 'label.kv')

# Widgets paths
__WIDGETS_DIR = os.path.join(__KV_DIR, 'widgets')

BOTTOM_NAVIGATION_WIDGET = os.path.join(__WIDGETS_DIR, 'bottom_navigation.kv')