# # import the necessary modules
# import freenect
# import cv2
# import numpy as np

# # function to get RGB image from kinect


# def get_video():
#     array, _ = freenect.sync_get_video()
#     #array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
#     return array

# # function to get depth image from kinect


# def get_depth():
#     array, _ = freenect.sync_get_depth()
#     array = array.astype(np.uint8)
#     return array


# if __name__ == "__main__":
#     while 1:
#         # get a frame from RGB camera
#         frame = get_video()
#         # get a frame from depth sensor
#         depth = get_depth()
#         # display RGB image
#         cv2.imshow('RGB image', frame)
#         # display depth image
#         cv2.imshow('Depth image', depth)

#         # quit program when 'esc' key is pressed
#         k = cv2.waitKey(5) & 0xFF
#         if k == 27:
#             break
#     cv2.destroyAllWindows()

import pygame
import numpy as np
import sys
from freenect import sync_get_depth as get_depth

# Check here for details
# https://github.com/OpenKinect/libfreenect/blob/master/examples/glview.c#L350-L402


def make_gamma():
    """
    Create a gamma table
    """
    num_pix = 2048  # there's 2048 different possible depth values
    npf = float(num_pix)
    _gamma = np.empty((num_pix, 3), dtype=np.uint16)
    for i in xrange(num_pix):
        v = i / npf
        v = pow(v, 3) * 6
        pval = int(v * 6 * 256)
        lb = pval & 0xff
        pval >>= 8
        if pval == 0:
            a = np.array([255, 255 - lb, 255 - lb], dtype=np.uint8)
        elif pval == 1:
            a = np.array([255, lb, 0], dtype=np.uint8)
        elif pval == 2:
            a = np.array([255 - lb, lb, 0], dtype=np.uint8)
        elif pval == 3:
            a = np.array([255 - lb, 255, 0], dtype=np.uint8)
        elif pval == 4:
            a = np.array([0, 255 - lb, 255], dtype=np.uint8)
        elif pval == 5:
            a = np.array([0, 0, 255 - lb], dtype=np.uint8)
        else:
            a = np.array([0, 0, 0], dtype=np.uint8)

        _gamma[i] = a
    return _gamma


gamma = make_gamma()


if __name__ == "__main__":
    fpsClock = pygame.time.Clock()
    FPS = 30  # kinect only outputs 30 fps
    disp_size = (640, 480)
    pygame.init()
    screen = pygame.display.set_mode(disp_size)
    font = pygame.font.Font(pygame.font.match_font(
        'Courier'), 32)  # provide your own font
    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                sys.exit()
        fps_text = "FPS: {0:.2f}".format(fpsClock.get_fps())
        # draw the pixels

        # get the depth readinngs from the camera
        depth = np.rot90(get_depth()[0])
        # the colour pixels are the depth readings overlayed onto the gamma
        # table
        pixels = gamma[depth]
        temp_surface = pygame.Surface(disp_size)
        pygame.surfarray.blit_array(temp_surface, pixels)
        pygame.transform.scale(temp_surface, disp_size, screen)
        screen.blit(font.render(fps_text, 1, (255, 255, 255)), (30, 30))
        pygame.display.flip()
        fpsClock.tick(FPS)
