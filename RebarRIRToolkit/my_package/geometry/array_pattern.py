class ArrayPattern:
    def create_grid_pattern(self, start_point, x_count, y_count, spacing):
        points = []
        for i in range(x_count):
            for j in range(y_count):
                point = (start_point[0] + i * spacing, start_point[1] + j * spacing, start_point[2])
                points.append(point)
        return points