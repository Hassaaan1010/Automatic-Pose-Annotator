import numpy as np

# import cv2


def bbox1_closer_than_bbox2(bbox1, bbox2, depth_frame):
    x1, y1, x2, y2 = bbox1
    a1, b1, a2, b2 = bbox2
    section1 = depth_frame[y1:y2, x1:x2]
    section2 = depth_frame[b1:b2, a1:a2]
    # smaller average = darker = closer
    return np.average(section1) < np.average(section2) - 10


# test
# dpt = cv2.imread("/home/hassaan/Downloads/multi_people_splitting/images1/17.png")
# coat = np.average(dpt[304:568, 647:751])
# floor = np.average(dpt[293:369, 309:474])
# print(coat, "vs", floor)
# bbox1 = [304, 568, 647, 751]
# bbox2 = [293, 369, 309, 474]
# print(bbox1_closer_than_bbox2(bbox1, bbox2, dpt))
