from pykeyboard import PyKeyboard

KK = PyKeyboard()
ACTIONS = {
    'increase': ['Control', 'Alternate', 'A'],
    'decrease': ['Control', 'Alternate', 'Y'],
    'level0': ['Control', 'Alternate', '0'],
    'level1': ['Control', 'Alternate', '1'],
    'level2': ['Control', 'Alternate', '2'],
    'level3': ['Control', 'Alternate', '3'],
    'level4': ['Control', 'Alternate', '4'],
    'level5': ['Control', 'Alternate', '5'],
    'level6': ['Control', 'Alternate', '6']
}


def press_keys(action='increase'):
    KK.press_keys(ACTIONS[action])


# Usage:

# import time
# for _ in range(10):
#     time.sleep(5)
#     press_keys('increase')
