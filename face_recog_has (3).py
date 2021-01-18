from tkinter import *
from datetime import date
from tkinter.filedialog import askopenfile
# from tkinter.ttk import *
from tkinter import messagebox, filedialog, ttk
import cv2
from PIL import Image
import mysql.connector
import wx
import wx.xrc
import wx.grid
import cv2 as cv
import re
import numpy as np
import string
import gettext
import os
from datetime import datetime

def train(): 
  recognizer = cv2.face.LBPHFaceRecognizer_create()
  path='C:/Face_Recognition/dataset'

  def getImagesWithID(path):
    
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    faces=[]    
    IDs=[]
    for imagePath in imagePaths:     
        faceImg=Image.open(imagePath).convert('L')
        faceNp=np.array(faceImg,'uint8')
        ID=int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(faceNp)
        IDs.append(ID)
        
        cv2.imshow("traning",faceNp) 
        cv2.waitKey(10)
        
    return IDs, faces
  Ids, faces = getImagesWithID(path)
  recognizer.train(faces, np.array(Ids))
  recognizer.save('trainner/trainner.yml')
  cv2.destroyAllWindows()
 
def my_function():  
  face_cascade=cv2.CascadeClassifier('C:/Face_Recognition/haarcascade_frontalface_default.xml')
  cap=cv2.VideoCapture(0);

  sampleNum=0;
  while (True):
    ret, img=cap.read()
    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces= face_cascade.detectMultiScale(gray,1.1,4)

    for(x,y,w,h) in faces :
      sampleNum=sampleNum+1
      cv2.imwrite("dataset/User."+str(roll.get())+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
      cv2.rectangle(img, (x,y),(x+w, y+h), (255,0,0), 2)
      cv2.waitKey(100)
    cv2.imshow("Face", img)
    cv2.waitKey(1)
    if(sampleNum>100):
      break         
  cap.release()
  cv2.destroyAllWindows()

def take_attendance(): 
  dict={}
  Date= str(date.today())
  fname="C:/Face_Recognition/trainner/trainner.yml"
  if not os.path.isfile(fname):
    print("Please train the data first")
    exit(0)
  cap =cv2.VideoCapture(0)
  face_cascade=cv2.CascadeClassifier('C:/Face_Recognition/haarcascade_frontalface_default.xml')
  rec=cv2.face.LBPHFaceRecognizer_create();
  rec.read(fname)
  id=0
  font= cv2.FONT_HERSHEY_SIMPLEX
  while(True):
    ret, img=cap.read()
    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray, 1.3, 5)
    for(x,y,w,h) in faces:
      cv2.rectangle(img, (x,y),(x+w, y+h), (0,0,255), 2)
      id,conf=rec.predict(gray[y:y+h,x:x+w])
     
      dict[id]=id
      
      cv2.putText(img,str(id),(x,y+h),font,1,(150,0,0),2,cv2.LINE_AA)
 
    cv2.imshow('Face', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      for key, value in dict.items() :
        myconn = mysql.connector.connect(host="localhost",  user="root",  passwd="root",  database="face_recog")
        cursor=myconn.cursor()
        cursor.execute("INSERT INTO attendance(date,enroll_id,attendance) VALUES (%s,%s,%s)",(Date,key,"present"))
        myconn.commit()
      break 
  cap.release()
  cv2.destroyAllWindows()
  buttonoptions()

def checkLogin():
  global u
  u = nameE.get()
  p = pwordE.get()

  conn = mysql.connector.connect(host="localhost",  user="root",  passwd="root",  database="face_recog")
  cur = conn.cursor()

  cur.execute("SELECT * FROM login where username='" + u + "'")

  flag=0

  for row in cur.fetchall():
    if row[1] == p:
      flag=1
      break
  if flag == 1:
    root.destroy()
    buttonoptions()
  else:
    messagebox.showinfo('Login', 'Incorrect Username or Password')
    nameE.delete(0, END)
    pwordE.delete(0, END)

def loginscreen():
  global nameE
  global pwordE
  global root

  root = Tk()
  root.title('Login')
  root.geometry('280x120+500+250')
  root.configure(background='SlateGray3')
  ins = Label(root, text='Enter admin credentials',bg='SlateGray3')
  ins.grid(sticky=W)

  name = Label(root, text='Username',bg='SlateGray3')
  pword = Label(root, text='Password',bg='SlateGray3')
  name.grid(row=2, sticky=W)
  pword.grid(row=3, sticky=W)

  nameE = Entry(root)
  pwordE = Entry(root, show='*')
  nameE.grid(row=2, column=1)
  pwordE.grid(row=3, column=1)
  nameE.focus()

  loginB = Button(root, text='Login',width=16, command=checkLogin,bg='light cyan')
  loginB.grid(row=4,column=1)
  root.mainloop()

def buttonoptions():
  global root
  root = Tk()
  root.title('Choose Option')
  root.geometry('600x600+350+40')
  root.configure(background='SlateGray3')

  newdata=Button(text='New Student Entry',command=new_data,width=50,height=3,font=("bold",9),bg='light cyan')
  newdata.place(x=100,y=50)
  update=Button(text='Update Student Record',width=50,command=update_student_data,font=("bold",9),height=3,bg='light cyan')
  update.place(x=100,y=120)
  attend=Button(text='Show Attendance',width=50,command=show_attend,height=3,font=("bold",9),bg='light cyan')
  attend.place(x=100,y=190)
  updatelogin=Button(text='Change Admin Login Credentials',width=50,command=update_login,font=("bold",9),height=3,bg='light cyan')
  updatelogin.place(x=100,y=260)
  deleterecord=Button(text='Delete Student Record',width=50,height=3,command=delete1,font=("bold",9),bg='light cyan')
  deleterecord.place(x=100,y=330)
  takatt=Button(text='Take Attendance',width=50,height=3,command=take_attend,font=("bold",9),bg='light cyan')
  takatt.place(x=100,y=400)
  logout=Button(text='Logout',width=50,command=log_out,height=3,font=("bold",9),bg='light cyan')
  logout.place(x=100,y=470)

def new_data():
  root.destroy()
  show_data()

def take_attend():
  root.destroy()
  take_attendance()

def log_out():
  root.destroy()
  loginscreen()

def update_login():
  root.destroy()
  update_admin()

def show_attend():
  root.destroy()
  show_attendance()

def delete1():
  root.destroy()
  delete_record()

def delete_record():
  global root
  root = Tk()
  root.geometry('350x150+400+200')
  root.title("Delete Record")
  root.configure(bg='SlateGray3')
  global roll1
  roll1=IntVar()

  label_0 = Label(root, text="Enroll Id",width=20,font=("bold", 10),bg='SlateGray3')
  label_0.place(x=10,y=10)

  entry_0 = Entry(root,textvar=roll1)
  entry_0.place(x=150,y=10)

  Button(root,text='Submit',width=12,fg='black',command=delete_data,bg='light cyan').place(x=100,y=50)
  Button(root,text='Back',width=12,fg='black',command=back,bg='light cyan').place(x=200,y=50)
  root.mainloop()

def delete_data():
  enroll=roll1.get()
  myconn = mysql.connector.connect(host="localhost",  user="root",  passwd="root",  database="face_recog") 
  cursor=myconn.cursor()
  cursor.execute("SELECT enroll_id from signup where enroll_id=%s ",[enroll])
  flag=0
  for row in cursor.fetchall():
   if row[0]==enroll:
    flag=1
    break
  if flag==1:
   cursor1=myconn.cursor()   
   cursor1.execute("DELETE from attendance where enroll_id=%s ",[enroll])
   cursor1.execute("DELETE from signup where enroll_id=%s ",[enroll])
   myconn.commit()
   messagebox.showinfo('Deletion','Recored deleted successfully')
   root.destroy()
   buttonoptions()
  else:
   messagebox.showinfo('Alert', 'Enroll id not found')

def back():
  root.destroy()
  buttonoptions()

def  show_attendance():
  class Database ( wx.Frame ):
    def __init__( self, parent ):
      wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Attendance", pos = wx.DefaultPosition, size = wx.Size( 700,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
        
      self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
      self.SetBackgroundColour(wx.Colour(52,203,142))
      bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
      bSizer5 = wx.BoxSizer( wx.VERTICAL )
        
      self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Attendance", wx.DefaultPosition, wx.DefaultSize, 0 )
      self.m_staticText1.Wrap( -1 )
      self.m_staticText1.SetFont( wx.Font( 20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, "Elephant" ) )
      self.m_staticText1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWFRAME ) )
       
      bSizer5.Add( self.m_staticText1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
      
      bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
        
      bSizer7 = wx.BoxSizer( wx.VERTICAL )
        
      bSizer16 = wx.BoxSizer( wx.VERTICAL )
        
      self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size(20,20), wx.TAB_TRAVERSAL )
      self.m_panel1.SetBackgroundColour(wx.Colour(52,203,142))
      bSizer16.Add( self.m_panel1, 1, wx.ALL, 5 )
      
      bSizer7.Add( bSizer16, 1, wx.EXPAND, 5 )
        
      bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
      bSizer8 = wx.BoxSizer( wx.VERTICAL )    

      bSizer8 = wx.BoxSizer( wx.VERTICAL )
        
      bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
        
      self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Search by date :",wx.DefaultPosition, wx.DefaultSize, 0 )
      self.m_staticText2.Wrap( -1 )
      self.m_staticText2.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
        
      bSizer9.Add( self.m_staticText2, 0, wx.ALIGN_TOP|wx.ALL, 5 )
        
      self.txtSearch = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
      self.txtSearch.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
        
      bSizer9.Add( self.txtSearch, 0, wx.ALIGN_TOP|wx.ALL, 5 )
        
      self.btnSearch = wx.Button( self, wx.ID_ANY, u"Search", wx.DefaultPosition, wx.Size( 120,28 ), 0 )
      self.btnSearch.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
      self.btnSearch.SetBackgroundColour(wx.Colour(178,178,178))
        
      bSizer9.Add( self.btnSearch, 0, wx.ALIGN_TOP|wx.ALL, 5 )
             
      bSizer8.Add( bSizer9, 1, wx.EXPAND, 5 )
      self.btnBack = wx.Button( self, wx.ID_ANY, u"Back", wx.DefaultPosition, wx.Size( 120,28 ), 0 )
      self.btnBack.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
      self.btnBack.SetBackgroundColour( wx.Colour(178,178,178) )
        
      bSizer9.Add( self.btnBack, 0, wx.ALIGN_TOP|wx.ALL, 5 ) 
      self.btnBack.Bind(wx.EVT_BUTTON, self.btnBackClick)
      self.btnSearch.Bind( wx.EVT_BUTTON, self.btnSearchClick )

      self.m_grid1 = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 150,460 ), 0 )

      self.m_grid1.CreateGrid( 50, 7 )
      self.m_grid1.EnableEditing( False )
      self.m_grid1.EnableGridLines( True )
      self.m_grid1.EnableDragGridSize( False )
      self.m_grid1.SetMargins( 0, 0 )

      self.m_grid1.EnableDragColMove( False )
      self.m_grid1.EnableDragColSize( True )
      self.m_grid1.SetColLabelSize( 30 )
      self.m_grid1.SetColLabelValue( 0, u"Date" )
      self.m_grid1.SetColLabelValue( 1, u"Enroll Id" )
      self.m_grid1.SetColLabelValue( 2, u"Name" )
      self.m_grid1.SetColLabelValue( 3, u"Phone No.")
      self.m_grid1.SetColLabelValue( 4, u"Guardian Name" )
      self.m_grid1.SetColLabelValue( 5, u"Guardian No." )
      self.m_grid1.SetColLabelValue( 6, u"Attendance" )
      self.m_grid1.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
      
      self.m_grid1.EnableDragRowSize( True )
      self.m_grid1.SetRowLabelSize( 40 )
      self.m_grid1.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
      
      self.m_grid1.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
      self.m_grid1.SetFont( wx.Font( 5, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
        
      bSizer8.Add( self.m_grid1, 0, wx.EXPAND, 5 )
      bSizer6.Add( bSizer8, 1, wx.EXPAND, 5 )        
      bSizer5.Add( bSizer6, 1, wx.EXPAND, 5 )
      bSizer1.Add( bSizer5, 1, wx.EXPAND, 5 )
      
      self.SetSizer( bSizer1 )
      self.Layout()
      self.Centre( wx.BOTH )
      cnn = mysql.connector.connect(host="localhost",  user="root",  passwd="root",  database="face_recog")
      cur = cnn.cursor()
      cur.execute("SELECT attendance.date,attendance.enroll_id,signup.name,signup.phone_no,signup.guardian_name,signup.guardian_no,attendance.attendance FROM signup,attendance WHERE signup.enroll_id=attendance.enroll_id ORDER BY attendance.date DESC limit 50")
      rows = cur.fetchall()
      for i in range(0,len(rows)):
        for j in range(0,7):
          cell = rows[i]
          self.m_grid1.SetCellValue(i,j,str(cell[j]))

    def __del__(self):
      pass

    def btnSearchClick( self, event ): 
      cnn = mysql.connector.connect(host="localhost",  user="root",  passwd="root",  database="face_recog")
      cur = cnn.cursor()
      cur.execute("SELECT attendance.date,attendance.enroll_id,signup.name,signup.phone_no,signup.guardian_name,signup.guardian_no,attendance.attendance FROM signup,attendance WHERE signup.enroll_id=attendance.enroll_id AND attendance.date LIKE '%"+self.txtSearch.Value+"%' ORDER BY attendance.date DESC limit 50")
      rows = cur.fetchall()
      for i in range(0,len(rows)):
        for j in range(0,7):
          cell = rows[i]
          self.m_grid1.SetCellValue(i,j,str(cell[j]))
    def btnBackClick( self, event ):
      buttonoptions()

    def clear_grid(self):
      self.txtID.Value=""
      self.txtName.Value=""
      self.txtAge.Value=""
      self.txtAddress.Value=""  
 
  app = wx.App(False)
  frame = Database(None)
  frame.Show()
  app.MainLoop()  

def update_student_data():
  root.destroy()
  new_update()

def dt():
  pass1=p.get()
  conn = mysql.connector.connect(host="localhost",  user="root",  passwd="root",  database="face_recog")
  con=conn.cursor()
  con.execute("UPDATE login SET pass=%s WHERE username=%s",(pass1,u))
  conn.commit()
  messagebox.showinfo('Updation','Password updated successfully')
  log_out()

def update_admin():
  global root
  global p
  root = Tk()
  root.geometry('400x150+400+200')
  root.configure(background='SlateGray3')
  root.title("Admin Password Change")
  p=StringVar()

  label_0 = Label(root, text="Password",width=20,font=("bold", 10),bg='SlateGray3')
  label_0.place(x=10,y=20)

  entry_0 = Entry(root,width=30,textvar=p)
  entry_0.place(x=130,y=20)

  Button(root,text='Submit',width=15,fg='black',command=dt,bg='light cyan').place(x=120,y=80)
  Button(root,text='Back',width=15,fg='black',command=back,bg='light cyan').place(x=240,y=80)
  root.mainloop()

def new_update():
  def data1():
    global ell
    ell=roll2.get()
    st = mysql.connector.connect(host="localhost",  user="root",  passwd="root",  database="face_recog")
    student=st.cursor()
    student.execute("select * from signup where enroll_id=%s",[ell])
    flag=0
    for coloumn in student.fetchall():
     if coloumn[0] == ell:
       flag=1
       break
    if flag==1:
      root.destroy()
      update2(ell)
    else:
      messagebox.showinfo('Id check','Incorrect Enroll id')

  def update1():
    global root
    root = Tk()
    root.geometry('400x200+400+250')
    root.configure(background='SlateGray3')
    root.title('Record Updation')

    global roll2
    global nm
    global phn
    global gn
    global gno

    roll2=IntVar()
    label_0 = Label(root, text="Enroll Id",width=20,font=("bold", 10),bg='SlateGray3')
    label_0.place(x=10,y=20)

    entry_0 = Entry(root,textvar=roll2)
    entry_0.place(x=150,y=20)

    Button(root,text='Submit',width=15,fg='black',command=data1,bg='light cyan').place(x=100,y=80)
    Button(root,text='Back',width=15,fg='black',command=back,bg='light cyan').place(x=230,y=80)
    root.mainloop()

  def data2():
    a=email1.get()
    b=ph.get()
    c=gn1.get()
    d=gno1.get()
    e=sem1.get()
    curr = mysql.connector.connect(host="localhost",  user="root",  passwd="root",  database="face_recog")
    curr1=curr.cursor()
    curr1.execute("UPDATE signup SET email_id=%s,phone_no=%s,guardian_name=%s,guardian_no=%s,sem=%s WHERE enroll_id=%s",(a,b,c,d,e,ell))
    curr.commit()
    messagebox.showinfo('Updation', 'Record Updated Successfully')
    root.destroy()
    buttonoptions()

  def update2(ell):
    global root
    root = Tk()
    root.geometry('500x300+400+200')
    root.configure(background='SlateGray3')
    root.title('Update Record')
    global email1
    global ph
    global gn1
    global gno1
    global sem1
    email1=StringVar()
    ph=IntVar()
    gn1=StringVar()
    gno1=IntVar()
    sem1=IntVar()
    my = mysql.connector.connect(host="localhost",  user="root",  passwd="root",  database="face_recog")
    cn=my.cursor()
    cn.execute("select email_id,phone_no,guardian_name,guardian_no,sem from signup where enroll_id=%s",[ell])
    for row in cn.fetchall():
      em=row[0]
      phn=row[1]
      gn=row[2]
      gno=row[3]
      sm=row[4]

    label_0 = Label(root, text="Email id",width=20,font=("bold", 10),bg='SlateGray3')
    label_0.place(x=10,y=20)
    entry_0 = Entry(root,textvar=email1,width=20)
    entry_0.insert(0,em)
    entry_0.place(x=150,y=20)

    label_1 = Label(root, text="Phone no",width=20,font=("bold", 10),bg='SlateGray3')
    label_1.place(x=10,y=50)
    entry_1 = Entry(root,textvar=ph)
    entry_1.insert(0,phn)
    entry_1.place(x=150,y=50)

    label_2 = Label(root, text="Guardian name",width=20,font=("bold", 10),bg='SlateGray3')
    label_2.place(x=10,y=80)
    entry_2 = Entry(root,textvar=gn1)
    entry_2.insert(0,gn)
    entry_2.place(x=150,y=80)

    label_3 = Label(root, text="Guardian no",width=20,font=("bold", 10),bg='SlateGray3')
    label_3.place(x=10,y=120)
    entry_3 = Entry(root,textvar=gno1)
    entry_3.insert(0,gno)
    entry_3.place(x=150,y=120)

    label_4 = Label(root, text="Semester",width=20,font=("bold", 10),bg='SlateGray3')
    label_4.place(x=10,y=160)
    entry_4 = Entry(root,textvar=sem1)
    entry_4.insert(1,sm)
    entry_4.place(x=150,y=160)

    Button(root,text='Submit',width=15,fg='black',command=data2,bg='light cyan').place(x=120,y=220)
    Button(root,text='Cancel',width=15,fg='black',command=back,bg='light cyan').place(x=250,y=220)
    root.mainloop()
  update1()

def database(): 
  try:
    int(phone.get())
    int(guardian_num.get())

  except:
    messagebox.showinfo('Error', "Please enter digit as phone number")
    root.destroy()
    show_data()
  if (len(str(phone.get()))==10 and len(str(guardian_num.get()))==10):
    pass 
  else:
    messagebox.showinfo('Error', 'Please enter 10 digit')
    root.destroy()
    show_data()     

  enroll_id=roll.get()
  name=name1.get()
  phone_no=phone.get()
  email_id=Email.get()
  guardian_name=guardian_n.get()
  guardian_no=guardian_num.get()
  gender=gender1.get()
  courses=tkcourse.get()
  sem=tksem.get()

  try:
    myconn = mysql.connector.connect(host="localhost",  user="root",  passwd="root",  database="face_recog")
   
    cursor=myconn.cursor()
    if gender==1:
      gender='m'
    elif gender==2:
      gender='f'
    else:
      gender='others'

    cursor.execute("INSERT INTO signup(enroll_id,name,phone_no,email_id,guardian_name,guardian_no,gender,courses,sem) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(enroll_id,name,phone_no,email_id,guardian_name,guardian_no,gender,courses,sem))

    myconn.commit()
    my_function()
    messagebox.showinfo('Data Entry', 'Register Successfully')  
    train()
  except mysql.connector.Error as er:
    messagebox.showinfo('Error', er)  

def show_data():
  global root
  root = Tk()
  root.geometry('600x600+150+20')
  root.configure(background='SlateGray3')
  root.title("Registration Form")
  
  global roll
  global name1
  global phone
  global Email
  global gender1
  global guardian_n
  global guardian_num
  global tkcourse
  global tksem

  roll=IntVar()
  name1=StringVar()
  phone=IntVar()
  Email=StringVar()
  gender1 = IntVar()
  guardian_n=StringVar()
  guardian_num=IntVar()
  tkcourse=StringVar()
  tksem=StringVar()   

  label_00 = Label(root, text="Registration form",width=20,font=("bold", 20),bg='SlateGray3')
  label_00.place(x=90,y=20)

  label_0 = Label(root, text="Enroll Id",width=20,font=("bold", 10),bg='SlateGray3')
  label_0.place(x=80,y=80)

  entry_0 = Entry(root,textvar=roll)
  entry_0.place(x=240,y=80)

  label_1 = Label(root, text="Full name",width=20,font=("bold", 10),bg='SlateGray3')
  label_1.place(x=80,y=130)

  entry_1 = Entry(root,textvar=name1)
  entry_1.place(x=240,y=130)

  label_2 = Label(root, text="Phone no",width=20,font=("bold", 10),bg='SlateGray3')
  label_2.place(x=80,y=180)

  entry_2 = Entry(root,textvar=phone)
  entry_2.place(x=240,y=180)

  label_3 = Label(root, text="Email",width=20,font=("bold", 10),bg='SlateGray3')
  label_3.place(x=80,y=230)

  entry_3 = Entry(root,textvar=Email)
  entry_3.place(x=240,y=230)

  label_4 = Label(root, text="Guardian name",width=20,font=("bold", 10),bg='SlateGray3')
  label_4.place(x=80,y=280)

  entry_4 = Entry(root,textvar=guardian_n)
  entry_4.place(x=240,y=280)

  label_5 = Label(root, text="Guardian no",width=20,font=("bold", 10),bg='SlateGray3')
  label_5.place(x=80,y=330)

  entry_5 = Entry(root,textvar=guardian_num)
  entry_5.place(x=240,y=330)

  label_6 = Label(root, text="Gender",width=20,font=("bold", 10),bg='SlateGray3')
  label_6.place(x=80,y=380)

  Radiobutton(root, text="Male", padx = 5, variable=gender1, value=1,bg='SlateGray3').place(x=235,y=380)
  Radiobutton(root, text="Female", padx = 20, variable=gender1, value=2,bg='SlateGray3').place(x=290,y=380)
  Radiobutton(root, text="others", padx = 30, variable=gender1, value=3,bg='SlateGray3').place(x=380,y=380)

  courses = { 'MCA','MBA','M. Tech'}
  tkcourse.set('MCA')

  semester={'1','2','3','4','5','6'}
  tksem.set('1')

  coursemenu = OptionMenu(root, tkcourse, *courses)
  coursemenu.configure(bg='light cyan')
  label_7=Label(root, text="Course" ,bg='SlateGray3')
  label_7.place(x=130,y=430)
  coursemenu.place(x=240,y=430)

  semmenu = OptionMenu(root, tksem, *semester)
  semmenu.configure(bg='light cyan')
  label_8=Label(root, text="Semester" ,bg='SlateGray3')
  label_8.place(x=130,y=480)
  semmenu.place(x=240,y=480)

  Button(root, text='Submit',width=15,fg='black',command=database,bg='light cyan').place(x=200,y=550)
  Button(root,text='Back',width=15,fg='black',command=back,bg='light cyan').place(x=350,y=550)  
  root.mainloop()
loginscreen() 