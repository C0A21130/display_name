# 四角の線の座標
line_point = []*4 
line_pos = []*4 
 
# ビル系の座標 
buil_pos = [[-10, 200, 200, 400], [550, 100, 300, 500], [300, 50, 200, 550]]
buil_window_pos=[[30, 210], [340, 70], [600, 150]]

 
# カウンタ類 
counter = 0 
build_counter=0 
build_end_time = 0 
build_window_end_time = []*3
 
def setup(): 
    global line_point ,line_pos 
    frameRate(60) 
    size(800, 600) 
    line_point = [[40, 40], [width-40, 40], [width-40, height-40], [40, height-40]] 
    line_pos = [[40, 40], [width-40, 40], [width-40, height-40], [40, height-40]] 
     
def draw(): 
    global line_pos, counter, build_counter, build_end, build_window_end
    
    strokeWeight(3) 
    stroke(40) 
    if counter==0 and frameCount%1 == 0:
        background(255)
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
     
    elif counter==1: # ビルと窓の描写
        background(0)  
        if build_counter==0: 
            build_end = frameCount+240
            build_window_end = [frameCount+240, frameCount+270, frameCount+300]
            build_counter=1 
        elif build_counter==1: # ビル本体の描写
            if frameCount==build_end: 
                draw_build(2) 
                build_counter=2 
            else:
                print(frameCount)
                draw_build(1) 
        elif build_counter==2: # 窓の描写
            draw_build(2)
            if frameCount>=build_window_end[2]:
                draw_window(3)
                counter=2  
            elif frameCount>=build_window_end[1]:
                draw_window(2)
            elif frameCount>=build_window_end[0]:
                draw_window(1)
    elif counter==2:
        print("counter=3")          
 
# ビルの描写     
def draw_build(mode): 
    rate =(float(frameCount)-250)/220
    if mode==1: 
        noStroke()
        fill(255)
        rect(buil_pos[0][0], buil_pos[0][1], buil_pos[0][2], buil_pos[0][3]*rate) 
        rect(buil_pos[1][0], buil_pos[1][1], buil_pos[1][2], buil_pos[1][3]*rate) 
        rect(buil_pos[2][0], buil_pos[2][1], buil_pos[2][2], buil_pos[2][3]*rate)
    elif mode==2:
        noStroke()
        fill(255)
        rect(buil_pos[0][0], buil_pos[0][1], buil_pos[0][2], buil_pos[0][3]) 
        rect(buil_pos[1][0], buil_pos[1][1], buil_pos[1][2], buil_pos[1][3]) 
        rect(buil_pos[2][0], buil_pos[2][1], buil_pos[2][2], buil_pos[2][3]) 
    else:
        print("mode_errer")
    noStroke()
    fill(0)
    rect(550, 100, 100, 100)
     
# 窓の描写 
def draw_window(mode): 
    fill(0)
    if mode==1:
        for i in range(10):
            for n in range(2):
                rect(buil_window_pos[0][0]+100*n, buil_window_pos[0][1]+50*i, 30, 30)
    elif mode==2:
        for i in range(10):
            for n in range(2):
                rect(buil_window_pos[0][0]+100*n, buil_window_pos[0][1]+50*i, 30, 30)
                rect(buil_window_pos[2][0]+110*n, buil_window_pos[2][1]+80*i, 40, 40)        
    elif mode==3:
        for i in range(10):
            for n in range(2):
                rect(buil_window_pos[0][0]+100*n, buil_window_pos[0][1]+50*i, 30, 30)
                rect(buil_window_pos[1][0]+100*n, buil_window_pos[1][1]+55*i, 25, 25)
                rect(buil_window_pos[2][0]+110*n, buil_window_pos[2][1]+80*i, 40, 40)            
    else:
        print("mode_errer")
