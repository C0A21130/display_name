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
name_point = [[[100,200],[120,300],[145,300],[210,200],[100, 400]], [[250, 200],[250, 360],[280,400],[360,400],[360,200]],
              [[430,200],[430,400],[520,220],[465,290],[430,290],[520, 400]], [[575,220],[645,200],[720,220],[645,400],[580,400],[710, 400]]] # 名前の目標座標：[[Y], [U], [K], [I]]
moon = [[0, 0, 50], [0, 0, 40]]  # 三日月の座標

# 星の座標と移動幅
star_n = 80
stars = [[0]*star_n, [0]*star_n, [0]*star_n, [100]*star_n, [0]*star_n] # 星のxy座標と角度とどこの部分に接触したかを保存
dstars = [1]*star_n      # 星の移動する数を保存
name_hit_count = [-1]*6  # 星が名前の先端についた数を保存
name_hit_counter = [0]*6 # 星をためる数が満タンかそうでないかを保存
 
def setup(): 
    global line_point ,line_pos, buil_window_colors, window1
    frameRate(60)  # フレームレートを60に設定
    size(800, 600) # 800X600のウィンドウを作成
    line_point = [[40, 40], [width-40, 40], [width-40, height-40], [40, height-40]] # 目標とする線の座標を設定
    line_pos = [[40, 40], [width-40, 40], [width-40, height-40], [40, height-40]]   # 現在の線の座標を設定
    set_window() # 窓の座標と色を設定 
    set_stars()  # 星の座標と状態を設定
     
def draw(): 
    global line_pos, counter, build_counter, build_end, window_time, name_counter, eff_start, name_start, name_end
    
    # ビルと窓の描写の映像レイヤー
    if counter==1: # ビルと窓の描写の映像レイヤーであることを感知
        background("#333333") # 夜空の色を設定
        if build_counter==0: # まだ最初の段階であることを感知
            build_end = frameCount+120                                                     # 窓の表示に切り変わる時間の設定
            window_time = [frameCount+130, frameCount+160, frameCount+190, frameCount+270] # ビルを表示し始める時間の設定
            build_counter=1                                                                # ビルと窓の段階へ以降
        elif build_counter==1: # ビル本体の描写の段階であることを感知
            if frameCount==build_end: # 時間が終わりの段階であるかを感知
                draw_build(2)    # ビルを常に描写するモードで描写
                build_counter=2  # 窓の描画の段階に移動
            else:
                draw_build(1)  # ビルを時間によって変位するモードで描写
        elif build_counter==2: # 窓の描写の段階であることを感知
            draw_build(2) # ビルを常に描写するモードで描写
            if frameCount>=window_time[3]:
                draw_window(3) # １と２と３番目のビルに窓を描写 
                counter=2      # 次の映像レイヤーに移動
            elif frameCount>=window_time[2]:
                draw_window(3) # １と２と３番目のビルに窓を描写    
            elif frameCount>=window_time[1]:
                draw_window(2) # １と３番目のビルに窓を描写
            elif frameCount>=window_time[0]:
                draw_window(1) # １番目のビルに窓を描写
        draw_moon() # 月を常に描画する
    
    # 名前を表示する映像レイヤー
    elif counter==2: # 名前を描写する映像レイヤーであることを感知
        background("#333333")  # 夜空の色を設定
        draw_build(2)          # ビルを常に描写
        draw_window(3)         # 窓を常に描写
        draw_moon()            # 月を常に描写
        fill(51, 51, 51, 128)
        rect(0, 0, width, height) # 文字を表示するための背景を描写
        # タイマー類を初期化
        if name_counter==0: 
            eff_start = frameCount+5   # エフェクトがかかるフレームを設定
            name_start = frameCount+80 # 名前を表示するフレームを設定
            name_end = frameCount+120  # 全てが終わるフレームを設定
            name_counter=1             # 次の実際に描写する段階に移動
        # 実際に名前やエフェクトを描写
        elif name_counter==1:
            if frameCount>=name_end: # 終わりの時間になったことを感知
                draw_name() # 名前を描写
                counter=3   # 次の映像レイヤーへ移行
            elif frameCount>=name_start: # 名前の描写の時間になったことを感知
                draw_name() # 時間ごとに下線が変化する名前を描写
            elif frameCount>=eff_start: # 始まりの時間になったことを感知
                draw_eff()   # エフェクトを描写

    # 星と名前を描写する映像レイヤー
    elif counter==3: # 名前と星が描写する映像レイヤーであることを感知
        background("#333333")     # 夜空の色を設定
        draw_build(2)             # ビルを常に表示
        draw_window(3)            # 窓を常に表示
        draw_moon()               # 月を常に表示
        fill(51, 51, 51, 128)   # 背景の色白の透明に設定
        rect(0, 0, width, height) # 文字を表示するための背景を表示
        draw_name()               # 名前を表示
        draw_stars()              # 星を表示
        
 
