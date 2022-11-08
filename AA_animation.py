from PIL import Image , ImageDraw , ImageFont
import tkinter
import tkinter.filedialog
import cv2
import os
import shutil
import numpy as np

np.seterr(divide='ignore', invalid='ignore')

colorset = "MWN$@%#&B89EGA6mK5HRkbYT43V0JL7gpaseyxznocv?jIftr1li*=-~^`':;,. "

ttfontname = os.path.dirname(__file__)+"/NotoSansMono-VariableFont_wdth,wght.ttf"

fontsize = 12

AA_Reduction = int(input("How big is it?\nPlease specify the width:"))

AA_name = input("What is the name of the video?")

def resize(src, h, w):

    dst = np.empty((h,w))

    hi, wi = src.shape[0], src.shape[1]

    ax = w / float(wi)
    ay = h / float(hi)

    for y in range(0, h):
        for x in range(0, w):
            xi, yi = int(round(x/ax)), int(round(y/ay))

            if xi > wi -1: xi = wi -1
            if yi > hi -1: yi = hi -1

            dst[y][x] = src[yi][xi]

    return dst

def save_all_frames(video_path, dir_path, basename, ratio, file_pass,font_name = ttfontname, fontsize = fontsize, ext='jpg'):

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    n = 0

    while True:
        ret, frame = cap.read()
        if ret:
            
            size=frame.shape
            width = size[1]

            ratio = round(width/AA_Reduction)

            img_gray = 0.299 * frame[:, :, 2] + 0.587 * frame[:, :, 1] + 0.114 * frame[:, :, 0]

            if size[1] % ratio != 0:
                    size_coordinate_y = size[1] // ratio + 1
            else:
                    size_coordinate_y = size[1] // ratio

            if size[1] % ratio != 0:
                    size_coordinate_x = size[0] // ratio + 1
            else:
                    size_coordinate_x = size[0] // ratio

            Completed_image = resize(img_gray, size_coordinate_x, size_coordinate_y)

            Completed_image = np.resize(Completed_image,(size_coordinate_x,size_coordinate_y)).astype(np.uint8)


            img = Completed_image

            Completed_size = img.shape

            AA_result = ""

            for y in img:
                AA_result += "\n"
                for x in y:
                    AA_result += colorset[x // 4] *2
            
            canvasSize    = (round(fontsize*1.2*Completed_size[1]), round(fontsize*1.4*Completed_size[0]))
            backgroundRGB = (255)
            textRGB       = (0)

            img  = Image.new('L', canvasSize, backgroundRGB)
            draw = ImageDraw.Draw(img)

            font = ImageFont.truetype(ttfontname, fontsize)
            textWidth, textHeight = draw.textsize(AA_result,font=font)
            draw.text((0,0), AA_result, fill=textRGB, font=font)

            img = np.array(img)

            print(size)
            
            if canvasSize[1] > size[1]:
                img = resize(img,img.shape[0]//3,img.shape[1]//3)

                cv2.imwrite(str(base_path)+'_'+str(n).zfill(digit)+'.' +str(ext),img)

                size = img.shape

                print(size)

                #print(type(img),type(size)) 
            
            else:

                cv2.imwrite(str(base_path)+'_'+str(n).zfill(digit)+'.' +str(ext),img)

                size = img.shape
            
                print(size) 

            n += 1

            print(n)

        else:
            break

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    video = cv2.VideoWriter(Filepass + AA_name +'.mp4',fourcc, fps, (size[1],size[0]))
    
    for i in range(n):
        img = cv2.imread(str(base_path)+'_'+str(i).zfill(digit)+'.' +str(ext))

        if img is None:
            print("can't read")
            break

        video.write(img)

    video.release()

Filepass = tkinter.filedialog.askdirectory(title="Which file do you want to put it in?") + '/'
file_name= tkinter.filedialog.askopenfilename(filetypes = [("Movie file", "*.mp4") ])

new_dir_name = Filepass + 'AA_data_folder/'

os.mkdir(new_dir_name)

save_all_frames(file_name, new_dir_name, 'Siberian_ascii', AA_Reduction, Filepass,'png')

print('written')

shutil.rmtree(new_dir_name)
