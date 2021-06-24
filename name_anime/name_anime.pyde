# カウンタやタイミング類の初期化
counter = 0                  # 映像レイヤーのカウンタ
build_counter=0              # 今ビルが建っているカウンタ
name_counter = 0             # 名前が出来上がるカウンタ
build_end_time = 0           # ビルが建ち終わるタイミングを保存
build_window_time = [0]*4    # ビルの窓ができるタイミングを保存
eff_start = 0                # エフェクトのかかるタイミングを保存
name_start = 0               # 名前のアニメーションがかかるタイミングを保存
name_end = 0                 # 名前のアニメーションが終わるタイミングを保存

# 四角の線の座標
line_point = [0]*4 # 目標とする線の座標を初期化
line_pos = [0]*4   # 現在の線の座標を初期化

# ビル類の座標 
buil_pos = [[-10, 200, 200, 400], [300, 150, 200, 450], [550, 100, 300, 500]]           # ビルの座標：[[１番ビル][２番ビル][３番ビル]]
window_pos=[[30, 210], [340, 170], [600, 150]]                                          # ビルの窓の座標：[[１番ビルの窓][２番ビルの窓][３番ビルの窓]]
window_init_pos=[[30, 210], [340, 170], [600, 150]]                                     # ビルの窓の座標：[[１番ビルの窓][２番ビルの窓][３番ビルの窓]]
window = [[[0]*2, [0]*20, [""]*20], [[0]*2, [0]*20, [""]*20], [[0]*2, [0]*20, [""]*20]] # 窓の座標と色を保存：[[x],[y],[色]]            

# 名前のアニメーションの座標系
eff_line_point = [[240,200],[240,400],[390,400],[390,200]] # 2番目のエフェクトの目標の座標
eff_line_pos = [[240,200],[240,400],[390,400],[390,200]]   # 2番目のエフェクトの現在の座標
eff_box_pos = [[80,200,150,200], [410,200,150, 200]]       # 1と3番目のエフェクトの座標
eff_pos = [570,200]                                        # 4番目のエフェクトの座標
name_point = [[[80,200],[125,300],[155,300],[230,200],[80, 400]], [[240, 200],[240, 360],[270,400],[390,400],[390,200]],
              [[410,200],[410,400],[530,200],[465,290],[410,290],[560, 400]], [[575,200],[645,200],[720,220],[645,400],[570,400],[720, 400]]] # 名前の目標座標：[[Y], [U], [K], [I]]
under_line = [50, 400, 750, 400] # 名前の下に線を引く
moon = [[0, 0, 40], [0, 0, 30]]  # 三日月の座標：[[光], [影]]

 
def setup(): 
    global line_point ,line_pos, buil_window_colors, window1
    frameRate(60)  # フレームレートを60に設定
    size(800, 600) # 800X600のウィンドウを作成
    line_point = [[40, 40], [width-40, 40], [width-40, height-40], [40, height-40]] # 目標とする線の座標を設定
    line_pos = [[40, 40], [width-40, 40], [width-40, height-40], [40, height-40]]   # 現在の線の座標を設定
    window_set() # 窓の座標と色を設定
    moon_set()   # 月の座標を設定  
     
