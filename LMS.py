import mysql.connector
import os
import pickle

def display_bk():
    s="*"
    print(s*20)
    print("       GENRE:")
    print(s*20)
    print("1: All genres")
    print("2: Fiction")
    print("3: Horror")
    print("4: Non-Fiction")
    print("5: Romance")
    print("6: Fantasy")
    print("7: Mystery")
    try:
            mycon=mysql.connector.connect(host='localhost',user='root',passwd='girlpower',database='library_management')
            mycur=mycon.cursor()
            print()
            ch=int(input("Kindly enter a genre:"))
            print()
            if ch==1:
                print('\t','\t','\t',"~~ BOOK LIST ~~")
                mycur.execute('select * from books')
            elif ch==2:
                print('\t','\t','\t',"~~ FICTION CORNER ~~")
                mycur.execute('select * from books where genre="Fiction"')
            elif ch==3:
                print('\t','\t','\t',"~~ HORROR CORNER ~~")
                mycur.execute('select * from books where genre="Horror"')
            elif ch==4:
                print('\t','\t','\t',"~~ NON-FICTION CORNER ~~")
                mycur.execute('select * from books where genre="Non-fiction"')
            elif ch==5:
                print('\t','\t','\t',"~~ ROMANCE CORNER ~~")
                mycur.execute('select * from books where genre="Romance"')
            elif ch==6:
                print('\t','\t','\t',"~~ FANTASY ~~")
                mycur.execute('select * from books where genre="Fantasy"')
            elif ch==7:
                print('\t','\t','\t',"~~ MYSTERY ~~") 
                mycur.execute('select * from books where genre="Mystery"')
            rs=mycur.fetchall()
            s="*"
            print(s*72)
            print('|','%7s'%'Book no.','|','%18s'%'Book name','|','%20s'%'Author','|','%15s'%'Genre''|')
            print(s*72)
            for r in rs:
                print('|','%7s'%r[0],'|','%19s'%r[1],'|','%20s'%r[2],'|','%13s'%r[3],'|')
            print(s*72)    
    except Exception as e:
            print(e)
            
    mycur.close()
    mycon.close()


def insert_user_record(un,pw):
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='girlpower',database='library_management')
        mycur=mycon.cursor()
        sname=input("Enter name:")
        sgrade=int(input("Enter grade:"))
        sgen=input("Enter gender:")
        issue_date=input("Enter date of issue:")
        bno1=0
        bno2=0
        rb=0
        mycur.execute("insert into students values('{}',{},'{}',{},{},{},'{}','{}','{}')".format(sname,sgrade,issue_date,bno1,bno2,rb,sgen,un,pw))
        mycon.commit()
    except Exception as e:
        print(e)
    print()
    print("--- ACCOUNT CREATED SUCCESSFULLY ---")
    print()
    
    mycur.close()
    mycon.close()


def borrow_bk(un):
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='girlpower',database='library_management')
        mycur=mycon.cursor()
        print()
        q="select*from students where username='{}'".format(un)
        mycur.execute(q)
        rs=mycur.fetchone()  
        display_bk()
        print()
        bk=int(input("Enter book no. of desired book:"))
        h="select*from books where Bno={}".format(bk)
        mycur.execute(h)
        br=mycur.fetchone()
        if br[4]==0:
            print()
            print("!!! NO COPIES AVALIABLE !!!")
            borrow_bk(un)
        elif rs[3]==0:
            mycur.execute("update students set bno1={},rb=rb+1 where username='{}'".format(bk,un))
            print()
            print("--- BOOK BORROWED ---")
            print()
            a="update books set Copies=Copies-1 where bno={}".format(bk)    
            mycur.execute(a)
            mycon.commit()
        elif rs[4]==0:
            rb=2
            mycur.execute("update students set bno2={},rb=rb+1 where username='{}'".format(bk,un))
            print()
            print("--- BOOK BORROWED ---")
            print()
            a="update books set Copies=Copies-1 where bno={}".format(bk)    
            mycur.execute(a)
            mycon.commit()
        else:
            print()
            print("!!! ONLY TWO BOOKS CAN BE BORROWED !!!")
            print()
    except Exception as e:
        print(e)
        
    mycur.close()
    mycon.close()

 
