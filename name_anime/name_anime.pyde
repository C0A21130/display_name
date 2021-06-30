# カウンタやタイミング類の初期化
counter = 1                  # 映像レイヤーのカウンタ
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
name_point = [[[80,200],[110,300],[135,300],[200,200],[80, 400]], [[260, 200],[260, 360],[290,400],[370,400],[370,200]],
              [[430,200],[430,400],[520,220],[465,290],[430,290],[520, 400]], [[575,220],[645,200],[720,220],[645,400],[580,400],[710, 400]]] # 名前の目標座標：[[Y], [U], [K], [I]]
moon = [[0, 0, 50], [0, 0, 40]]  # 三日月の座標：[[光の部分の情報], [影の部分の情報]]

# 星の座標と
stars = [[0]*50, [0]*50, [0]*50, [0]*50]
dstars = [[0]*50, [0]*50]

 
def setup(): 
    global line_point ,line_pos, buil_window_colors, window1
    frameRate(60)  # フレームレートを60に設定
    size(800, 600) # 800X600のウィンドウを作成
    line_point = [[40, 40], [width-40, 40], [width-40, height-40], [40, height-40]] # 目標とする線の座標を設定
    line_pos = [[40, 40], [width-40, 40], [width-40, height-40], [40, height-40]]   # 現在の線の座標を設定
    set_window() # 窓の座標と色を設定 
    set_stars()
     
def draw(): 
    global line_pos, counter, build_counter, build_end, window_time, name_counter, eff_start, name_start, name_end
    
    # ビルと窓の描写の映像レイヤー
    if counter==1: 
        background("#333333") # 夜空の色を設定
        if build_counter==0: 
            build_end = frameCount+120                                                     # 窓の表示に切り変わる時間の設定
            window_time = [frameCount+130, frameCount+160, frameCount+190, frameCount+270] # ビルを表示し始める時間の設定
            build_counter=1 
        elif build_counter==1: # ビル本体の描写
            if frameCount==build_end: 
                draw_build(2) # ビルの終わりを常に表示
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

    # 名前を表示する映像レイヤー
    elif counter==2:
        background("#333333")  # 夜空の色を設定
        draw_build(2)  # ビルを常に表示
        draw_window(3) # 窓を常に表示
        draw_moon()    # 月を常に表示
        fill(0, 128)
        rect(0, 0, width, height) # 文字を表示するための背景を表示
        # タイマー類を初期化
        if name_counter==0: 
            eff_start = frameCount+5   # エフェクトがかかるフレームを設定
            name_start = frameCount+80 # 名前を表示するフレームを設定
            name_end = frameCount+200  # 全てが終わるフレームを設定
            name_counter=1             # 次の実際に描写する段階に移動
        # 実際に名前やエフェクトを描写
        elif name_counter==1:
            if frameCount>=name_end:
                draw_name() # 名前を表示して次のレイヤーへ
                counter=3
            elif frameCount>=name_start:
                draw_name() # 時間ごとに下線が変化する名前を描写
            elif frameCount>=eff_start:
                draw_eff()   # エフェクトを描写

    elif counter==3:
        background("#333333")  # 夜空の色を設定
        draw_build(2)  # ビルを常に表示
        draw_window(3) # 窓を常に表示
        draw_moon()    # 月を常に表示
        fill(0, 128)              # 背景の色白の透明に設定
        rect(0, 0, width, height) # 文字を表示するための背景を表示
        draw_name()  # 名前を表示
        draw_stars() # 星を表示
        
 
# ビルの描写をする関数
def draw_build(mode): 
    rate =(float(frameCount)-1)/120
    noStroke()
    fill("#eeeeee")
    if mode==1: 
        rect(buil_pos[0][0], buil_pos[0][1], buil_pos[0][2], buil_pos[0][3]*rate) 
        rect(buil_pos[1][0], buil_pos[1][1], buil_pos[1][2], buil_pos[1][3]*rate) 
        rect(buil_pos[2][0], buil_pos[2][1], buil_pos[2][2], buil_pos[2][3]*rate)
    elif mode==2:
        rect(buil_pos[0][0], buil_pos[0][1], buil_pos[0][2], buil_pos[0][3]) 
        rect(buil_pos[1][0], buil_pos[1][1], buil_pos[1][2], buil_pos[1][3]) 
        rect(buil_pos[2][0], buil_pos[2][1], buil_pos[2][2], buil_pos[2][3]) 
    else:
        print("mode_errer") # 例外処理
    draw_build_sub() # ３番ビルの左側を削る

