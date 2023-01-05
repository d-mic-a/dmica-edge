
def map_point(obj_pt,screen_pt,space_pt):
    #space_pt = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    #screen_pt = [[0,0],[0,0],[0,0],[0,0]]
    #obj_pt = [0,0]
    x, y, z = obj_pt[0], obj_pt[1], 0
    x1, y1, z1 = screen_pt[0][0], screen_pt[0][1], 0
    x2, y2, z2 = screen_pt[1][0], screen_pt[1][1], 0
    x3, y3, z3 = screen_pt[2][0], screen_pt[2][1], 0
    x4, y4, z4 = screen_pt[3][0], screen_pt[3][1], 0
    x5, y5, z5 = space_pt[0][0], space_pt[0][1], space_pt[0][2]
    x6, y6, z6 = space_pt[1][0], space_pt[1][1], space_pt[1][2]
    x7, y7, z7 = space_pt[2][0], space_pt[2][1], space_pt[2][2]
    x8, y8, z8 = space_pt[3][0], space_pt[3][1], space_pt[3][2]
    

    points1 = [(x1, y1, z1), (x2, y2, z2), (x3, y3, z3), (x4, y4, z4)]
    points2 = [(x5, y5, z5), (x6, y6, z6), (x7, y7, z7), (x8, y8, z8)]

    avg1 = [(x1 + x2 + x3 + x4) / 4, (y1 + y2 + y3 + y4) / 4, (z1 + z2 + z3 + z4) / 4]
    avg2 = [(x5 + x6 + x7 + x8) / 4, (y5 + y6 + y7 + y8) / 4, (z5 + z6 + z7 + z8) / 4]

    dist1 = [((i - x1) ** 2 + (j - y1) ** 2 + (k - z1) ** 2) ** 0.5 for (i, j, k) in points1]
    dist2 = [((i - x5) ** 2 + (j - y5) ** 2 + (k - z5) ** 2) ** 0.5 for (i, j, k) in points2]

    total_dist1 = sum(dist1)
    total_dist2 = sum(dist2)

    factor = total_dist2 / total_dist1

    mapped_point = [(x - avg1[0]) * factor + avg2[0], (y - avg1[1]) * factor + avg2[1], (z - avg1[2]) * factor + avg2[2]]

    return mapped_point


if __name__ == '__main__':
    obj_pt = [-5.0, 5.86]
    screen_pt = [[-12,0.6], [-4.08,0.59], [-4, 6.65], [-12,7]]
    space_pt = [[0.72,-4.39,0.8], [14.65,-14,0.8], [19.64,0.53,0.8], [14.6,4.25,0.8]]
    x = map_point(obj_pt, screen_pt,space_pt)
    print(x)