# ビルの描写を引数で渡されたモードで描写する関数
def draw_build(mode): 
    rate =(float(frameCount)-1)/120 # ビルを表示する割合を設定
    noStroke()
    fill("#eeeeee")
    if mode==1: # ビルを時間変位によって描写するモードであることを感知
        rect(buil_pos[0][0], buil_pos[0][1], buil_pos[0][2], buil_pos[0][3]*rate) 
        rect(buil_pos[1][0], buil_pos[1][1], buil_pos[1][2], buil_pos[1][3]*rate) 
        rect(buil_pos[2][0], buil_pos[2][1], buil_pos[2][2], buil_pos[2][3]*rate)
    elif mode==2: # ビルを常に描写するモードであることを感知
        rect(buil_pos[0][0], buil_pos[0][1], buil_pos[0][2], buil_pos[0][3]) 
        rect(buil_pos[1][0], buil_pos[1][1], buil_pos[1][2], buil_pos[1][3]) 
        rect(buil_pos[2][0], buil_pos[2][1], buil_pos[2][2], buil_pos[2][3]) 
    draw_build_sub() # ３番ビルの左側を削る

# ３番ビルの角を削る関数
def draw_build_sub():
    noStroke()
    fill("#333333")
    rect(550, 100, 100, 100)

# 1/10の確率で窓を点灯させる
def change_window_color():
    color_value = int(random(1, 7)) # 窓の色を変数に設定
    if color_value==1 or color_value==2:
        return "#ffff00" # 窓の色を黄色に設定
    else:
        return "#333333" # 窓の色を黒色に設定

# moon変数で設定された座標に月を描写
def draw_moon():
    global moon
    h = float(hour())   # 今の時間を変数hに代入
    m = float(minute()) # 今の分を変数mに代入
    x = 50+700*(h/24)   # 月のx座標を計算
    y = 40+30*(m/60)    # 月のy座標を計算
    moon[0][0] = x   # 月の光のx座標
    moon[1][0] = x-5 # 月の影のx座標
    moon[0][1] = y   # 月の光のy座標
    moon[1][1] = y-5 # 月の影のy座標
    noStroke()
    fill("#ffff7f")
    ellipse(moon[0][0], moon[0][1], moon[0][2], moon[0][2]) # 月の光の部分を表示
    fill("#333333")
    ellipse(moon[1][0], moon[1][1], moon[1][2], moon[1][2]) # 月の影の部分を表示
    

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
            eff_line_pos[0][1] += 20
        elif eff_line_pos[1][0]<eff_line_point[2][0]: # 最初：左下　目標：右下
            eff_line_pos[1][0] += 10
        elif eff_line_pos[2][1]>eff_line_point[3][1]: # 最初：右下　目標：右上
            eff_line_pos[2][1] -= 20
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
    rect(eff_box_pos[1][0], eff_box_pos[1][1], eff_box_pos[1][2], eff_box_pos[1][3]*rate) # 四角形を描写
    # Iの位置に丸を最大５０個描写
    a=int((frameCount-276)/7) # 丸を表示する列の数をframeによって決めて変数aに設定
    for i in range(5):     # 丸を縦に5個
        for n in range(a): # 横にa個並べる
            ellipse(eff_pos[0]+i*30, eff_pos[1]+n*22, 7, 7) # 丸の描写

# 名前を表示するアニメーション
def draw_name():
    strokeWeight(10)  # 名前の線を10に設定
    stroke("#ffffff") # 名前の色を#ffffffに設定
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
    for i in range(star_n): # 星の数だけ繰り返す
        stars[0][i] = random(15, 780)     # 星の横の座標を設定
        stars[1][i] = random(11, 100)    # 星の縦の座標を設定
 