def return_bk(un):
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='girlpower',database='library_management')
        mycur=mycon.cursor()
        q="select*from students where username='{}'".format(un)
        mycur.execute(q)
        rs=mycur.fetchone()  
        z1=rs[3]
        z2=rs[4]
        s="-"
        if z1==0 and z2==0:
            print()
            print("!!! YOU DON'T OWN ANY BOOKS !!!")
            return
        print()
        print("     ~~ BOOKS OWNED ~~")
        print(s*33)
        print('|','%7s'%'Book no.','|','%18s'%'Book name','|')
        print(s*33)
        if z1!=0:
            mycur.execute("select bno,bname from books where bno={}".format(z1))
            cs=mycur.fetchone()
            print('|','%8s'%cs[0],'|','%18s'%cs[1],'|')
        if z2!=0:
            mycur.execute("select bno,bname from books where bno={}".format(z2))
            bs=mycur.fetchone()
            print('|','%8s'%bs[0],'|','%18s'%bs[1],'|')
        print(s*33)    
        print()
        bk=int(input("Enter book no. of book to be returned:"))
        if rs[3]==bk:
            b=0
            mycur.execute("update students set bno1={},rb=rb-1 where username='{}'".format(b,un))
            print()
            print("--- BOOK RETURNED ---")
            a="update books set Copies=Copies+1 where bno={}".format(bk)    
            mycur.execute(a)
            mycon.commit()
        elif rs[4]==bk:
            b=0
            mycur.execute("update students set bno2={},rb=rb-1 where username='{}'".format(b,un))
            print("--- BOOK RETURNED ---")
            a="update books set Copies=Copies+1 where bno={}".format(bk)    
            mycur.execute(a)
            mycon.commit()
        else:
            print("!!! YOU DO NOT OWN THIS BOOK !!!")     
    except Exception as e:
        print(e)
    
    mycur.close()
    mycon.close()


def lost_bk(un):
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='girlpower',database='library_management')
        mycur=mycon.cursor()
        q="select*from students where username='{}'".format(un)
        mycur.execute(q)
        rs=mycur.fetchone()  
        z1=rs[3]
        z2=rs[4]
        s="-"
        print()
        print("    ~~ BOOKS OWNED ~~")
        print(s*33)
        print('|','%7s'%'Book no.','|','%18s'%'Book name','|')
        print(s*33)
        if z1!=0:
            mycur.execute("select bno,bname from books where bno={}".format(z1))
            cs=mycur.fetchone()
            print('|','%8s'%cs[0],'|','%18s'%cs[1],'|')
        if z2!=0:
            mycur.execute("select bno,bname from books where bno={}".format(z2))
            bs=mycur.fetchone()
            print('|','%8s'%bs[0],'|','%18s'%bs[1],'|')
        print(s*33)    
        print()
        bk=int(input("Enter book no. of lost book :"))
        if rs[3]==bk:
            b=0
            mycur.execute("update students set bno1={},rb=rb-1 where username='{}'".format(b,un))
            mycon.commit()
            print()
            p="select bno,bname,rate,rate+(rate/2) from books where bno={}".format(bk)
            mycur.execute(p)
            qr=mycur.fetchone()
            s="*"
            print('\t','\t','\t',"     ~~ FINE ~~")
            print(s*70)
            print('|','%7s'%'Book no.','|','%18s'%'Book name','|','%18s'%'Original price','|','%13s'%'Fine','|')
            print(s*70)
            print('|','%8s'%qr[0],'|','%18s'%qr[1],'|','%18s'%qr[2],'|','%13s'%qr[3],'|')
            print(s*70)  
        elif rs[4]==bk:
            b=0
            mycur.execute("update students set bno2={},rb=rb-1 where username='{}'".format(b,un))
            mycon.commit()
            print()
            p="select bno,bname,rate,rate+(rate/2) from books where bno={}".format(bk)
            mycur.execute(p)
            qr=mycur.fetchone()
            s="*"
            print('\t','\t','\t',"     ~~ FINE ~~")
            print(s*70)
            print('|','%7s'%'Book no.','|','%18s'%'Book name','|','%18s'%'Original price','|','%13s'%'Fine','|')
            print(s*70)
            print('|','%8s'%qr[0],'|','%18s'%qr[1],'|','%18s'%qr[2],'|','%13s'%qr[3],'|')
            print(s*70)
        else:
            print("!!! YOU DO NOT OWN THIS BOOK !!!")     
    except Exception as e:
        print(e)
    
    
    mycur.close()
    mycon.close()

 
