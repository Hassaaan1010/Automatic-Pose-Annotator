import cv2
import numpy as np


def blur_bbox(bbox, frame):
    x1, y1, x2, y2 = bbox

    # Extract the region of interest (ROI) from the frame
    roi = frame[y1:y2, x1:x2]

    # Apply Gaussian blur to the ROI
    blurred_roi = cv2.GaussianBlur(roi, (11, 11), 0)

    # Replace the original ROI in the frame with the blurred version
    frame[y1:y2, x1:x2] = blurred_roi

    return frame


def blur_instance_segment(mask, frame):
    # Create a blurred version of the entire frame
    blurred_frame = cv2.GaussianBlur(frame, (21, 21), 0)

    # Combine the original frame and the blurred frame using the mask
    # Mask should be a binary mask (same size as the frame) where the instance segment is white (255) and the rest is black (0)
    mask = mask.astype(bool)  # Ensure the mask is a boolean array

    # Apply the mask: keep original frame where mask is False, and use blurred frame where mask is True
    frame[mask] = blurred_frame[mask]

    return frame


# def inpaint_instance_segment(mask, frame):
#     inpainted_frame = cv2.inpaint(
#         frame, mask.astype(np.uint8), inpaintRadius=3, flags=cv2.INPAINT_TELEA
#     )
#     return inpainted_frame