# 星の描画
def draw_stars():
    global stars, dstars
    noStroke()
    fill("#ffff7f") 
    for i in range(star_n): # 星の数だけ繰り返す 
        if frameCount%2==0: # フレームカウントが偶数の時に実行
            if stars[2][i]<0:
                stars[2][i] += 1
            elif stars[2][i]>0:
                stars[2][i] -= 1
        check_wall(width, height, i) # 壁に衝突したときの処理を実行する関数を実行
        check_touch_name(i)     # 名前の端に衝突したときに処理を実行する関数を実行
        count_name_hit(i)       # 名前の欄に星が蓄えられる数が限界かどうかを感知する関数を実行
        change_stars(i)         # 星の状態によって移動する角度を変更する関数を実行
        stars[0][i] += dstars[i]*cos(radians(stars[2][i]+90)) # 星のx座標の中心を変更
        stars[1][i] += dstars[i]*sin(radians(stars[2][i]+90)) # 星のy座標の中心を変更
        x = [0]*5 # 星の頂点のx座標を初期化
        y = [0]*5 # 星の頂点のy座標を初期化
        for n in range(5):
            x[n]=stars[0][i]+13*cos(radians(72*n+(90+stars[2][i]))) # 星の頂点のx座標を設定
            y[n]=stars[1][i]-13*sin(radians(72*n+(90+stars[2][i]))) # 星の頂点のy座標を設定
        # 星を描く
        beginShape()
        vertex(x[0], y[0]) 
        vertex(x[2], y[2])
        vertex(x[4], y[4])
        vertex(x[1], y[1])
        vertex(x[3], y[3])
        endShape()

# 名前の線の先に当たったことをカウンタに記録する関数
def check_touch_name(i):
    global stars
    if (stars[0][i]>=name_point[0][0][0]-10 and stars[0][i]<=name_point[0][0][0]+10) and (stars[1][i]>=name_point[0][0][1]-5 and stars[1][i]<=name_point[0][0][1]+5) and name_hit_counter[0]==0: # Y1
        stars[3][i]=0
    elif (stars[0][i]>=name_point[0][3][0]-10 and stars[0][i]<=name_point[0][3][0]+10) and (stars[1][i]>=name_point[0][3][1]-7 and stars[1][i]<=name_point[0][3][1]+5) and name_hit_counter[1]==0: # Y2
        stars[3][i]=1
    elif (stars[0][i]>=name_point[1][0][0]-7 and stars[0][i]<=name_point[1][0][0]+7) and (stars[1][i]>=name_point[1][0][1]-5 and stars[1][i]<=name_point[1][0][1]+5) and name_hit_counter[2]==0: # U1
        stars[3][i]=2
    elif (stars[0][i]>=name_point[1][4][0]-7 and stars[0][i]<=name_point[1][4][0]+7) and (stars[1][i]>=name_point[1][4][1]-5 and stars[1][i]<=name_point[1][4][1]+5) and name_hit_counter[3]==0: # U2
        stars[3][i]=3
    elif (stars[0][i]>=name_point[2][0][0]-10 and stars[0][i]<=name_point[2][0][0]+10) and (stars[1][i]>=name_point[2][0][1]-5 and stars[1][i]<=name_point[2][0][1]+5) and name_hit_counter[4]==0: # K1
        stars[3][i]=4
    elif (stars[0][i]>=name_point[2][2][0]-10 and stars[0][i]<=name_point[2][2][0]+10) and (stars[1][i]>=name_point[2][2][1]-5 and stars[1][i]<=name_point[2][2][1]+5) and name_hit_counter[5]==0: # K2
        stars[3][i]=5

# check_name関数で感知された場合移動する角度を変更する関数
def change_stars(i):
    global stars, dstars
    fill("#ffff7f")
    # 星の状態によって角度と停止をif文で仕分けるようにする
    if stars[3][i]==0:
        if stars[1][i]>=name_point[0][1][1]-(name_hit_count[0]*20):
            dstars[i]=0 # 星を停止させる
        else:
            stars[2][i]=-15 # 星の角度を設定
    if stars[3][i]==1: 
        if stars[1][i]>=name_point[0][2][1]-(name_hit_count[1]*20):
            dstars[i]=0 # 星を停止させる
        else:
            stars[2][i] = 30
    if stars[3][i]==2:
        if stars[1][i]>=name_point[1][1][1]-(name_hit_count[2]*20):
            dstars[i]=0 # 星を停止させる
        else:
            stars[2][i] = 0
    if stars[3][i]==3:
        if stars[1][i]>=name_point[1][3][1]-(name_hit_count[3]*20):
            dstars[i]=0 # 星を停止させる
        else:
            stars[2][i] = 0
    if stars[3][i]==4:
        if stars[1][i]>=name_point[2][4][1]-(name_hit_count[4]*20):
            dstars[i]=0 # 星を停止させる
        else:
            stars[2][i] = 0
    if stars[3][i]==5:
        if stars[1][i]>=name_point[2][3][1]-(name_hit_count[5]*20):
            dstars[i]=0 # 星を停止させる
        else:
            stars[2][i] = 40    

