import cv2

import ColorPallet, ImagePanel

ColorPallet.open()
ImagePanel.open()

while True:
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        cv2.imwrite("final_image.jpg",ImagePanel.image)
        cv2.destroyAllWindows()
        break