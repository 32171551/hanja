##폴더여는 버튼 삭제 >> 프로그램 실행시 자동으로 폴더 호출
import os
import tkinter
from tkinter import *
import tkinter.font
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import shutil
from pathlib import Path

# 가장 기본적인 경로들
base_path = str(f'{os.path.dirname(__file__)}')  # 파이썬 프로그램이 저장되어 있는 함수의 위치 호출
title_path = base_path + "/title"  # 타이틀의 경로
subtitle_path = base_path + "/subtitle"  # 서브 타이틀의 경로

#title/subtitle 폴더 존재 여부 확인
if os.path.isdir(title_path) == False:
    messagebox.showwarning("warning", "title 폴더가 존재하지 않습니다.")
    exit()
if os.path.isdir(subtitle_path) == False:
    messagebox.showwarning("warning", "subtitle 폴더가 존재하지 않습니다.")
    exit()
tmp_path = base_path + '/tmp'

root = Tk()

# 앱의 이름
root.title("hanja")
width = 900
height = 900
root.geometry('{}x{}+{}+{}'.format(width, height,50,50))  # 켰을때의 화면 크기

# create all of the main containers
# 유니코드가 뜰 부분, 제일 상단
top_frame_width = width * 0.986
top_frame_height = height * 0.1
top_frame = Frame(root, width=top_frame_width, height=top_frame_height,
                  pady=3)  # 이 부분에 색을 넣고 싶은 경우 folder_label의 background 색상을 같이 지정해줘야 함
top_frame.grid(row=0, sticky="ew")  # grid로 위치 지정
folder_label = Label(top_frame, text="name", padx=10, pady=4)  # 유니코드, folder_name: 불러온 폴더의 이름이 뜨게 됨
folder_label.grid(row=0, columnspan=3)  # grid 지정

# 이미지를 불러올 컨데이너, 제일 중앙에 위치
image_frame_width = width * 0.7
image_frame_height = height * 0.9
image_frame = Frame(root, width=image_frame_width, height=image_frame_height, pady=1, background="black")
image_frame.grid(row=1, sticky="nsew")


# main container의 빈공간을 채우기 위한 함수
root.grid_rowconfigure(1, weight=1)  # row 번호
root.grid_columnconfigure(0, weight=1)  # column 번호
# 이미지 컨테이너의 빈공간
image_frame.grid_rowconfigure(0, weight=1)
image_frame.grid_columnconfigure(1, weight=1)

# 버튼이 오는 위치
button_left_width = width * 0.34
button_left_height = height * 0.38
button_left = Frame(image_frame, width=button_left_width, height=button_left_height)
button_left.grid(row=0, column=0, sticky="ns")

button_top_width = width * 0.34
button_top_height = height * 0.38
button_left_top = Frame(button_left, width=button_left_width, height=button_left_height)
button_left_top.grid(row=0, column=0, sticky="n")


button_btm_width = width * 0.34
button_btm_height = height * 0.38
button_left_btm = Frame(button_left, width=button_left_width, height=button_left_height)
button_left_btm.grid(row=1, column=0, sticky="s")

# 이미지가 들어가는 위치
image_mid_width = width * 0.347
image_mid_height = height * 0.38
image_mid = Frame(image_frame, bg='white', width=image_mid_width, height=image_mid_height, padx=3, pady=3)
image_mid.grid(row=0, column=1, sticky="nsew")

#페이지 넘김 버튼이 위치하는 중앙 우측
page_mid_width = width * 0.05
page_mid_height = height * 0.38
page_mid = Frame(image_frame, width=page_mid_width, height=page_mid_height, padx=3, pady=3)
page_mid.grid(row=0, column=2, sticky="nsew")


# 불러올 폴더 선택
def open_folder():
    global f, f_len
    global dir_path
    global call_folder, first_folder

    # dir_path = filedialog.askdirectory(parent=root, initialdir="./title", title='select directory')  # title폴더를 기준 경로로 선택
    first_folder = os.listdir(title_path)
    if len(first_folder) == 0:
        messagebox.showwarning("warning","title 폴더가 비어있습니다.")
    if len(os.listdir(subtitle_path)) == 0:
        messagebox.showwarning("warning","subtitle 폴더가 비어있습니다.")

    call_folder = title_path + "/" + first_folder[0]
    print(first_folder[0])
    print(call_folder)
    dir_path = call_folder
    f = os.listdir(dir_path)
    print(f)
    # 폴더 안에 들어있는 파일의 개수
    f_len = len(f)
    path_name = dir_path.split('/')[-1]
    count_folder(path_name)
    tmp(path_name)
    # lbox()


