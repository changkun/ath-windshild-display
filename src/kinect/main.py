# import the necessary modules
import freenect
import cv2
import numpy as np
import math
import time
import keystroke


empirical_value = 100


def get_depth():
    array, _ = freenect.sync_get_depth()
    array = array.astype(np.uint8)
    return array


def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)


if __name__ == "__main__":

    # calculate initial environment brightness
    step = 20
    init_bright = 0
    depth = get_depth()
    time.sleep(5)      # five sec for preparation
    depth = get_depth()
    for x in range(0, depth.shape[0], step):
        for y in range(0, depth.shape[1], step):
            init_bright += translate(depth[x][y], 0, 255, 150, -150)

    print('init_bright: ', init_bright)

    last_level = 0
    count = 0
    while True:
        # calculate global brightness
        global_bright = 0
        depth = get_depth()
        brightness_img = np.zeros(depth.shape, np.uint8)
        bright_points_num = (depth.shape[0] / step) * (depth.shape[1] / step)

        for x in range(0, depth.shape[0], step):
            for y in range(0, depth.shape[1], step):
                bright = depth[x][y]
                bright = translate(bright, 0, 255, 150, -150)
                global_bright += bright
                # global_bright += bright / 255.0        # normalization
                cv2.rectangle(brightness_img, (y, x),
                              (y + step / 2, x + step / 2), float(bright), -1)
        # global_bright -= init_bright

        if global_bright < 0:
            global_bright *= -1

        cv2.imshow('brightness image', brightness_img)
        cv2.imshow('depth_image', get_depth())
        cv2.moveWindow('depth_image', 640, 0)

        current_level = int(global_bright / empirical_value)
        print(current_level, last_level, current_level - last_level)

        # print(current_level, last_level, str(int(current_level / 5)))

        if count == 2:
            keystroke.press_keys(
                'level' + str(int(translate(current_level, 300, 1000, 0, 5))))
            # if current_level - last_level == 1:
            #     keystroke.press_keys('increase')
            #     print('increase')
            # elif current_level - last_level == -1:
            #     keystroke.press_keys('decrease')
            #     print('decrease')
            # else:
            #     print('satble')

            count = 0
        else:
            count += 1

        last_level = current_level

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