# ３番ビルの角を削る
def draw_build_sub():
    noStroke()
    fill("#333333")
    rect(550, 100, 100, 100)

# 1/10の確率で窓を点灯させる
def change_window_color():
    color_value = int(random(1, 7))
    if color_value==1 or color_value==2:
        return "#ffff00" # 窓の色を黄色に設定
    else:
        return "#333333" # 窓の色を黒色に設定

# 月の座標を時間で設定
def set_moon():
    global moon
    h = float(hour())   # 今の時間をhに代入
    m = float(minute()) # 今の分をmに代入
    x = 50+700*(h/24)   # 月のx座標を計算
    y = 40+30*(m/60)    # 月のy座標を計算
    moon[0][0] = x   # 月の光のx座標
    moon[1][0] = x-5 # 月の影のx座標
    moon[0][1] = y   # 月の光のy座標
    moon[1][1] = y-5 # 月の影のy座標
    
# moon変数で設定された座標に月を描写
def draw_moon():
    set_moon()
    noStroke()
    fill("#ffff7f")
    ellipse(moon[0][0], moon[0][1], moon[0][2], moon[0][2])
    fill("#333333")
    ellipse(moon[1][0], moon[1][1], moon[1][2], moon[1][2])
    

# 窓の座標と色をセットする関数
def set_window():
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

# 名前を表示する前のエフェクト        
def draw_eff():
    rate=0 # rateを初期化
    # rate変数を正の数かつ１以下になるように調整
    if (float(frameCount)-276)/60<=0:   # rate変数が負の時に０
        rate=0
    elif (float(frameCount)-276)/60>=1: # rate変数が1以上の時に１
        rate=1
    else:                               # 60フレーム分の今のフレームの割合をrate変数に代入
        rate=(float(frameCount)-276)/60 
    # Yの位置に左から右へ四角形が伸びるアニメーション
    noStroke()
    fill(255)
    rect(eff_box_pos[0][0], eff_box_pos[0][1], eff_box_pos[0][2]*rate, eff_box_pos[0][3])
    # Uの位置に線で四角形を順に描写
    if frameCount%1==0:                               # １フレーム毎に数値を増やす
        if eff_line_pos[0][1]<eff_line_point[1][1]:   # 最初：左上　目標：左下
            eff_line_pos[0][1] += 10
        elif eff_line_pos[1][0]<eff_line_point[2][0]: # 最初：左下　目標：右下
            eff_line_pos[1][0] += 10
        elif eff_line_pos[2][1]>eff_line_point[3][1]: # 最初：右下　目標：右上
            eff_line_pos[2][1] -= 10
        elif eff_line_pos[3][0]>eff_line_point[0][0]: # 最初：右上　目標：左上
            eff_line_pos[3][0] -= 10
        strokeWeight(3)
        stroke(255)
        line(eff_line_point[0][0], eff_line_point[0][1], eff_line_pos[0][0], eff_line_pos[0][1]) # 左の線を描写
        line(eff_line_point[1][0], eff_line_point[1][1], eff_line_pos[1][0], eff_line_pos[1][1]) # 下の線を描写
        line(eff_line_point[2][0], eff_line_point[2][1], eff_line_pos[2][0], eff_line_pos[2][1]) # 右の線を描写
        line(eff_line_point[3][0], eff_line_point[3][1], eff_line_pos[3][0], eff_line_pos[3][1]) # 上の線を描写
    # Kの位置に上から下へ四角形が伸びるアニメーション
    noStroke() # ストロークは無し
    fill(255)  # 色は白
    rect(eff_box_pos[1][0], eff_box_pos[1][1], eff_box_pos[1][2], eff_box_pos[1][3]*rate)
    # Iの位置に丸を最大５０個描写
    a=0 # aを初期化
    if frameCount-276<=6: # 6フレーム事にaの値を増やして描写する丸５個ずつ増やす
        a=1  # aを1に設定
    elif frameCount-276<=12: # 12フレーム
        a=2  # aを2に設定
    elif frameCount-276<=18: # 18フレーム
        a=3  # aを3に設定
    elif frameCount-276<=24: # 24フレーム
        a=4  # aを4に設定
    elif frameCount-276<=30: # 30フレーム
        a=5  # aを5に設定
    elif frameCount-276<=36: # 36フレーム
        a=6  # aを6に設定
    elif frameCount-276<=42: # 42フレーム
        a=7  # aを7に設定
    elif frameCount-276<=48: # 48フレーム
        a=8  # aを8に設定
    elif frameCount-276<=54: # 54フレーム
        a=9  # aを9に設定
    else:                    # 60フレーム
        a=10 # aを10に設定
    for i in range(5):     # 丸を縦に5個
        for n in range(a): # 横にa個並べる
            ellipse(eff_pos[0]+i*30, eff_pos[1]+n*22, 7, 7) # eff_pos：グローバル変数