# 星同士がぶつかったときに角度を変更する関数
def check_hit(i):
    global stars
    for n in range(i-1, -1, -1):
        r = dist(stars[0][i], stars[1][i], stars[0][n], stars[1][n]) # 星と別の星の距離をrに設定
        if r<=18: # 星同士が衝突したとき星を跳ね返す
            if stars[2][i]>0:
                stars[2][i]+=2.5
            elif stars[2][i]<0:
                stars[2][i]-=2.5
            elif stars[2][i]==0:
                stars[2][i]=180

# 何かものが衝突したときに挙動を変化させる                   
def check_wall(w, h, i):
    check_hit(i)
    harf_ran = int(random(0,2)) # 1/2の乱数を代入
    if stars[0][i]<=10 or stars[0][i]>=w-10: # 壁とぶつかったことを感知
        stars[2][i] = -0.7*stars[2][i] # 0.7の反発係数で星を反射
    if stars[1][i]>h-10 and (stars[0][i]<=w/2-20 or stars[0][i]>=w/2+20): # 中央以外の地面に追加たことを感知
        stars[1][i]=h-10 # 星のy座標を地面の位置に設定
        if stars[0][i]<=w/2-10: # 星が中央より左側なら右へ移動
            stars[0][i] +=1
        elif stars[0][i]>=w/2+10: # 星が中央より右側なら左へ移動
            stars[0][i] -=1
    if stars[1][i]<10: # 天井についたときに下へ落ちていくようにする
        stars[1][i]=10 # 星の座標を天井にする
        if stars[0][i]>w/2: # 中央より左なら角度を-80に設定
            stars[2][i]=-75
        else:               # 中央より右なら角度を80に設定
            stars[2][i]=75
    # 中央についたときに上昇する
    if stars[0][i]>=w/2-20 and stars[0][i]<=w/2+20: 
        stars[1][i]-=2.5           # 星が上昇する
        tran = int(random(5,8))    # 時間の乱数1～3で設定
        aran = int(random(30, 60)) # 角度を変数３０～６０で設定
        if frameCount%(10*tran)==0: # 時間の乱数のタイミングによって時間を設定
            if harf_ran==0:
                stars[2][i]=-90-aran # 右に飛ぶように設定
            else:
                stars[2][i]=90+aran  # 左に飛ぶように設定

# 名前の欄に星が蓄えられる数が限界かどうかを感知する関数
def count_name_hit(i):
    global name_hit_cunt, name_hit_counter
    for j in range(6):
        if stars[4][i]==0 and stars[3][i]==j:
            name_hit_count[j]+=1 # 名前に当たったときに１増やす
            stars[4][i]=1        # 名前に当たったことを記録
        # 蓄えられる数を各段階によって超えたかを感知し超えたなら変数に設定する
        if name_hit_count[0]>4:
            name_hit_counter[0]=1
        if name_hit_count[1]>4:
            name_hit_counter[1]=1
        if name_hit_count[2]>10:
            name_hit_counter[2]=1
        if name_hit_count[3]>13:
            name_hit_counter[3]=1
        if name_hit_count[4]>3:
            name_hit_counter[4]=1
        if name_hit_count[5]>4:
            name_hit_counter[5]=1

# 画面の写真を撮る
def keyPressed():
    global stars
    if key=="p":
        save("report.png")
    if key=="a" and counter==3: # aボタンを押したときに地面から星を打ち上げる
        for i in range(star_n):
            ran = int(random(0,2))
            # 地面から150ピクセルのときに1/2の確立で-180か180の星の角度を変更する
            if ran==0 and stars[1][i]>height-200: 
                stars[2][i]=180  # 星の角度を180に設定する
            elif ran==1 and stars[1][i]>height-200:
                stars[2][i]=-180 # 星の角度を-180に設定する
