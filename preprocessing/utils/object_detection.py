from .bbox_area import bbox_area
from .average_depth import average_depth_too_low

import cv2
import numpy as np


def object_detection(frame, depth_frame, model, pose_model):
    height, width, _ = frame.shape
    results = model(frame)
    bboxes = []
    confs = []

    # Render the results
    for result in results:
        if result.masks is not None:
            for i, (mask, box) in enumerate(zip(result.masks.data, result.boxes)):
                label = model.names[int(box.cls[0])]
                confidence = box.conf[0]

                if label == "person" and confidence > 0:
                    bbox = box.xyxy[0].numpy().astype(int)  # Keep as NumPy array on CPU

                    if (
                        len(bboxes) <= 4  # less than 5 people in image
                        and bbox_area(bbox) > 35000  # bbox not too small
                        # add condition for when smaller bounding box is inside another bounding box (911.png   )
                        and not average_depth_too_low(
                            bbox, depth_frame
                        )  # bbox not too similar to background
                    ):
                        padding = 3
                        bboxes.append(
                            [
                                max(0, bbox[0] - padding),
                                max(0, bbox[1] - padding),
                                min(bbox[2] + padding, width),
                                min(bbox[3] + padding, height),
                            ]
                        )
                        confs.append(
                            confidence.item()
                        )  # Convert confidence to a Python number

                    else:

                        # Ensure mask is a NumPy array
                        mask = (
                            mask.cpu().numpy()
                        )  # If mask is in tensor format, convert to NumPy

                        # Resize mask to match the frame dimensions
                        mask_resized = cv2.resize(
                            mask, (frame.shape[1], frame.shape[0])
                        )

                        # Inpaint the masked region to make the person undetectable
                        # Create an inpainting mask (should be binary: 0 for background, 255 for object)
                        inpaint_mask = (mask_resized * 255).astype(np.uint8)

                        # Apply inpainting using the Telea or Navier-Stokes method
                        frame = cv2.inpaint(
                            frame,
                            inpaint_mask,
                            inpaintRadius=1,
                            flags=cv2.INPAINT_TELEA,
                        )

    return frame, bboxes, confs  # Frame remains a NumPy array



""" messed up implementation while converting to gpu compliance
# from bbox_area import bbox_area
# from blur_bbox import blur_bbox, blur_instance_segment, inpaint_instance_segment
# from average_depth import average_depth_too_low
# import cv2
# import torch
# import numpy as np


# def object_detection(frame, depth_frame, model):
#     # Ensure the model and tensors are on the GPU
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     frame = torch.from_numpy(frame).to(device)  # Move frame to GPU
#     depth_frame = torch.from_numpy(depth_frame).to(
#         device
#     )  # Move depth frame to GPU if needed

#     results = model(frame)
#     bboxes = []
#     confs = []

#     # Render the results
#     for result in results:
#         if result.masks is not None:
#             for i, (mask, box) in enumerate(zip(result.masks.data, result.boxes)):
#                 label = model.names[int(box.cls[0])]
#                 confidence = box.conf[0]

#                 if label == "person" and confidence > 0:
#                     bbox = (
#                         box.xyxy[0].cpu().numpy().astype(int)
#                     )  # Move to CPU for bbox area calculation

#                     if (
#                         len(bboxes) <= 4  # less than 5 people
#                         and bbox_area(bbox) > 35000  # bbox not too small
#                         and not average_depth_too_low(
#                             bbox, depth_frame.cpu().numpy()
#                         )  # bbox not too similar to background
#                     ):
#                         bboxes.append(bbox)
#                         confs.append(
#                             confidence.item()
#                         )  # Convert confidence to a Python number
#                     else:
#                         # Apply mask blur
#                         mask = mask.float().to(device)  # Ensure the mask is on the GPU

#                         # Resize mask (move to CPU if necessary)
#                         mask_resized = cv2.resize(
#                             mask.cpu().numpy(), (frame.shape[1], frame.shape[0])
#                         )

#                         # Convert back to GPU tensor
#                         mask_resized = torch.from_numpy(mask_resized).to(device)

#                         # Blur the instance segment
#                         frame = blur_instance_segment(
#                             mask_resized.cpu().numpy(), frame.cpu().numpy()
#                         )

#     return (
#         frame.cpu().numpy(),
#         bboxes,
#         confs,
#     )  # Move frame back to CPU and convert to NumPy


# # Optional: Alternate object_detection implementation with blur_bbox()
# # def object_detection(frame, model):
# #     frame = torch.from_numpy(frame).to(device)  # Move frame to GPU
# #     results = model(frame)
# #     bboxes = []
# #     confs = []

# #     # Render the results
# #     for result in results:
# #         if result.boxes is not None:
# #             for box in result.boxes:
# #                 confidence = box.conf[0].item()

# #                 # if bbox is of person
# #                 if int(box.cls[0]) == 0 and confidence > 0.4:
# #                     bbox = box.xyxy[0].cpu().numpy().astype(int)  # Move to CPU

# #                     if len(bboxes) <= 4 and bbox_area(bbox) > 40000:
# #                         bboxes.append(bbox)
# #                         confs.append(confidence)

# #                     else:
# #                         frame = blur_bbox(bbox, frame.cpu().numpy())

# #     return bboxes, confs
"""
