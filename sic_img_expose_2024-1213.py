import glob
import os,cv2
import numpy as np
from pathlib import Path
from glob import glob
from tkinter import filedialog
from tkinter import *
from functools import partial

class SimpleTkForm(object):
    def __init__(self):
        self.root = Tk()
        self.outdir = ""
        self.brightness = 0 #b
        self.contrast = 0 #c

    def myform(self):
        self.root.title('SIC transform Dialog')
        frame = Frame(self.root, pady=10)
        form_data = dict()
        form_fields = ['output_directory' , 'brightness', 'contrast'] #, 'database name']
        cnt = 0
        for form_field in form_fields:
            Label(frame, text=form_field, anchor=NW).grid(row=cnt,column=1, pady=5, padx=(10, 1), sticky="W")
            textbox = Text(frame, height=1, width=15)
            form_data.update({form_field: textbox})
            textbox.grid(row=cnt,column=2, pady=5, padx=(3,20))
            cnt += 1

        conn_test = partial(self.test_db_conn, form_data=form_data)
        Button(frame, text='Submit', width=15, command=conn_test).grid(row=cnt,column=2, pady=5, padx=(3,20))

        Button(frame, text='End', width=15,command=self.quit).grid(row=cnt,column=1, pady=10, padx=(3,20))
        frame.pack()
        self.root.mainloop()

    def test_db_conn(self, form_data):
        data = {k:v.get('1.0', END).strip() for k,v in form_data.items()}
        # validate data or do anything you want with it
        self.outdir = data['output_directory']
        self.brightness = int(data['brightness'])
        self.contrast = int(data['contrast'])
        self.bmp2png()
        # print("-------0-----> ", type(data['contrast']),type(self.contrast))
        # print(self.outdir)

    def quit(event):
        quit()

    def bmp2png(self):
        fdd = filedialog.askdirectory()
        all_img = glob(fdd+"/**/*.bmp", recursive=True)
        all_img.sort()
        #print("-------0-----> ", all_img)
        cur_dir = Path(all_img[0]).parent
        #print("-------1-----> ", cur_dir)
        dd = self.outdir
        print("-------2.0----> ", type(self.contrast),self.contrast)#(cur_dir / dd))

        if (os.path.exists(cur_dir / dd) == False):
            os.makedirs(cur_dir / dd)
            print("Creat new folder-------2.5----> ", cur_dir / dd)
        cur_dir1 = cur_dir / dd
        #print("-------3----> ", cur_dir1)
        idx = 0
        for img in glob(str(cur_dir / "*.bmp")):
            filename = Path(img).stem
            gray = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
            output = gray * (255 / 100 + 1) - self.contrast + self.brightness  # 轉換公式
            output = np.clip(output, 0, 255)
            output = np.uint8(output)
            cv2.imwrite(str(cur_dir1 / f'{filename}.png'),output)
            print(idx,"=>", str( f'{filename}.png'))
            #print(idx)
            idx+=1
        cv2.destroyAllWindows()

if __name__ == '__main__':
    api = SimpleTkForm()
    api.myform()

