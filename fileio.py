def array_to_csv(filename, array, header=None):
    f = open(filename + ".csv", 'w')
    if header is not None:
        f.write(header + "\n")
    for row in array:
        line = ""
        for column in row:
            line += "{0:.2f}".format(column)
            line += "," if column != row[-1] else ""
        f.write(line + "\n")
    f.close()


def points_to_csv(filename, points, header=None):
    f = open(filename + ".csv", 'w')
    if header is not None:
        f.write(header + "\n")
    for point in points:
        f.write(str(point) + "\n")
    f.close()