def update_acc_details(un):
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='girlpower',database='library_management')
        mycur=mycon.cursor()
        q="select*from students where username='{}'".format(un)
        mycur.execute(q)
        rs=mycur.fetchone()
        if rs==None:
            print("!!! ACCOUNT DOESNT EXIST !!!")
        else:
            print(rs)
            print()
            name=input('Enter new name:')
            date=input("Enter new date of issue:")
            grade=int(input('Enter new grade:'))
            passwd=input('Enter new password:')
            a="update students set sname='{}',issue_date='{}',sgrade={},password='{}' where username='{}'".format(name,date,grade,passwd,un)
            mycur.execute(a)
            rec=[]
            found=0
            f=open("Registration.dat","rb")
            f1=open("Temp.dat","wb")
            while True:
                try:
                    rec=pickle.load(f)
                    if rec[0]==un:
                        rec[1]=passwd
                        found=1
                    pickle.dump(rec,f1)
                except EOFError:
                    f.close()
                    f1.close()
                    if found==0:
                        print(seno,"does not exist")
                    break
            os.remove("Registration.dat")
            os.rename("Temp.dat","Registration.dat")
            print()
            print("--- RECORD UPDATED ---")
            mycon.commit()
    except Exception as e:
        print(e)
        
    mycur.close()
    mycon.close()    


def display_bk_borrowed(un):
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='girlpower',database='library_management')
        mycur=mycon.cursor()
        q="select*from students where username='{}'".format(un)
        mycur.execute(q)
        rs=mycur.fetchone()  
        z1=rs[3]
        z2=rs[4]
        s="-"
        print()
        print("     ~~ BOOKS OWNED ~~")
        print(s*30)
        print('%7s'%'Book no.','%18s'%'Book name')
        print(s*30)
        if z1!=0:
            mycur.execute("select bno,bname from books where bno={}".format(z1))
            cs=mycur.fetchone()
            print('|','%7s'%cs[0],'|','%18s'%cs[1],'|')
        if z2!=0:
            mycur.execute("select bno,bname from books where bno={}".format(z2))
            bs=mycur.fetchone()
            print('|','%7s'%bs[0],''|',%18s'%bs[1],'|')
        print(s*30)
        print()
    except Exception as e:
        print(e)
    
    mycur.close()
    mycon.close()


def delete_acc_b():
    rec=[]
    found=0
    f=open("Registration.dat","rb")
    f1=open("Temp.dat","wb")
    print()
    n=input("Enter name of user to be deleted:")
    while True:
        try:
            rec=pickle.load(f)
            if rec[0]!=n:
                found=1
                pickle.dump(rec,f1)
        except EOFError:
            f.close()
            f1.close()
            if found==0:
                print()
                print(n,"!!! DOES NOT EXIST !!!")
            break
    os.remove("Registration.dat")
    os.rename("Temp.dat","Registration.dat")
    print()
 
 
def delete_acc(un):
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='girlpower',database='library_management')
        mycur=mycon.cursor()
        q="select*from students where username='{}'".format(un)
        mycur.execute(q)
        rs=mycur.fetchone()
        print(rs)
        if rs[5]!=0:
            print()
            print("!!! BOOKS NEED TO BE RETURNED BEFORE DELETING ACCOUNT !!!")
            print()
            try:
                mycon=mysql.connector.connect(host='localhost',user='root',passwd='girlpower',database='library_management')
                mycur=mycon.cursor()
                q="select*from students where username='{}'".format(un)
                mycur.execute(q)
                rs=mycur.fetchone() 
                z1=rs[3]
                z2=rs[4]
                s="-"
                print()
                print("     ~~ BOOKS OWNED ~~")
                print(s*30)
                print('%7s'%'Book no.','%18s'%'Book name')
                print(s*30)
                if z1!=0:
                    mycur.execute("select bno,bname from books where bno={}".format(z1))
                    cs=mycur.fetchone()
                    print('|','%7s'%cs[0],'|','%18s'%cs[1],'|')
                if z2!=0:
                    mycur.execute("select bno,bname from books where bno={}".format(z2))
                    bs=mycur.fetchone()
                    print('|','%7s'%bs[0],'|','%18s'%bs[1],'|')
                print(s*30)
                print(rs)
                print()
                bk1=input("Enter bno of book1 to be returned:")
                bk2=input("Enter bno of book2 to be returned:")
                mycur.execute("update books set Copies=Copies+1 where bno={}".format(bk1))
                mycur.execute("update books set Copies=Copies+1 where bno={}".format(bk2))
            except Exception as e:
                print(e)
        q='delete from students where username="{}"'.format(un)
        mycur.execute(q)
        mycon.commit()
        delete_acc_b()
        print('--- ACCOUNT DELETED ---')
        print()
        print(" ~~ see you soon ~~ ")
    except Exception as e:
        print(e)
        mycon.rollback()
        
    mycur.close()
    mycon.close()

        
