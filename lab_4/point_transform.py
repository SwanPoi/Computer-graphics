def circle_point_transform(circle_points, x_center, y_center):
    for point in circle_points:
        point[0] += x_center
        point[1] += y_center
