from utils.check_overlap import check_overlap_for_2
from utils.bbox_area import bbox_area
from utils.average_depth import bbox1_closer_than_bbox2


# return depth sections and rgb sections [], []
def split_people_bboxes(depth_frame, rgb_frame, bboxes, confs):

    # 1 person
    if len(bboxes) == 1:
        print("CASE 1")
        # return depthmap of corresponding image as it is into dataset
        return [depth_frame], [rgb_frame]

    # 2 person
    elif len(bboxes) == 2:
        print("CASE 2")
        bbox1, bbox2 = bboxes
        area = check_overlap_for_2(bbox1, bbox2)
        # no overlap
        if area <= 0:
            print("CASE 2.1")
            # sort bboxes to organize by TL corner
            bboxes.sort(key=lambda x: x[0])
            bbox1, bbox2 = bboxes  # dont comment this
            x1, y1, x2, y2 = bbox1
            a1, b1, a2, b2 = bbox2

            # not right, above or below. :. box1 is to the left of box2
            if x2 <= a1:
                print("CASE 2.1.1")
                mid_x = (x2 + a1) // 2

                depth_section1 = depth_frame[:, :mid_x]
                rgb_section1 = rgb_frame[:, :mid_x]

                depth_section2 = depth_frame[:, mid_x:]
                rgb_section2 = rgb_frame[:, mid_x:]

            # box1 is above or below box2
            else:
                print("CASE 2.1.2")
                if y2 >= b1:  # if above
                    print("CASE 2.1.2.1")
                    mid_y = (y2 + b1) // 2

                elif b2 >= y1:  # if below
                    print("CASE 2.1.2.2")
                    mid_y = (b2 + y1) // 2

                depth_section1 = list(depth_frame[:, :mid_y])
                depth_section2 = list(depth_frame[:, mid_y:])

                rgb_section1 = list(rgb_frame[:, :mid_y])
                rgb_section2 = list(rgb_frame[:, mid_y:])

            return [depth_section1, depth_section2], [rgb_section1, rgb_section2]

        # if overlap large
        elif area > 0.15 * bbox_area(bbox1) and area > 0.15 * bbox_area(bbox2):
            print("CASE 2.2")
            x1, y1, x2, y2 = bbox1
            a1, b1, a2, b2 = bbox2
            # if
            if bbox1_closer_than_bbox2(bbox1, bbox2, depth_frame):
                print("CASE 2.2.1")
                depth_section1 = depth_frame[y1:y2, x1:x2]
                rgb_section1 = rgb_frame[y1:y2, x1:x2]

                return [depth_section1], [rgb_section1]

            elif bbox1_closer_than_bbox2(bbox2, bbox1, depth_frame):
                print("CASE 2.2.2")
                depth_section1 = depth_frame[b1:b2, a1:a2]
                rgb_section1 = rgb_frame[b1:b2, a1:a2]

                return [depth_section1], [rgb_section1]

            else:
                print("CASE 2.2.3")
                return [], []

        # else:- overlap small
        else:
            print("CASE 2.3")
            x1, y1, x2, y2 = bbox1
            a1, b1, a2, b2 = bbox2

            depth_section1 = depth_frame[y1:y2, x1:x2]
            depth_section2 = depth_frame[b1:b2, a1:a2]
            rgb_section1 = rgb_frame[y1:y2, x1:x2]
            rgb_section2 = rgb_frame[b1:b2, a1:a2]

            return [depth_section1, depth_section2], [rgb_section1, rgb_section2]

    # 3 person
    elif len(bboxes) == 3:
        print("CASE 3")
        bbox1, bbox2, bbox3 = bboxes

        x1, y1, x2, y2 = bbox1
        a1, b1, a2, b2 = bbox2
        p1, q1, p2, q2 = bbox3

        # size is bbox area
        size1 = bbox_area(bbox1)
        size2 = bbox_area(bbox2)
        size3 = bbox_area(bbox3)

        # result lists
        depth_sections, rgb_sections = [], []

        area12 = check_overlap_for_2(bbox1, bbox2)
        area13 = check_overlap_for_2(bbox1, bbox3)
        area23 = check_overlap_for_2(bbox2, bbox3)

        # if bbox1 has insignificant overlap with others
        if area12 < 0.1 * size1 and area13 < 0.1 * size1:
            print("CASE 3.1")
            depth1 = list(depth_frame[y1:y2, x1:x2])
            rgb1 = list(rgb_frame[y1:y2, x1:x2])

            depth_sections.append(depth1)
            rgb_sections.append(rgb1)

        # if bbox2 has insignificant overlap with others
        if area12 < 0.1 * size2 and area23 < 0.1 * size2:
            print("CASE 3.2")
            depth1 = list(depth_frame[b1:b2, a1:a2])
            rgb1 = list(rgb_frame[b1:b2, a1:a2])

            depth_sections.append(depth1)
            rgb_sections.append(rgb1)

        # if bbox3 has insignificant overlap with others
        if area13 < 0.1 * size3 and area23 < 0.1 * size3:
            print("CASE 3.3")
            depth1 = list(depth_frame[q1:q2, p1:p2])
            rgb1 = list(rgb_frame[q1:q2, p1:p2])

            depth_sections.append(depth1)
            rgb_sections.append(rgb1)
            pass

        return depth_sections, rgb_sections

    elif len(bboxes) == 4:
        print("CASE 4")
        bboxes.sort(key=lambda x: x[0])
        print(bboxes)  # temp
        bbox1, bbox2, bbox3, bbox4 = bboxes

        x1, y1, x2, y2 = bbox1
        a1, b1, a2, b2 = bbox2
        p1, q1, p2, q2 = bbox3
        r1, s1, r2, s2 = bbox4

        # size is bbox area
        size1 = bbox_area(bbox1)
        size2 = bbox_area(bbox2)
        size3 = bbox_area(bbox3)
        size4 = bbox_area(bbox4)

        # result lists
        depth_sections, rgb_sections = [], []

        area12 = check_overlap_for_2(bbox1, bbox2)
        area13 = check_overlap_for_2(bbox1, bbox3)
        area14 = check_overlap_for_2(bbox1, bbox4)

        area23 = check_overlap_for_2(bbox2, bbox3)
        area24 = check_overlap_for_2(bbox2, bbox4)

        area34 = check_overlap_for_2(bbox3, bbox4)
        print(area12, area13, area14, area23, area24, area34)
        # if bbox1 does not hava insignificant overlap with others
        if area12 < 0.1 * size1 and area13 < 0.1 * size1 and area14 < 0.1 * size1:
            print("CASE 4.1")
            depth1 = list(depth_frame[y1:y2, x1:x2])
            rgb1 = list(rgb_frame[y1:y2, x1:x2])
            # and bbox1 is not too small

            depth_sections.append(depth1)
            rgb_sections.append(rgb1)

        # if bbox2 does not hava insignificant overlap with others
        if area12 < 0.1 * size2 and area23 < 0.1 * size2 and area24 < 0.1 * size2:
            print("CASE 4.2")
            depth1 = list(depth_frame[b1:b2, a1:a2])
            rgb1 = list(rgb_frame[b1:b2, a1:a2])

            depth_sections.append(depth1)
            rgb_sections.append(rgb1)

        # if bbox3 does not hava insignificant overlap with others
        if area13 < 0.1 * size3 and area23 < 0.1 * size3 and area34 < 0.1 * size3:
            print("CASE 4.3")
            depth1 = list(depth_frame[q1:q2, p1:p2])
            rgb1 = list(rgb_frame[q1:q2, p1:p2])

            depth_sections.append(depth1)
            rgb_sections.append(rgb1)

        # if bbox3 does not hava insignificant overlap with others
        if area14 < 0.1 * size4 and area24 < 0.1 * size4 and area34 < 0.1 * size4:
            print("CASE 4.4")
            depth1 = list(depth_frame[s1:s2, r1:r2])
            rgb1 = list(rgb_frame[s1:s2, r1:r2])

            depth_sections.append(depth1)
            rgb_sections.append(rgb1)

        return depth_sections, rgb_sections

    else:
        print("CASE 5")
        print(f"else case in box splitting, number of bboxes: {len(bboxes)}")
        return [], []


# import cv2

# rgb_path = "/home/hassaan/Downloads/allFinal/0.png"
# depth_path = "/home/hassaan/Downloads/DPT2/0.png"

# # read image
# rgb_frame = cv2.imread(rgb_path)
# depth_frame = cv2.imread(depth_path)

# bboxes = [[800, 98, 907, 313]]
# confs = ul[tensor(0.8189)]


# print(
#     split_people_bboxes(
#         depth_frame=depth_frame, rgb_frame=rgb_frame, bboxes=bboxes, confs=confs
#     ),
# )
