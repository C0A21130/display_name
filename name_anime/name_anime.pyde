# 四角の線
line_point = []*4
line_pos = []*4

# ビルの座標
buil_pos = [[-10, 200, 200, 400], [550, 100, 300, 500], [300, 50, 200, 550]]

# カウンタ類
counter = 0
build_counter=0
build_end_time = 0

def setup():
    global line_point ,line_pos
    frameRate(60)
    size(800, 600)
    line_point = [[40, 40], [width-40, 40], [width-40, height-40], [40, height-40]]
    line_pos = [[40, 40], [width-40, 40], [width-40, height-40], [40, height-40]]
    
def draw():
    global line_pos, counter, build_counter, frame,build_end_time
    background(254)
    strokeWeight(3)
    stroke(40)
    frame = frameCount
    if counter==0 and frameCount%1 == 0:
        for i in range(100):
            n = sin(i+frameCount//5)*30
            ellipse(0+i*10, 300+n, 3, 3)
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
    
    elif counter==1:
        if build_counter==0:
            build_end_time = frameCount+300
            build_counter=1
        elif build_counter==1:
            if frameCount==build_end_time:
                draw_build(2)
                build_counter=2
            else:
                draw_build(1)
        elif build_counter==2:
            draw_build(2)
            draw_window()
            counter==2

# ビルの描写    
def draw_build(mode):
    rate =(float(frameCount)-250)/300
    print(frameCount)
    fill(100)
    if mode==1:
        rect(buil_pos[0][0], buil_pos[0][1], buil_pos[0][2], buil_pos[0][3]*rate)
        rect(buil_pos[1][0], buil_pos[1][1], buil_pos[1][2], buil_pos[1][3]*rate)
        rect(buil_pos[2][0], buil_pos[2][1], buil_pos[2][2], buil_pos[2][3]*rate)
    elif mode==2:
        rect(buil_pos[0][0], buil_pos[0][1], buil_pos[0][2], buil_pos[0][3])
        rect(buil_pos[1][0], buil_pos[1][1], buil_pos[1][2], buil_pos[1][3])
        rect(buil_pos[2][0], buil_pos[2][1], buil_pos[2][2], buil_pos[2][3])
    
# 窓の描写
def draw_window():
    print("win")
    
