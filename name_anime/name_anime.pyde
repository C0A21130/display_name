# 四角の線の座標
line_point = []*4 # 目標とする線の座標を設定
line_pos = []*4   # 現在の線の座標を設定
 
# ビル系の座標 
buil_pos = [[-10, 200, 200, 400], [550, 100, 300, 500], [300, 50, 200, 550]] # ビルの位置座標
buil_window_pos=[[30, 210], [340, 70], [600, 150]]                           # ビルの窓の座標
buil_window_colors = []*10
 
# カウンタ類の初期化
counter = 0              # 映像のレイヤーのカウンタ
build_counter=0          # 今ビルが建っているタイミング
build_end_time = 0       # ビルが建ち終わるタイミング
build_window_time = [255, 0] # ビルの窓ができるタイミング
 
def setup(): 
    global line_point ,line_pos, buil_window_colors
    frameRate(60)  # フレームレートを60に設定
    size(800, 600) # 800X600のウィンドウを作成
    line_point = [[40, 40], [width-40, 40], [width-40, height-40], [40, height-40]] # 目標とする線の座標を設定
    line_pos = [[40, 40], [width-40, 40], [width-40, height-40], [40, height-40]]   # 現在の線の座標を設定
    
     
def draw(): 
    global line_pos, counter, build_counter, build_end, build_window_time
    
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
            counter = 1 # 次の映像レイヤーに移動
        line(line_point[0][0], line_point[0][1], line_pos[0][0], line_pos[0][1]) # ０～１に線を引く
        line(line_point[1][0], line_point[1][1], line_pos[1][0], line_pos[1][1]) # １～２に線を引く
        line(line_point[2][0], line_point[2][1], line_pos[2][0], line_pos[2][1]) # ２～３に線を引く
        line(line_point[3][0], line_point[3][1], line_pos[3][0], line_pos[3][1]) # ３～０に線を引く
     
    elif counter==1: # ビルと窓の描写
        background(0)  
        if build_counter==0: 
            build_end = frameCount+160
            build_window_time = [frameCount+180, frameCount+210, frameCount+240]
            build_counter=1 
        elif build_counter==1: # ビル本体の描写
            if frameCount==build_end:
                print("building")
                draw_build(2) 
                build_counter=2 
            else:
                print(frameCount)
                draw_build(1) 
        elif build_counter==2: # 窓の描写
            draw_build(2)
            if frameCount>=build_window_time[2]:
                draw_window(3)
                counter=2  
            elif frameCount>=build_window_time[1]:
                draw_window(2)
            elif frameCount>=build_window_time[0]:
                draw_window(1)
    elif counter==2: # 名前の表示
        print("")          
 
# ビルの描写     
def draw_build(mode): 
    rate =(float(frameCount)-250)/160
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
        print("mode_errer") # 例外処理
    # ３番ビルの左側を削る
    noStroke()
    fill(0)
    rect(550, 100, 100, 100)
 
def change_window_color():
    color_value = int(random(1, 10))
    print(color_value)
    if color_value==1:
        return "#ffff00"
    else:
        return 0
             
# 窓の描写 
def draw_window(mode): 
    if mode==1: # １番ビルに窓を表示
        for i in range(10):
            for n in range(2):
                rect(buil_window_pos[0][0]+100*n, buil_window_pos[0][1]+50*i, 30, 30) # １番ビルに窓を表示
            # ３番ビルの左側を削る
        noStroke()
        fill(0)
        rect(550, 100, 100, 100)
    elif mode==2: # １と３番ビルに窓を表示
        for i in range(10):
            for n in range(2):
                rect(buil_window_pos[0][0]+100*n, buil_window_pos[0][1]+50*i, 30, 30) # １番ビルに窓を表示
                rect(buil_window_pos[2][0]+110*n, buil_window_pos[2][1]+80*i, 40, 40) # ２番ビルに窓を表示  
        noStroke()
        fill(0)
        rect(550, 100, 100, 100)
    elif mode==3: # １と２と３番ビルに窓を表示
        for i in range(10):
            for n in range(2):
                fill(change_window_color())
                rect(buil_window_pos[0][0]+100*n, buil_window_pos[0][1]+50*i, 30, 30) # １番ビルに窓を表示
                fill(change_window_color())
                rect(buil_window_pos[1][0]+100*n, buil_window_pos[1][1]+55*i, 25, 25) # ２番ビルに窓を表示
                fill(change_window_color())
                rect(buil_window_pos[2][0]+110*n, buil_window_pos[2][1]+80*i, 40, 40) # ３番ビルに窓を表示
        noStroke()
        fill(0)
        rect(550, 100, 100, 100)         
    else:
        print("mode_errer") # 例外処理
        
