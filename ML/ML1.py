from tkinter import *
import PIL
from PIL import ImageTk
from PIL import Image
from tkinter import messagebox
root=Tk()
root.title('Spotify Survey')
root.iconbitmap('C:/Users/mayan/Downloads/datasets/Spotify_logo_symbol.ico')
root.config(background='White')
var1=StringVar()
str1='below 18'
str2='18 to 24'
str3='25 and above'
var1.set('NaN')
var2=StringVar()
str4='Yes'
str5='No'
var2.set('NaN')
def display_button():
    top=Toplevel()
    name='Your Name: '+name_entry.get()
    name1=Label(top,text=name).pack()
    email='Email Address: '+email_entry.get() 
    email1=Label(top,text=email).pack()
    q1_label=Label(top,text='Q1:What is your Age?',anchor=W).pack()
    
    Radiobutton(top,text='below 18',variable=var1,value=str1,state=DISABLED,command=lambda:display_button(var1.get())).pack()
    Radiobutton(top,text='18 to 24',variable=var1,value=str2,state=DISABLED,command=lambda:display_button(var1.get())).pack()
    Radiobutton(top,text='25 and above 25',variable=var1,value=str3,state=DISABLED,command=lambda:display_button(var1.get())).pack()
    q2_label=Label(top,text='Q2:Where Did you heard about Spotify from?',anchor=W).pack()
    #q2_answer=q2_entry.get()
    q2_label=Label(top,text=q2_entry.get()).pack()
    q3_label=Label(top,text='Q3:Did you Like Spotify?',anchor=W).pack()
    Radiobutton(top,text='Yes',variable=var2,value=str4,state=DISABLED,command=lambda:display_button(var2.get())).pack()
    Radiobutton(top,text='No',variable=var2,value=str5,state=DISABLED,command=lambda:display_button(var2.get())).pack()
    def close():
        response=messagebox.askyesno('Close Window','Do you want to close?')
        if response==1:
            top.destroy()
        else:
            pass
    
    close_button=Button(top,text='Close Window',command=close).pack()
    

Image_top=ImageTk.PhotoImage(Image.open('C:/Users/mayan/Downloads/datasets/spotify.png'))
Image_label=Label(root,image=Image_top,bg='white')
heading_Label=Label(root,text='Spotify Advertisment',font=('Comic San MS',24),bg='White')
name_Label=Label(root,text='Name: ',font=('Comic San MS',16),bg='White',anchor=W)
name_entry=Entry(root)
email_label=Label(root,text='Email: ',font=('ComicSansMS',16),bg='White',anchor=W)
email_entry=Entry(root)
ques_heading=Label(root,text='Questions: ',font=('ComicSansMS',16),bg='White',anchor=W)
q1_label=Label(root,text='Q1:What is your Age?',bg='White',font=('ComicSansMS',16),anchor=W)
Radiobutton(root,text='below 18',bg='White',variable=var1,value=str1,command=lambda:display_button(var1.get())).grid(row=9,column=2)
Radiobutton(root,text='18 to 24',bg='White',variable=var1,value=str2,command=lambda:display_button(var1.get())).grid(row=9,column=3)
Radiobutton(root,text='25 and above 25',bg='White',variable=var1,value=str3,command=lambda:display_button(var1.get())).grid(row=9,column=4)
q2_label=Label(root,text='Q2:Where Did you heard about Spotify from?',font=('ComicSansMS',16),bg='White',anchor=W)
q2_entry=Entry(root)
q3_label=Label(root,text='Q3:Did you Like Spotify?',font=('Com Sans MS',16),bg='White',anchor=W)
Radiobutton(root,text='Yes',variable=var2,value=str4,bg='White',command=lambda:display_button(var2.get())).grid(row=13,column=2)
Radiobutton(root,text='No',variable=var2,value=str5,bg='White',command=lambda:display_button(var2.get())).grid(row=13,column=3)
continue_button=Button(root,text='Continue',font=('Com Sans MS',16),bg='White',command=display_button)



q2_entry.grid(row=11,column=2,padx=10,ipadx=100)
continue_button.grid(row=14,column=2)
q3_label.grid(row=12,column=2)
q2_label.grid(row=10,column=2)
ques_heading.grid(row=7,column=1)
q1_label.grid(row=8,column=2)
email_entry.grid(row=4,column=3,padx=10,ipadx=100)
email_label.grid(row=4,column=2)
name_entry.grid(row=3,column=3,padx=10,ipadx=100)
name_Label.grid(row=3,column=2)
Image_label.grid(row=0,column=0)
heading_Label.grid(row=0,column=2)
title_label=Label(root,text='Purcharse Survey',font=34)
root.mainloop()