def options(un):
    while True:
        print()
        print()
        s='*'
        print(s*44)
        print('\t','WHAT WOULD YOU LIKE TO DO?')
        print(s*44)
        print()
        print('1: Display Books')
        print('2: Borrow Books')
        print('3: Return Books')
        print('4: Lost book?')
        print('5: Update Account Details')
        print('6: Display books borrowed')
        print('7: Delete Account')
        print('8: Exit')
        print()
        ch=int(input('Enter a choice:'))
        print()
        if ch==1:
            display_bk()
        elif ch==2:
            borrow_bk(un)
        elif ch==3:
            return_bk(un)
        elif ch==4:
            lost_bk(un)
        elif ch==5:
            update_acc_details(un)
        elif ch==6:
            display_bk_borrowed(un)
        elif ch==7:
            delete_acc(un)
            break
        elif ch==8:
            print(" ~~ see you soon ~~ ") 
            break
        
  
def sign_up():
    f=open("Registration.dat","rb")
    un=input("Enter username:")
    rec=[]
    found=0
    while True:
        try:
            rec=pickle.load(f)
            if rec[0]==un:
                found=1
                print("!!! USERNAME ALREADY EXISTS. TRY A NEW USERNAME. !!!")
                break
        except EOFError:
            f.close()
            break
    if found==0:
         f=open("Registration.dat","ab")
         pw=input("Enter password:")
         rec=[un,pw]
         pickle.dump(rec,f)
         f.close()
         insert_user_record(un,pw)
         options(un)


def sign_in():
    f=open("Registration.dat","rb")
    un=input("Enter username:")
    password=input("Enter password:")
    found=0
    while True:
        try:
            rec=pickle.load(f)
            if rec[0]==un and rec[1]==password:
                f.close()
                found=1
                options(un)
                break
        except EOFError:
            if found==0:
                print()
                print("!!! ACCOUNT NOT FOUND !!!")
                break
 
def student():
    while True:
        print()
        print("1: Sign up")
        print("2: Sign in")
        print()
        ch=int(input("Enter choice:"))
        print()
        if ch==1:
            sign_up()
            break
        if ch==2:
            sign_in()
            break

def add_bk_ad():
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='girlpower',database='library_management')
        mycur=mycon.cursor()
        bno=int(input("Enter book no."))
        bname=input("Enter book name:")
        au=input("Enter author's name:")
        genre=input("Enter genre:")
        co=int(input("Enter no. of copies:"))
        rate=float(input("Enter cost of the book:"))
        mycur.execute("insert into books values({},'{}','{}','{}',{},{})".format(bno,bname,au,genre,co,rate))
        mycon.commit()
    except Exception as e:
        print(e)
    print()
    print("--- BOOK ADDED SUCCESSFULLY ---")
    print()
    
    mycur.close()
    mycon.close()
 
def update_bk_ad():
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='girlpower',database='library_management')
        mycur=mycon.cursor()
        try:
            mycon=mysql.connector.connect(host='localhost',user='root',passwd='girlpower',database='library_management')
            mycur=mycon.cursor()
            print('\t','\t','\t',"~~ BOOK LIST ~~")
            mycur.execute('select * from books')
            rs=mycur.fetchall()
            s="*"
            print(s*70)
            print('|','%7s'%'Book no.','|','%18s'%'Book name','|','%18s'%'Author','|','%13s'%'Genre','|')
            print(s*70)
            for r in rs:
                print('|','%7s'%r[0],'|','%18s'%r[1],'|','%20s'%r[2],'|','%13s'%r[3],'|')
            print(s*70)    
        except Exception as e:
                print(e)
        no=int(input("Enter Bno of book to be updated:"))
        q="select*from books where Bno={}".format(no)
        mycur.execute(q)
        rs=mycur.fetchone()
        if rs==None:
            print("!!! BOOK DOESNT EXIST !!!")
        else:
            print(rs)
            print()
            bno=int(input("Enter book no."))
            bname=input("Enter book name:")
            au=input("Enter author's name:")
            genre=input("Enter genre:")
            co=int(input("Enter no. of copies:"))
            rate=float(input("Enter cost of the book:"))
            a="update books set Bno={},Bname='{}',Author='{}',Genre='{}',Copies={},Rate={} where Bno={}".format(bno,bname,au,genre,co,rate,no)
            mycur.execute(a)
            print()
            print("--- RECORD UPDATED ---")
            mycon.commit()
    except Exception as e:
        print(e)
        
    mycur.close()
    mycon.close()    