# 名前を表示するアニメーション
def draw_name():
    strokeWeight(3)
    stroke("#ffffff")
    # Yの描写
    line(name_point[0][0][0], name_point[0][0][1], name_point[0][1][0], name_point[0][1][1])
    line(name_point[0][1][0], name_point[0][1][1], name_point[0][2][0], name_point[0][2][1])
    line(name_point[0][3][0], name_point[0][3][1], name_point[0][4][0], name_point[0][4][1])
    # Uの描写
    line(name_point[1][0][0], name_point[1][0][1], name_point[1][1][0], name_point[1][1][1])
    line(name_point[1][1][0], name_point[1][1][1], name_point[1][2][0], name_point[1][2][1])
    line(name_point[1][2][0], name_point[1][2][1], name_point[1][3][0], name_point[1][3][1])  
    line(name_point[1][3][0], name_point[1][3][1], name_point[1][4][0], name_point[1][4][1])
    # Kの描写
    line(name_point[2][0][0], name_point[2][0][1], name_point[2][1][0], name_point[2][1][1])
    line(name_point[2][2][0], name_point[2][2][1], name_point[2][3][0], name_point[2][3][1])  
    line(name_point[2][3][0], name_point[2][3][1], name_point[2][4][0], name_point[2][4][1])
    line(name_point[2][4][0], name_point[2][4][1], name_point[2][5][0], name_point[2][5][1])
    # Iの描写
    line(name_point[3][0][0], name_point[3][0][1], name_point[3][1][0], name_point[3][1][1])
    line(name_point[3][1][0], name_point[3][1][1], name_point[3][2][0], name_point[3][2][1])
    line(name_point[3][1][0], name_point[3][1][1], name_point[3][3][0], name_point[3][3][1])  
    line(name_point[3][4][0], name_point[3][4][1], name_point[3][5][0], name_point[3][5][1])

# 星に関する配列の初期化
def set_stars():
    global stars, dstars
    for i in range(50):
        xran = int(random(1, 600))
        yran = int(random(1, 100))
        stars[0][i] = 100+xran
        stars[1][i] = yran
        dstars[0][i] = 1 # 星のx座標の移動幅
        dstars[1][i] = 1 # 星のy座標の移動幅

# 星の移動を止める
def stop_star(i):
    global dstars
    dstars[0][i]=0
    dstars[1][i]=0

# 星の描画
def draw_stars():
    global stars, dstars
    noStroke()
    fill("#ffff7f") 
    for i in range(30):
        if frameCount%2==0:
            if stars[2][i]<0:
                stars[2][i] += 1
            elif stars[2][i]>0:
                stars[2][i] -= 1
        if frameCount%1==0:
            check_wall(800, 600, i)
            check_touch_name(i)
        check_hit(i)
        change_stars(i)
        stars[0][i] += dstars[0][i]*cos(radians(90+stars[2][i]))
        stars[1][i] += dstars[1][i]*sin(radians(90+stars[2][i]))
        ellipse(stars[0][i], stars[1][i], 20, 20)

