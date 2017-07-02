# import the necessary modules
import freenect
import cv2
import numpy as np
import time
import keystroke


def get_depth():
    array, _ = freenect.sync_get_depth()
    array = array.astype(np.uint8)
    return array


if __name__ == "__main__":
    # calculate initial environment brightness
    step = 10
    init_bright = 0
    depth = get_depth()
    time.sleep(5)      # five sec for preparation
    for x in range(0, depth.shape[0], step):
        for y in range(0, depth.shape[1], step):
            init_bright += depth[x][y] / 255.0

    print('init_bright: ', init_bright)

    last_level = 0
    while True:
        global_bright = 0
        depth = get_depth()
        brightness_img = np.zeros(depth.shape, np.uint8)
        bright_points_num = (depth.shape[0] / step) * (depth.shape[1] / step)

        for x in range(0, depth.shape[0], step):
            for y in range(0, depth.shape[1], step):
                bright = depth[x][y]
                global_bright += bright / 255.0
                cv2.rectangle(brightness_img, (y, x),
                              (y + step / 2, x + step / 2), float(bright), -1)
        global_bright -= init_bright
        # print('global_bright:', global_bright)
        cv2.putText(brightness_img, 'global_bright: ' + str(global_bright),
                    (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))

        cv2.imshow('brightness image', brightness_img)

        current_level = int(global_bright / 100)
        print(current_level, last_level, current_level - last_level)

        if current_level - last_level == 1:
            keystroke.press_keys('increase')
            print('increase')
        elif current_level - last_level == -1:
            keystroke.press_keys('decrease')
            print('decrease')
        else:
            print('satble')

        last_level = current_level

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