#화면 재정렬
def window():
    t_path = base_path + '/tmp'
    uni = os.listdir(t_path)
    path_name = uni[0]
    print("uni", path_name)
    tmp_path = t_path + '/' + path_name
    print("t", tmp_path)
    image_label(tmp_path, path_name)

# 임시 폴더 생성
def tmp(path_name):
    check_tmp_path = base_path + '/tmp'
    path_name = path_name
    print("tmp path name", path_name)
    call_folder = title_path + '/' + path_name
    # print("tmp path name", path_name)
    if os.path.isdir(check_tmp_path) == False:
        os.mkdir(check_tmp_path)
    if len(os.listdir(check_tmp_path)) == 0: #tmp 폴더가 비어있는 경우
        tmp_path = base_path + '/tmp/' + path_name
        if not os.path.exists(tmp_path): #tmp폴더에 유니코드 폴더가 없는 경우 생성
            os.mkdir(tmp_path)
        # copy_tree(call_folder, tmp_path)
        call_img_list = os.listdir(call_folder)
        for img in call_img_list:
            move_img = os.path.join(call_folder, img)
            dst = os.path.join(tmp_path, img)
            shutil.copy(move_img, dst)
    else:
        shutil.rmtree(check_tmp_path, ignore_errors=True)
        tmp_path = base_path + '/tmp/' + path_name
        shutil.copytree(call_folder, tmp_path)
    f = os.listdir(tmp_path)
    image_label(tmp_path, path_name)

#프레임을 비워줌(1>5>3의 순으로 이미지 개수가 변화해도 기존에 남아있던 이미지는 전부 사라짐)
def clearFrame():
    # destroy all widgets from frame
    for widget in image_mid.winfo_children():
        widget.destroy()
    # this will clear frame and frame will be empty if you want to hide the empty panel then
    image_mid.pack_forget()

# NEXT 버튼을 눌렀을 때 작용
def next_folder():
    global first_folder
    clearFrame() #화면에 떠있는 기존의 이미지 삭제
    t_path = base_path + '/tmp'
    if os.path.isdir(t_path) == False: #임시 폴더가 없는 경우 생성해줌(폴더 불러오기 버튼을 사용하지 않았을 때 필요함)
        os.mkdir(t_path)
    t_list = os.listdir(t_path)
    print("t_list", t_list)
    if len(t_list) == 0:  # open folder을 누르지 않은 상태로 next를 눌렀을 경우
        open_folder()  # open folder 함수에 연결
        # count_folder(path_name)
    else: #tmp 폴더 내부에 데이터가 남아있을 경우
        print("---------------------------------------------------------------")
        global f_len
        move_image() #tmp폴더에 저장되어 있는 내용을 전부 done폴더로 이동시켜줌
        path_list = os.listdir(t_path)  # 기존 tmp폴더에 들어있던 폴더 이름 가지고 오기
        path_name = path_list[0]
        for a in range(len(first_folder)):
            # print("first_folder", first_folder)
            if path_name == first_folder[a]:  # tmp 파일의 유니코드와 동일한 이름의 폴더를 title폴더에서 찾으면
                path_name = first_folder[a + 1]  # 다음 title 폴더의 이름으로 변경
                break
            else:
                a += 1
        # print("next path name", path_name)
        count_folder(path_name) #리스트 박스에서 진행사항을 확인하기 위해 필요
        tmp(path_name)  # 다음 폴더로 이동&임시 폴더 생성을 위해 tmp 호출
    #
    # count_folder(path_name)
    # move_image()

# done 버튼을 누르면 작동. 이미 작업이 끝난 폴더를 전부 삭제
def done():
    global first_folder, title_path
    t_path = base_path + '/tmp' #tmp의 경로를 불러옴
    title_path = title_path  # title의 경로 불러옴
    tt_list = os.listdir(t_path)
    tmp_uni = tt_list[0]
    first_folder = first_folder
    title_len = len(first_folder)  # title 폴더안에 들어가있는 한자 폴더의 개수 확인
    for i in range(title_len):  # 일단은 반복문
        if tmp_uni == first_folder[i]: #마지막으로 작업한 폴더의 내용
            print("작업이 종료될 폴더", first_folder[i])
            del_file = title_path + "/" + first_folder[i] #작업이 완료 되어 삭제할 title 폴더 찾기
            shutil.rmtree(del_file) #title 폴더에서 작업 완료 폴더 삭제
            break #작업이 완료된 폴더를 전부 삭제했으므로 해당 루프문을 종료
        else:  #마지막으로 작업한 폴더가 아니라면
            print("작업이 완료된 폴더", first_folder[i])
            del_file = title_path + "/" + first_folder[i]
            shutil.rmtree(del_file) #title 폴더에서 해당 폴더 삭제
    print("남은 title_path", os.listdir(title_path))
    move_image() #title 폴더의 삭제를 완료 했으므로 확인을 위해 남겨두었던 tmp폴더의 내용을 done 폴더로 이동
    t_folder_path = t_path + '/' + tmp_uni
    shutil.rmtree(t_folder_path) #tmp폴더 안의 내용을 삭제
    listbox.delete(0, END) #리스트 박스 초기화
    clearFrame() #중앙 이미지 프레임 초기화

