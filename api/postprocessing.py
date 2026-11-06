"""Landmark selection for the two existing DDH pose models.

The first three keypoints are the unique vertices in the common 4-point
closed-polygon annotation. The fourth keypoint closes the polygon.
"""


def select_current(points):
    """Original vertical-extremes rule, kept for reproducible comparisons."""
    usable = [(int(x), int(y)) for x, y in points if x != 0 and y != 0]
    if len(usable) < 2:
        return None
    usable.sort(key=lambda point: point[1])
    return usable[-1], usable[0]


def select_geometry(points, image_side):
    """Choose the medial vertex and superior lateral vertex of each hip.

    image_side names the image half, not the patient's anatomical laterality.
    This matches the existing polygon labels, but still needs clinician validation.
    """
    if image_side not in ("left", "right"):
        raise ValueError("image_side must be 'left' or 'right'")
    usable = [(float(x), float(y)) for x, y in points[:3] if x != 0 and y != 0]
    if len(usable) != 3:
        return None
    inner_index = (max if image_side == "left" else min)(
        range(3), key=lambda index: usable[index][0]
    )
    outer_indices = [index for index in range(3) if index != inner_index]
    rim_index = min(outer_indices, key=lambda index: usable[index][1])
    return usable[inner_index], usable[rim_index]