# 名前の線の先に当たったことをカウンタに記録する
def check_touch_name(i):
    global stars
    if (stars[0][i]>=name_point[0][0][0]-5 and stars[0][i]<=name_point[0][0][0]+5) and (stars[1][i]>=name_point[0][0][1]-5 and stars[1][i]<=name_point[0][0][1]+5):
        stars[3][i]=1
        print("Y1")
    elif (stars[0][i]>=name_point[0][3][0]-5 and stars[0][i]<=name_point[0][3][0]+5) and (stars[1][i]>=name_point[0][3][1]-5 and stars[1][i]<=name_point[0][3][1]+5):
        stars[3][i]=2
        print("Y2")
    elif (stars[0][i]>=name_point[1][0][0]-5 and stars[0][i]<=name_point[1][0][0]+5) and (stars[1][i]>=name_point[1][0][1]-5 and stars[1][i]<=name_point[1][0][1]+5):
        stars[3][i]=3
        print("U1")
    elif (stars[0][i]>=name_point[1][4][0]-5 and stars[0][i]<=name_point[1][4][0]+5) and (stars[1][i]>=name_point[1][4][1]-5 and stars[1][i]<=name_point[1][4][1]+5):
        stars[3][i]=4
        print("U2")
    elif (stars[0][i]>=name_point[2][0][0]-5 and stars[0][i]<=name_point[2][0][0]+5) and (stars[1][i]>=name_point[2][0][1]-5 and stars[1][i]<=name_point[2][0][1]+5):
        stars[3][i]=5
        print("K1")
    elif (stars[0][i]>=name_point[2][2][0]-5 and stars[0][i]<=name_point[2][2][0]+5) and (stars[1][i]>=name_point[2][2][1]-5 and stars[1][i]<=name_point[2][2][1]+5):
        stars[3][i]=6
        print("K2")

# check_name関数で感知された場合移動する角度を変更する関数
def change_stars(i):
    global stars
    fill("#ffff7f")
    if stars[3][i]==1 and stars[1][i]>=name_point[0][0][1]:
        if stars[1][i]>=name_point[0][1][1]:
            stop_star(i)
        else:
            stars[2][i] = -25
    elif stars[3][i]==2 and stars[1][i]>=name_point[0][3][1]:
        if stars[1][i]>=name_point[0][2][1]:
            stop_star(i)
        else:
            stars[2][i] = 30
    elif stars[3][i]==3 and stars[1][i]>=name_point[1][0][1]:
        if stars[1][i]>=name_point[1][1][1]:
            stop_star(i)
        else:
            stars[2][i] = 0
    elif stars[3][i]==4 and stars[1][i]>=name_point[1][4][1]:
        if stars[1][i]>=name_point[1][3][1]:
            stop_star(i)
        else:
            stars[2][i] = 0
    elif stars[3][i]==5 and stars[1][i]>=name_point[2][0][1]:
        if stars[1][i]>=name_point[2][4][1]:
            stop_star(i)
        else:
            stars[2][i] = 0
    elif stars[3][i]==6 and stars[1][i]>=name_point[2][2][1]:
        if stars[1][i]>=name_point[2][3][1]:
            stop_star(i)
        else:
            stars[2][i] = 40    

# 星同士がぶつかったときに角度を変更する関数
def check_hit(n):
    global stars
    for i in range(n-1, -1, -1):
        r = dist(stars[0][n], stars[1][n], stars[0][i], stars[1][i])
        if r<19:
            stars[2][i] = int(-0.7*stars[2][i])
            if stars[2][n]==0:
                if stars[1][n]>stars[1][i]:
                    stars[2][n]=0
                elif stars[1][n]<stars[1][i]:
                    stars[2][n]=180
                        
# def check_senter():
    
def check_wall(w, h, i):
    if stars[0][i]<=0 or stars[0][i]>=w:
        stars[2][i] = int(-0.6*stars[2][i])
    elif stars[1][i]>=h and (stars[0][i]<=w/2-20 or stars[0][i]>=w/2+20):
        stars[1][i]=h
        if stars[0][i]<=w/2-10:
            stars[0][i] +=1
        elif stars[0][i]>=w/2+10:
            stars[0][i] -=1
            
    if stars[0][i]>=w/2-20 and stars[0][i]<=w/2+20:
        stars[1][i]-=3
        ran = int(random(1,4))
        aran = int(random(-50, 50)) # 1~3で乱数
        if frameCount%(30*ran)==0:
            if aran==0:
                print(aran)
            else:
                stars[2][i]=180+aran
            
            
