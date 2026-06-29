from tkinter import *
from PIL import Image,ImageTk

root = Tk()
root.title('Crop Recommendation window')
root.geometry('1500x750')
img=Image.open("a.jpg")
img=img.resize((1500,750))
bg=ImageTk.PhotoImage(img)

lbl=Label(root,image=bg)
lbl.place(x=0,y=0)
out=['rice']
res_img=Image.open("result\\"+str(out[0])+".jpg")
res_img=res_img.resize((300,300))
bgg=ImageTk.PhotoImage(res_img)
##    out_img.configure(image=bgg)
out_img = Label(root,image=bgg)
out_img.place(x=900,y=500)
root.mainloop()