#tmp 폴더 안에 들어있는 이미지들을 전부 done 폴더로 이동동
def move_image():
    done_path = base_path + '/done'
    if os.path.isdir(done_path) == False: #done 폴더가 없다면 폴더 생성
        os.mkdir("done")
    t_list = os.listdir(tmp_path)
    t_folder_path = base_path + '/tmp/' + t_list[0]
    get_files = os.listdir(t_folder_path)
    for g in get_files: #tmp폴더 안의 내용을 done 폴더 안으로 이동
        shutil.copy(t_folder_path + '/' + g, done_path) #작업이 끝나면 해당 함수를 가지고 있는 다른 함수에서 tmp폴더를 삭제 예정(여기서 하지 않아도 됨)

# subtitle 폴더와 연동 될 수 있도록 한다 > 이미지가 선택되면 화면의 이미지 또한 바뀌어야 함
def change_image(i, tmp_path, path_name):  # 작업은 임시 폴더에서 진행
    global f
    tmp_path = tmp_path
    f = os.listdir(tmp_path)
    path_name = path_name
    print("이미지 이동", path_name)
    # 수정을 원하는 이미지 파일 이동
    sub_path = subtitle_path + '/' + path_name
    if os.path.isdir(sub_path) == False: #subtitle 폴더가 비어있거나 아예 없는 경우 경고문 발생
        messagebox.showwarning(title="경고", message="subtitle이 존재하지 않습니다.\n폴더를 확인해주세요.")
    else:
        move_path = base_path + "/wrong"
        if os.path.isdir(move_path) == False:  # wrong 폴더가 없는 경우 생성
            os.mkdir("wrong")
        img_path = filedialog.askopenfilename(parent=root, initialdir='./subtitle/' + path_name, title='파일선택', filetypes=(
            ('jpg files', '*.jpg'), ('png files', '*.png'), ('all files', '*.*')))
        if img_path == '': #이미지를 선택하지 않은 경우 아무런 작업도 하지 않는다
            print("이미지 선택 하지않음")
        else: #이미지를 선택한 경우
            shutil.move(os.path.join(tmp_path, f[i]), os.path.join(move_path, f[i])) #title 폴더에 있는 이미지 이동
            shutil.move(img_path, tmp_path)# 선택한 이미지 subtitle에서 가지고 옴
            f = os.listdir(tmp_path)
            image_label(tmp_path, path_name) #변경된 내용의 이미지를 화면 출력

#title 이미지 삭제
def delete_image(i, tmp_path, path_name):  # 작업은 임시 폴더에서 진행
    global f
    tmp_path = tmp_path
    path_name = path_name
    # if os.path.isdir(tmp_path) == False:
    #     os.mkdir("tmp")
    f = os.listdir(tmp_path)
    move_path = base_path + "/wrong"  # 잘못되었다고 판단되는 한자를 이동할 폴더
    if os.path.isdir(move_path) == False: #wrong 폴더가 없는 경우 생성
        os.mkdir("wrong")
    # shutil.move(tmp_path + '/' + f[i], move_path)
    shutil.move(os.path.join(tmp_path, f[i]), os.path.join(move_path, f[i])) #삭제할 이미지를 wrong 폴더로 이동, 변경과 다르게 이미지를 교체하지는 않음
    f = os.listdir(tmp_path)
    print(f)
    # clearFrame()
    image_label(tmp_path, path_name)

