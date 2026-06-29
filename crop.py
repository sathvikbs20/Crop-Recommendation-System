from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from sklearn import metrics
import warnings
warnings.filterwarnings('ignore')

# ================== ML PART ==================
df = pd.read_csv("crop_recommendation.csv")
features = df[['N', 'P','K','temperature', 'humidity', 'ph', 'rainfall']]
target = df['label']

from sklearn.model_selection import train_test_split
Xtrain, Xtest, Ytrain, Ytest = train_test_split(features,target,test_size = 0.2,random_state =2)

from sklearn.ensemble import RandomForestClassifier
RF = RandomForestClassifier(n_estimators=20, random_state=0)
RF.fit(Xtrain,Ytrain)

predicted_values = RF.predict(Xtest)
x = metrics.accuracy_score(Ytest, predicted_values)
print("RF's Accuracy is: {:.2f} ".format(x*100))
print(classification_report(Ytest,predicted_values))

# ================== GUI PART ==================
root = Tk()
root.title("🌱 Smart Crop Recommendation System")
root.geometry("1600x850")
root.resizable(False, False)

# Background image
img=Image.open("a.jpg")
img=img.resize((1500,750))
bg=ImageTk.PhotoImage(img)

lbl=Label(root,image=bg)
lbl.place(x=0,y=0)

label = Label(
    root,
    text="🌱 Smart Crop Recommendation System",
    font=("Segoe UI", 28, "bold"),
    fg="white",
    bg="#2E8B57",   
    padx=20,
    pady=10
)
label.place(x=300,y=10)

# Input fields
label_1 = Label(root, text ='nitrogen',font=("Helvetica", 18),background="#CDD954")
label_1.place(x=150,y=100)
Entry_1= Entry(root,font=("Helvetica", 18),justify=CENTER)
Entry_1.place(x=450,y=100)

label_2 = Label(root, text ='phosporus',font=("Helvetica", 16),background="#CDD954")
label_2.place(x=150,y=160)
Entry_2 = Entry(root,font=("Helvetica", 18),justify=CENTER)
Entry_2.place(x=450,y=160)

label_3 = Label(root, text ='pottasium',font=("Helvetica", 18),background="#CDD954")
label_3.place(x=150,y=220)
Entry_3 = Entry(root,font=("Helvetica", 18),justify=CENTER)
Entry_3.place(x=450,y=220)

label_4 = Label(root, text ='temperature',font=("Helvetica", 18),background="#CDD954")
label_4.place(x=150,y=280)
Entry_4= Entry(root,font=("Helvetica", 18),justify=CENTER)
Entry_4.place(x=450,y=280)

label_5 = Label(root, text ='humidity',font=("Helvetica", 18),background="#CDD954")
label_5.place(x=150,y=340)
Entry_5 = Entry(root,font=("Helvetica", 18),justify=CENTER)
Entry_5.place(x=450,y=340)

label_6 = Label(root, text ='ph',font=("Helvetica", 18),background="#CDD954")
label_6.place(x=150,y=400)
Entry_6 = Entry(root,font=("Helvetica", 18),justify=CENTER)
Entry_6.place(x=450,y=400)

label_7 = Label(root, text ='rainfall',font=("Helvetica", 18),background="#CDD954")
label_7.place(x=150,y=460)
Entry_7 = Entry(root,font=("Helvetica", 18),justify=CENTER)
Entry_7.place(x=450,y=460)

# ================== FUNCTIONS ==================
def clear_out():
    global out_img
    try:
        out_img.destroy()   # remove image if exists
    except:
        pass
    output.configure(text="")   # clear output text
    Entry_1.delete(0,END)
    Entry_2.delete(0,END)
    Entry_3.delete(0,END)
    Entry_4.delete(0,END)
    Entry_5.delete(0,END)
    Entry_6.delete(0,END)
    Entry_7.delete(0,END)

def predict():
    try:
        N = float(Entry_1.get())
        P = float(Entry_2.get())
        K = float(Entry_3.get())
        temperature = float(Entry_4.get())
        humidity = float(Entry_5.get())
        ph = float(Entry_6.get())
        rainfall = float(Entry_7.get())

        # ---------- Input Validation ----------
        if not (0 <= N <= 140):
            raise ValueError("Nitrogen must be between 0 and 140")

        if not (5 <= P <= 145):
            raise ValueError("Phosphorus must be between 5 and 145")

        if not (5 <= K <= 205):
            raise ValueError("Potassium must be between 5 and 205")

        if not (0 <= temperature <= 60):
            raise ValueError("Temperature must be between 0°C and 60°C")

        if not (0 <= humidity <= 100):
            raise ValueError("Humidity must be between 0% and 100%")

        if not (3.5 <= ph <= 9.5):
            raise ValueError("pH must be between 3.5 and 9.5")

        if not (0 <= rainfall <= 500):
            raise ValueError("Rainfall must be between 0 and 500 mm")

        # ---------- Prediction ----------
        out = RF.predict([[N, P, K, temperature, humidity, ph, rainfall]])

        output.configure(
            text="Recommended Crop : " + str(out[0]),
            fg="darkgreen",
            font=("Helvetica", 18, "bold")
        )

        try:
            res_img = Image.open("result\\" + str(out[0]) + ".jpg")
            res_img = res_img.resize((300,300), Image.LANCZOS)

            bgg = ImageTk.PhotoImage(res_img)

            global out_img
            out_img = Button(root, image=bgg, command=clear_out)
            out_img.image = bgg
            out_img.place(x=800, y=300)

        except:
            output.configure(text="Image not found for " + str(out[0]))

    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))

    except Exception:
        messagebox.showerror(
            "Input Error",
            "Please enter numeric values in all fields."
        )
# ================== BUTTONS ==================
b1 = Button(root, text = 'Predict',font=("Helvetica", 18),background="#CDD954",command = predict)
b1.place(x=150,y=550)

b2 = Button(root, text = 'Clear',font=("Helvetica", 18),background="red",fg="white",command = clear_out)
b2.place(x=300,y=550)

output = Label(root,font=("Helvetica", 18),justify=CENTER)
output.place(x=450,y=550)

root.mainloop()
