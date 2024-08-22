from utils.bbox_area import bbox_area


def object_detection(frame, model):

    results = model(frame)
    bboxes = []
    confs = []

    # Render the results
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                # label = model.names[int(box.cls[0])]
                confidence = box.conf[0].item()

                # if bbox is of person
                if int(box.cls[0]) == 0 and confidence > 0.4:
                    bbox = box.xyxy[0].numpy().astype(int)

                    # if bbox is insignificantly small in area, skip
                    if bbox_area(bbox) < 40000:
                        continue

                    confs.append(confidence)
                    bboxes.append(list(bbox))

                # images with more than 4 people shd be used in image-splitting part and dont get skipped.
                if len(bboxes) == 4:
                    break

    return bboxes, confs
