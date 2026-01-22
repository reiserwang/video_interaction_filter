def bboxes_overlap(bb1, bb2):
    """
    Check if two bounding boxes overlap.
    bb format: [x1, y1, x2, y2]
    """
    # Check if one rectangle is to the left of the other
    if bb1[2] < bb2[0] or bb2[2] < bb1[0]:
        return False
    # Check if one rectangle is above the other
    if bb1[3] < bb2[1] or bb2[3] < bb1[1]:
        return False
    return True

def get_bbox_center(bbox):
    """
    Returns (x, y) center of the bounding box.
    """
    x_center = int((bbox[0] + bbox[2]) / 2)
    y_center = int((bbox[1] + bbox[3]) / 2)
    return (x_center, y_center)
