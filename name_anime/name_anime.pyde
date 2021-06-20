# 四角の線
line_point = []*4
line_pos = []*4

counter = 0

def setup():
    global line_point ,line_pos
    frameRate(120)
    size(800, 600)
    line_point = [[40, 40], [width-40, 40], [width-40, height-40], [40, height-40]]
    line_pos = [[40, 40], [width-40, 40], [width-40, height-40], [40, height-40]]
    
def draw():
    global line_pos, counter
    background(254)
    strokeWeight(3)
    stroke(40)
    if frameCount%1 == 0:
        if line_pos[0][0]<=line_point[1][0]-10:
            line_pos[0][0] += 10
        elif line_pos[1][1]<=line_point[2][1]-10:
            line_pos[1][1] += 10
        elif line_pos[2][0]>=line_point[3][0]+10:
            line_pos[2][0] -= 10
        elif line_pos[3][1]>=line_point[0][1]+10:
            line_pos[3][1] -= 10
        else:
            counter = 1
    line(line_point[0][0], line_point[0][1], line_pos[0][0], line_pos[0][1])
    line(line_point[1][0], line_point[1][1], line_pos[1][0], line_pos[1][1])
    line(line_point[2][0], line_point[2][1], line_pos[2][0], line_pos[2][1])
    line(line_point[3][0], line_point[3][1], line_pos[3][0], line_pos[3][1])
    if counter == 1 and frameCounter:
        
