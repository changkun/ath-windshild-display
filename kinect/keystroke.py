from pykeyboard import PyKeyboard

KK = PyKeyboard()
ACTIONS = {
    'increase': ['Control', 'Alternate', 'A'],
    'decrease': ['Control', 'Alternate', 'Y']
}


def press_keys(action='increase'):
    KK.press_keys(ACTIONS[action])


# Usage:

# import time
# for _ in range(10):
#     time.sleep(5)
#     press_keys('increase')
