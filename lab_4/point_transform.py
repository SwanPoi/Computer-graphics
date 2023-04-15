def point_transform_to_center(points, x_center, y_center):
    for point in points:
        point[0] += x_center
        point[1] += y_center