def search_bno_owner():
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='girlpower',database='library_management')
        mycur=mycon.cursor()
        try:
            mycon=mysql.connector.connect(host='localhost',user='root',passwd='girlpower',database='library_management')
            mycur=mycon.cursor()
            print('\t','\t','\t',"~~ BOOK LIST ~~")
            mycur.execute('select * from books')
            rs=mycur.fetchall()
            s="*"
            print(s*70)
            print('|','%7s'%'Book no.','|','%18s'%'Book name','|','%18s'%'Author','|','%13s'%'Genre','|')
            print(s*70)
            for r in rs:
                print('|','%7s'%r[0],'|','%18s'%r[1],'|','%20s'%r[2],'|','%13s'%r[3],'|')
            print(s*70)    
        except Exception as e:
                print(e)
        no=int(input('Enter book no. to be searched:'))
        print()
        q="select * from students where bno1=%s or bno2=%s"%(no,no)
        mycur.execute(q)
        rs=mycur.fetchall()
        if rs==[]:
            print('!!! NO RECORDS !!!')
        else:
            s='-'
            print(s*34)
            print('|',"%3s"%"Name",'|',"%10s"%"Grade",'|',"%7s"%"Issue Date",'|')
            print(s*34)
            for r in rs:
                print('|',"%3s"%r[0],'|',"%10s"%r[1],'|',"%7s"%r[2],'|')
                print(s*34)
        mycon.commit()
        print()
    except Exception as e:
        print(e)
    
    mycur.close()
    mycon.close()



def delete_bk_ad():
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='girlpower',database='library_management')
        mycur=mycon.cursor()
        try:
            mycon=mysql.connector.connect(host='localhost',user='root',passwd='girlpower',database='library_management')
            mycur=mycon.cursor()
            print('\t','\t','\t',"~~ BOOK LIST ~~")
            mycur.execute('select * from books')
            rs=mycur.fetchall()
            s="*"
            print(s*70)
            print('|','%7s'%'Book no.','|','%18s'%'Book name','|','%18s'%'Author','|','%13s'%'Genre','|')
            print(s*70)
            for r in rs:
                print('|','%7s'%r[0],'|','%18s'%r[1],'|','%20s'%r[2],'|','%13s'%r[3],'|')
            print(s*70)    
        except Exception as e:
                print(e)
        no=int(input('Enter bno of book to be deleted:'))
        q="select*from books where Bno={}".format(no)
        mycur.execute(q)
        rs=mycur.fetchone()
        print(rs)
        q='delete from books where Bno={}'.format(no)
        mycur.execute(q)
        mycon.commit()
        print()
        print('--- BOOK DELETED ---')
    except Exception as e:
        print(e)
        mycon.rollback()
        
    mycur.close()
    mycon.close()



def options_ad():
    while True:
        print()
        print()
        s='*'
        print(s*44)
        print('\t','WHAT WOULD YOU LIKE TO DO?')
        print(s*44)
        print()
        print('1: Display Books')
        print('2: Add Books')
        print('3. Update Book record')
        print('4. Delete Book')
        print('5. Search book owner')
        print('6: Exit')
        print()
        ch=int(input('Enter a choice:'))
        print()
        if ch==1:
            display_bk()
        elif ch==2:
            add_bk_ad()
        elif ch==3:
            update_bk_ad()
        elif ch==4:
            delete_bk_ad()
        elif ch==5:
            search_bno_owner()
        elif ch==6:
            print(" ~~ Exited ~~ ")
            break
    

def admin():
    p=1234
    password=int(input("Enter password:"))
    if p==password:
        options_ad()
    else:
        print(" !!! WRONG PASSWORD !!! ")
        return
     

while True:
    s='*'
    print(s*40)
    print('\t'," Weclome to Anavrin",'\t')
    print(s*40)
    print()
    print("1. Admin")
    print("2. Student")
    print()
    c=int(input("Enter option:"))
    if c==1:
        admin()
        break
    if c==2:
        student()
        break
          