def draw(): 
    global line_pos, counter, build_counter, build_end, window_time, name_counter, eff_start, name_start, name_end
    
    if counter==0 and frameCount%1 == 0: # 1フレームレートごとに描画
        strokeWeight(3) 
        stroke(40)
        background(255)
        for i in range(100): 
            n = sin(i+frameCount//5)*30 
            ellipse(0+i*10, 300+n, 3, 3)
        # 最初から目標まで線が引かれてなければ値を増やす
        if line_pos[0][0]<=line_point[1][0]-10:   # 最初：左上　目標：右上
            line_pos[0][0] += 10 
        elif line_pos[1][1]<=line_point[2][1]-10: # 最初：右上　目標：右下
            line_pos[1][1] += 10 
        elif line_pos[2][0]>=line_point[3][0]+10: # 最初：右下　目標：左下
            line_pos[2][0] -= 10 
        elif line_pos[3][1]>=line_point[0][1]+10: # 最初：左下　目標：左上
            line_pos[3][1] -= 10 
        else: 
            counter = 1 # 次の映像レイヤーに移動
        # 線を伸ばして四角を作る
        line(line_point[0][0], line_point[0][1], line_pos[0][0], line_pos[0][1]) # 上の線
        line(line_point[1][0], line_point[1][1], line_pos[1][0], line_pos[1][1]) # 右の線
        line(line_point[2][0], line_point[2][1], line_pos[2][0], line_pos[2][1]) # 下の線
        line(line_point[3][0], line_point[3][1], line_pos[3][0], line_pos[3][1]) # 左の線
     
    elif counter==1: # ビルと窓の描写の映像レイヤー
        background(0)  
        if build_counter==0: 
            build_end = frameCount+120                                                     # 窓の表示に切り変わる時間の設定
            window_time = [frameCount+130, frameCount+160, frameCount+190, frameCount+270] # ビルを表示し始める時間の設定
            build_counter=1 
        elif build_counter==1: # ビル本体の描写
            if frameCount==build_end:
                draw_build(2) 
                build_counter=2 
            else:
                draw_build(1) 
        elif build_counter==2: # 窓の描写
            draw_build(2)
            if frameCount>=window_time[3]:
                draw_window(3) # １と２と３番目のビルに窓を描写 
                counter=2      # 次の映像レイヤーに移動
            elif frameCount>=window_time[2]:
                draw_window(3) # １と２と３番目のビルに窓を描写    
            elif frameCount>=window_time[1]:
                draw_window(2) # １と３番目のビルに窓を描写
            elif frameCount>=window_time[0]:
                draw_window(1) # １番目のビルに窓を描写
        draw_moon()

    # 名前を表示するアニメーション
    elif counter==2:
        background(0)  # 背景を常に初期化
        draw_build(2)  # ビルを常に建てる
        draw_window(3) # 窓を常に表示
        fill(0, 128)
        rect(0, 0, width, height) # 文字を表示するための背景を表示
        if name_counter==0: # タイマー類を初期化
            eff_start = frameCount+5
            name_start = frameCount+70
            name_end = frameCount+600
            name_counter=1
        elif name_counter==1:
            # if frameCount>=name_end:
            #     draw_name(2)
            #     print("not_def")
            if frameCount>=name_start:
                draw_name(1)
            elif frameCount>=eff_start:
                draw_eff()
            else:
                draw_name(2)
            
 
# ビルの描写をする関数
def draw_build(mode): 
    rate =(float(frameCount)-250)/120
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
    draw_build_sub() # ３番ビルの左側を削る

# ３番ビルの角を削る
def draw_build_sub():
    noStroke()
    fill(0)
    rect(550, 100, 100, 100)

# 1/10の確率で窓を点灯させる
def change_window_color():
    color_value = int(random(1, 5))
    if color_value==1 or color_value==2:
        return "#ffff00" # 窓の色を黄色に設定
    else:
        return 0         # 窓の色を黒色に設定

def moon_set():
    global moon
    now = hour()
    a = (now/24)*PI+PI/4
    moon[0][0] = 300*sin(a)
    moon[1][0] = (300-5)*sin(a)
    moon[0][1] = 50*cos(a)
    moon[1][1] = (50-5)*cos(a)
    
def draw_moon():
    noStroke()
    fill(255)
    ellipse(moon[0][0], moon[0][1], moon[0][2], moon[0][2])
    fill(0)
    ellipse(moon[1][0], moon[1][1], moon[1][2], moon[1][2])
    

# 窓の座標と色をセットする関数
def window_set():
    global window1
    noStroke()
    for i in range(20):
        if i<=9:
            window[0][1][i] = window_init_pos[0][1]+50*i # １番ビルの左側のy座標を設定
            window[1][1][i] = window_init_pos[1][1]+55*i # ２番ビルの左側のy座標を設定
            window[2][1][i] = window_init_pos[2][1]+80*i # ３番ビルの左側のy座標を設定
        else:
            window[0][1][i] = window_init_pos[0][1]+50*(i-10) # １番ビルの右側のy座標を設定
            window[1][1][i] = window_init_pos[1][1]+55*(i-10) # ２番ビルの右側のy座標を設定
            window[2][1][i] = window_init_pos[2][1]+80*(i-10) # ３番ビルの右側のy座標を設定
        window[0][2][i] = change_window_color() # １番ビルの色を決定
        window[1][2][i] = change_window_color() # ２番ビルの色を決定
        window[2][2][i] = change_window_color() # ３番ビルの色を決定
    for n in range(2):
        window[0][0][n] = window_init_pos[0][0]+100*n # １番ビルのx座標を設定
        window[1][0][n] = window_init_pos[1][0]+100*n # ２番ビルのx座標を設定
        window[2][0][n] = window_init_pos[2][0]+110*n # ３番ビルのx座標を設定
        
# 窓の描写 
def draw_window(mode):
    if mode==1: # １番ビルに窓を表示
        for i in range(20):
            a = 0 if i<=9 else 1
            fill(window[0][2][i])
            rect(window[0][0][a], window[0][1][i], 30, 30) # １番ビルに窓を表示
    elif mode==2: # １と３番ビルに窓を表示
        for i in range(20):
            a = 0 if i<=9 else 1 
            fill(window[0][2][i])
            rect(window[0][0][a], window[0][1][i], 30, 30) # １番ビルに窓を表示
            fill(window[2][2][i])
            rect(window[2][0][a], window[2][1][i], 40, 40) # ３番ビルに窓を表示  
    elif mode==3: # １と２と３番ビルに窓を表示
        for i in range(20):
            a = 0 if i<=9 else 1
            fill(window[0][2][i])
            rect(window[0][0][a], window[0][1][i], 30, 30) # １番ビルに窓を表示
            fill(window[1][2][i])
            rect(window[1][0][a], window[1][1][i], 25, 25) # ２番ビルに窓を表示
            fill(window[2][2][i])
            rect(window[2][0][a], window[2][1][i], 40, 40) # ３番ビルに窓を表示      
    else:
        print("mode_errer") # 例外処理
    draw_build_sub() # ３番ビルの左側を削る
        
def draw_eff():
    rate=0
    if (float(frameCount)-525)/60<=0:
        rate=0
    elif (float(frameCount)-525)/60>=1:
        rate=1
    else:
        rate=(float(frameCount)-525)/60
    noStroke()
    fill(255)
    rect(eff_box_pos[0][0], eff_box_pos[0][1], eff_box_pos[0][2]*rate, eff_box_pos[0][3])
    if frameCount%1==0:
        if eff_line_pos[0][1]<eff_line_point[1][1]:   # 最初：左上　目標：右上
            eff_line_pos[0][1] += 20
        elif eff_line_pos[1][0]<eff_line_point[2][0]: # 最初：右上　目標：右下
            eff_line_pos[1][0] += 15
        elif eff_line_pos[2][1]>eff_line_point[3][1]: # 最初：右下　目標：左下
            eff_line_pos[2][1] -= 20 
        elif eff_line_pos[3][0]>eff_line_point[0][0]: # 最初：左下　目標：左上
            eff_line_pos[3][0] -= 15
        strokeWeight(3)
        stroke(255)
        line(eff_line_point[0][0], eff_line_point[0][1], eff_line_pos[0][0], eff_line_pos[0][1]) # 上の線
        line(eff_line_point[1][0], eff_line_point[1][1], eff_line_pos[1][0], eff_line_pos[1][1]) # 右の線
        line(eff_line_point[2][0], eff_line_point[2][1], eff_line_pos[2][0], eff_line_pos[2][1]) # 下の線
        line(eff_line_point[3][0], eff_line_point[3][1], eff_line_pos[3][0], eff_line_pos[3][1]) # 左の線
    noStroke()
    fill(255)
    rect(eff_box_pos[1][0], eff_box_pos[1][1], eff_box_pos[1][2], eff_box_pos[1][3]*rate)
    a=0
    if frameCount-525<=6:
        a=1
    elif frameCount-525<=12:
        a=2
    elif frameCount-525<=18:
        a=3
    elif frameCount-525<=24:
        a=4
    elif frameCount-525<=30:
        a=5
    elif frameCount-525<=36:
        a=6
    elif frameCount-525<=42:
        a=7
    elif frameCount-525<=48:
        a=8
    elif frameCount-525<=54:
        a=9
    else:
        a=10
    for i in range(5):
        for n in range(a):
            ellipse(eff_pos[0]+i*30, eff_pos[1]+n*22, 7, 7)

def draw_name(mode):
    rate=0
    if float(frameCount-580)/60<0:
        rate=0
    elif float(frameCount-580)/60>=1:
        rate=1
    else:
        rate=float(frameCount-580)/60

    if mode ==1:
        strokeWeight(3)
        stroke(255)
        # Yの作成
        line(name_point[0][0][0], name_point[0][0][1], name_point[0][1][0], name_point[0][1][1])
        line(name_point[0][1][0], name_point[0][1][1], name_point[0][2][0], name_point[0][2][1])
        line(name_point[0][3][0], name_point[0][3][1], name_point[0][4][0], name_point[0][4][1])
        # Uの作成
        line(name_point[1][0][0], name_point[1][0][1], name_point[1][1][0], name_point[1][1][1])
        line(name_point[1][1][0], name_point[1][1][1], name_point[1][2][0], name_point[1][2][1])
        line(name_point[1][2][0], name_point[1][2][1], name_point[1][3][0], name_point[1][3][1])  
        line(name_point[1][3][0], name_point[1][3][1], name_point[1][4][0], name_point[1][4][1])
        # Kの作成
        line(name_point[2][0][0], name_point[2][0][1], name_point[2][1][0], name_point[2][1][1])
        line(name_point[2][2][0], name_point[2][2][1], name_point[2][3][0], name_point[2][3][1])  
        line(name_point[2][3][0], name_point[2][3][1], name_point[2][4][0], name_point[2][4][1])
        line(name_point[2][4][0], name_point[2][4][1], name_point[2][5][0], name_point[2][5][1])
        # Iの作成
        line(name_point[3][0][0], name_point[3][0][1], name_point[3][1][0], name_point[3][1][1])
        line(name_point[3][1][0], name_point[3][1][1], name_point[3][2][0], name_point[3][2][1])
        line(name_point[3][1][0], name_point[3][1][1], name_point[3][3][0], name_point[3][3][1])  
        line(name_point[3][4][0], name_point[3][4][1], name_point[3][5][0], name_point[3][5][1])
        # 下線
        line(under_line[0], under_line[1], under_line[2]*rate, under_line[3])
    elif mode==2:
        line(name_point[0][0][0], name_point[0][0][1], name_point[0][1][0], name_point[0][1][1])
        line(name_point[0][1][0], name_point[0][1][1], name_point[0][2][0], name_point[0][2][1])
        line(name_point[0][3][0], name_point[0][3][1], name_point[0][4][0], name_point[0][4][1])
        
        line(name_point[1][0][0], name_point[1][0][1], name_point[1][1][0], name_point[1][1][1])
        line(name_point[1][1][0], name_point[1][1][1], name_point[1][2][0], name_point[1][2][1])
        line(name_point[1][2][0], name_point[1][2][1], name_point[1][3][0], name_point[1][3][1])  
        line(name_point[1][3][0], name_point[1][3][1], name_point[1][4][0], name_point[1][4][1])
        
        line(name_point[2][0][0], name_point[2][0][1], name_point[2][1][0], name_point[2][1][1])
        line(name_point[2][2][0], name_point[2][2][1], name_point[2][3][0], name_point[2][3][1])  
        line(name_point[2][3][0], name_point[2][3][1], name_point[2][4][0], name_point[2][4][1])
        line(name_point[2][4][0], name_point[2][4][1], name_point[2][5][0], name_point[2][5][1])
        
        line(name_point[3][0][0], name_point[3][0][1], name_point[3][1][0], name_point[3][1][1])
        line(name_point[3][1][0], name_point[3][1][1], name_point[3][2][0], name_point[3][2][1])
        line(name_point[3][1][0], name_point[3][1][1], name_point[3][3][0], name_point[3][3][1])  
        line(name_point[3][4][0], name_point[3][4][1], name_point[3][5][0], name_point[3][5][1])
        line(under_line[0], under_line[1], under_line[2], under_line[3])
    else:
        print("mode_errer")
    