def tmp_to_error(): #잘못 분류된 폴더 tmp -> error 폴더로 이동
    #유니코드 폴더가 유니코드 이름을 통으로 달린채 이동해야 함
    tmp_path = base_path + "/tmp"
    t_list = os.listdir(tmp_path)
    if len(t_list) == 0: #tmp 폴더가 비어있을 때(폴더를 부르지 않고 변경하기 버튼을 누른 경우)
        messagebox.showwarning(title="경고", message="작업할 폴더를 불러와주세요")
    uni = t_list[0]
    uni_path = tmp_path + '/' + uni
    error_path = base_path + "/error" #error 폴더로 이동을 함
    if os.path.isdir(error_path) == False: #error 폴더가 없는 경우 생성
        os.mkdir("error")
    error_uni = error_path + '/' + uni
    if os.path.isdir(error_uni) == False: #unicode 이름에 해당되는 폴더를 생성
        os.mkdir(error_uni)
    call_tmp_list = os.listdir(uni_path) #tmp/uni에 들어있는 파일의 개수
    for i in call_tmp_list: #tmp/uni 안에 들어있는 파일들을 전부 복사
        move_img = os.path.join(uni_path, i)
        dst = os.path.join(error_uni, i)
        shutil.move(move_img, dst)
    next_folder() #파일 이동이 완료되면 자동으로 다음 폴더로 넘어가게 됨

#진행 사항 확인, 리스트 박스 상단에 위치
def count_folder(path_name):
    global order
    title_folder = base_path + '/title'
    title_folder_list = os.listdir(title_folder)
    title_folder_no = len(title_folder_list)

    path_name = path_name
    order = title_folder_list.index(path_name)
    o = '{}/{}'.format(order+1, title_folder_no)
    order_label = Label(button_left_top, text=o)
    order_label.grid(row=4, padx="10", pady="4")
    order_label.configure(font=16)
    #진행률 %
    # p = "%.2f%%" % (order+1 / title_folder_no * 100.0)
    # percent = Label(button_left_top, text=p)
    # percent.grid(row=0, padx="10", pady="4")
    # percent.configure(font=16)

#리스트 박스 안에 리스트 불러오기
def lbox():
    global unicode
    global order

    listbox.delete(0, END)
    title_list = os.listdir(title_path)
    for i in range(len(title_list)):
        listbox.insert(i, title_list[i])
    listbox.grid(row = 0)
    print(type(listbox))
    current_loc = order
    if current_loc == 0:
        listbox.itemconfig(current_loc, background='Yellow')
    elif current_loc % 35 == 0:
        listbox.yview(current_loc)
        listbox.itemconfig(current_loc, background='Yellow')
    else:
        remain = current_loc % 35
        listbox.yview(current_loc - remain)
        listbox.itemconfig(current_loc, background='Yellow')

# 마우스 클릭 이벤트
def click_event(path):
    print("click_event : ", path)

#리스트 박스 클릭 이벤트
def selected_item(event): #리스트 박스 안의 문자를 클릭하는 경우 해당 유니코드의 폴더안의 이미지를 불러오게 됨
    global title_path
    title_path = title_path
    print("title_path : ", title_path)
    for i in listbox.curselection():
        listbox_path = title_path + '/' + listbox.get(i)
        print("listbox_path : ", listbox_path)
        # click_event(listbox_path)


label = []

# 이미지 호출
def image_label(tmp_path, path_name):
    clearFrame()
    global f_len
    global f
    global unicode

    img_row = 0
    but_row = 2
    delete_col = 0
    modify_col = 1
    delete = []
    modify = []
    img_col = 0

    path_name = path_name  # 처음 화면에 이미지를 띄울 때만 title폴터에서 호출, 두번째 부터는 전부 임시 폴더에서 불러온다.
    tmp_path = tmp_path
    unicode = tmp_path.split('/')[-1]
    print("show", tmp_path)
    f = os.listdir(tmp_path)
    f_len = len(f)
    print("image len", f_len)

    new_data = path_name[1:5] #한자, 16진수로 변환
    data = "0x" + new_data
    ten = int(data, 16) #10진수로 변환
    t = chr(ten)
    new_path_name = path_name + "\t" + t
    fontpath = "./TH-Tshyn-P0.ttf" #폰트 지정이 된건가?
    font = tkinter.font.Font(family=fontpath, size=20)
    folder_label.config(text=new_path_name, font=font)


    for i in range(f_len):
        call_img = os.path.join(tmp_path, f[i])
        img = Image.open(call_img)
        w, h = img.size  # 보여지는 이미지 사이즈 통일
        image_mid_width = image_mid.winfo_width()
        image_mid_height = image_mid.winfo_height()
        # print("w , h : ", image_mid_width, image_mid_height)

        w_count = (image_mid_width // (w * 1.2)) #가로 출력 가능 이미지의 개수
        h_count = (image_mid_height // (h * 2)) #세로 출력 가능 이미지의 개수
        p_count = w_count * h_count #페이지 출력 가능 이미지의 개수
        # print("count : ", w_count, h_count)

        pic = ImageTk.PhotoImage(image=img)
        label = Label(image_mid, image=pic, width=w, height=h)
        label.image = pic  # 안하면 사진 안보임

        if i < w_count: #첫줄 이미지를 출력하는 방법
            label.grid(row=img_row, column=img_col, columnspan=2, rowspan=2, padx=6, pady=10)
            delete.append(Button(image_mid, text="삭제", width=5, height=2,
                                 command=lambda i=i: delete_image(i, tmp_path, path_name)))
            delete[i].grid(row=but_row, column=delete_col, padx=1, pady=0)
            # no 버튼을 누르면 이미지 파일 변경 가능
            modify.append(Button(image_mid, text="변경", width=5, height=2,
                                 command=lambda i=i: change_image(i, tmp_path, path_name)))
            modify[i].grid(row=but_row, column=modify_col, padx=1, pady=0)
        else: #두번째 줄 부터
            if i % w_count == 0:
                img_row += 3
                but_row += 3
                delete_col = 0
                modify_col = 1
                img_col = 0
            label.grid(row=img_row, column=img_col, columnspan=2, rowspan=2, padx=6, pady=10)
            delete.append(Button(image_mid, text="삭제", width=5, height=2,
                                 command=lambda i=i: delete_image(i, tmp_path, path_name)))
            delete[i].grid(row=but_row, column=delete_col, padx=1, pady=0)
            # no 버튼을 누르면 이미지 파일 변경 가능
            modify.append(Button(image_mid, text="변경", width=5, height=2,
                                 command=lambda i=i: change_image(i, tmp_path, path_name)))
            modify[i].grid(row=but_row, column=modify_col, padx=1, pady=0)
        delete_col += 10
        modify_col += 10
        img_col += 10
    lbox()

#프로그램 종료 전 자동 저장: done버튼을 누르지 않아도 작업한 내용이 전부 done으로 이동
def on_closing():
    bp = str(f'{os.path.dirname(__file__)}')
    tp = bp + '/tmp'
    MsgBox = messagebox.askquestion('프로그램 종료', '종료하시겟습니까?\n예를 선택 시 현재 화면의 폴더까지 삭제 됩니다. \n작업이 완료 되었다면 예를 눌러주세요.\n\n(아니오 선택 시 작업이 저장되지 않습니다.)', icon='error')
    if MsgBox == 'yes':
        if len(os.listdir(tp)) != 0: #tmp 폴더에 내용이 남아있을 때 done()작업 실행
            done()
        root.destroy() #작업 중지 및 화면 닫기
    else:#작업이 저장되지 않음
        t_path = Path(tp)
        if t_path.exists() == True: #tmp 폴더가 존재하는 경우 해당 폴더를 지운 후 프로그램 종료
            shutil.rmtree(tp) #tmp폴더를 삭제, 프로그램 실행시 tmp폴더를 만들어 주므로 삭제해도 문제 없음
        root.destroy() #작업 중지 및 화면 닫기
root.protocol("WM_DELETE_WINDOW", on_closing) #프로그램 종료


# 중앙 우측에서 작동하는 버튼
b1 = Button(button_left_top, text="불러오기", width=10, height=2, command=open_folder)
b1.grid(row=1, column=0, padx="10", pady="4")
b1 = Button(button_left_top, text="화면정렬", width=10, height=2, command=window)
b1.grid(row=2, column=0, padx="10", pady="4")
b3 = Button(button_left_top, text="작업저장", width=10, height=2, command=done)
b3.grid(row=3, column=0, padx="10", pady="4")
separate_line = Label(button_left_top, text='=================')
separate_line.grid()

#중앙 우측에 위치하는 리스트 박스
listbox = Listbox(button_left_btm, selectmode="extended", height=35)
# listbox.bind('<<ListboxSelect>>', selected_item)
# listbox.bind('<ButtonRelease>', selected_item)
scroll_y = Scrollbar(button_left_btm, orient="vertical", command=listbox.yview)
scroll_y.grid(row=0, column=1, sticky="ns")
listbox.configure(yscrollcommand=scroll_y.set)
# lbox()


#이미지 우측 작동 버튼
btm_b1 = Button(page_mid, text="다음\n폴더", width=6, height=3, command=next_folder)
btm_b1.grid(row=1, column=0, sticky="w", pady="4")
btm_b2 = Button(page_mid, text="분류\n실패", width=6, height=3, command=tmp_to_error)
btm_b2.grid(row=2, column=0, sticky="w", pady="4")
# btm_b3 = Button(page_mid, text="▶", width=6, height=2)
# btm_b3.grid(row=3, column=0, sticky="w", pady="4")

root.mainloop()