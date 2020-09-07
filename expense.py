from flask import Flask,request,session,render_template,redirect,url_for,flash
import sqlite3

app=Flask(__name__)
app.secret_key='uytf7tfjshcvslkjshfwei3u923kheh23kj389120dmcns'
sqlite3.connect(r"G:\expense\edbjoin.db")

#create visitor username password
def create_visitor():
    conn=sqlite3.connect('edbjoin.db') 
    c=conn.cursor()
    c.execute(''' create table if not exists visitor
                (username varchar(20) not null primary key,
                password varchar(20) not null) ''')
    conn.commit()
    conn.close()
create_visitor()    
#insert visitor data
def insert_visitor():
    create_visitor()
    conn=sqlite3.connect('edbjoin.db')
    c=conn.cursor()
    c.execute(''' insert into visitor values('{}','{}')'''.format(request.form['username'],request.form['password']))
    conn.commit()
    conn.close()
#display visitor username/password
def display_up():
    conn=sqlite3.connect('edbjoin.db')
    c=conn.cursor()
    c.execute('''select * from visitor''')
    up=c.fetchall()
    for up in up:
        print(up)
    conn.close()
#profile page
def create_profile():
    conn=sqlite3.connect('edbjoin.db')
    c=conn.cursor()
    c.execute(""" create table if not exists profile (
        name varchar(90) not null ,
        dob varchar(10) not null ,
        email varchar(40) not null primary key ,
        gender char(10) not null , 
        contact no integer(20) not null,
        username varchar(20) REFERENCES visitor(username));
        """)
    conn.commit()
    conn.close()

def insert_profiledata():
    try:
        conn=sqlite3.connect('edbjoin.db')
        c=conn.cursor()
        c.execute(""" insert into profile  values('{}','{}','{}','{}','{}','{}')""".format(request.form['name'],request.form['dob'],request.form['email'],request.form['gender'],request.form['contact'],session['username']))
        flash('profile data added')
    except sqlite3.IntegrityError as e:
        flash('email id already exists.so login')
        c='one'
        return c
    else:
       conn.commit()
       conn.close()
       c=0
       return c    
def display_pd():    
    conn=sqlite3.connect('edbjoin.db')
    c=conn.cursor()
    c.execute(""" select * from profile; """)
    data=c.fetchall()
    for data in data:
        print(data)
    conn.commit()
    conn.close()
#database for expense page
 
def payment_type():
    conn=sqlite3.connect('edbjoin.db')
    c=conn.cursor()
    c.execute(""" create table if not exists """+session['username']+
              """_paymenttype (id int primary key,paymenttype varchar(50) not null)""")
    conn.commit()
    conn.close()
def ipayment_type():
    conn=sqlite3.connect('edbjoin.db')
    c=conn.cursor()
    records=[(1,"cash"),(2,'credit card'),(3,'debit card'),(4,'phonepe'),(5,'googlepay'),(6,'bank account')]
    c.executemany(""" insert into """+session['username']+"""_paymenttype values(?,?);""",records)
    conn.commit()
    conn.close()  
def category():
    conn=sqlite3.connect('edbjoin.db')
    c=conn.cursor()
    c.execute(""" create table if not exists """+session['username']+
              """_category (p_id int primary key,category varchar(50) not null)""")
    conn.commit()
    conn.close()
def icategory_type():
    conn=sqlite3.connect('edbjoin.db')
    c=conn.cursor()
    record=[(1,"monthly payments"),(2,'grocery'),(3,'Transportation'),(4,'Medical Expenses'),(5,'Insurence and Loans'),(6,'Bussiness Expenses')]
    c.executemany(""" insert into """+session['username']+ """_category
            (p_id,category) values(?,?)""",record)
    conn.commit()
    conn.close()   
def subcategory():
    conn=sqlite3.connect('edbjoin.db')
    c=conn.cursor()
    c.execute(""" create table if not exists """+session['username']+ """_subcategory
    (id int not null ,subcategory varchar(50) not null primary key,
    pid int not null ,FOREIGN KEY(pid) REFERENCES tom_category(p_id))""")
    conn.commit()
    conn.close()
#subcategory declaration
def isubcategory_type(record):
    conn=sqlite3.connect('edbjoin.db')
    c=conn.cursor()
    
    c.executemany(""" insert into """+session['username']+ """_subcategory
            (id,subcategory,pid) values(?,?,?)""",record)
    conn.commit()
    conn.close()
#records:
def record():
    monthly_payment=[(1,'rent',1),(2,'phone recharge',1),(3,'TV recharges',1),(4,'app subscription',1),(5,'internet',1),(6,'gas',1),(7,'security',1),(8,'Elecricity bill',1)]
    groceries= [(1,'food',2),(2,'baby needs',2),(3,'household supplies',2),(4,'toiletries',2)]
    transportation=[(1,'fuel',3),(2,'auto/taxi',3),(3,'transit',3),(4,'parking',3),(5,'rentals',3),(6,'tolls',3)]
    health_care=[(1,'medical premiums',4),(2,'medication',4),(3,'ENT care',4),(4,'suplements',4)]
    insurance=[(1,'2-wheeler insurence',5),(2,'4-wheeler insurence',5),(3,'life insurence',5),(4,'credit card',5),(5,'housing loans',5),(6,'leases',5),(7,'government debt',5),(8,'personal debt',5)]
    bussiness_expenses=[(1,'materials',6),(2,'labour',6),(3,'taxes',6),(4,'professional or administration fees',6),(5,'human resources',6),(6,'uniform and clothings',6),(7,'parties',6),(8,'maintanance charge',6)]                               
    isubcategory_type(monthly_payment)
    isubcategory_type(groceries)
    isubcategory_type(transportation)
    isubcategory_type(health_care)
    isubcategory_type(insurance)
    isubcategory_type(bussiness_expenses)
    print("sucess")

#other works
def delete():
    conn=sqlite3.connect('edbjoin.db')
    c=conn.cursor()
    c.execute(""" drop table tom_details""")
    dat=c.fetchall()
    conn.commit()
    conn.close()
    print("table deleted")

def display_pt(name):
    conn=sqlite3.connect('edbjoin.db')
    c=conn.cursor()
    c.execute(""" select * from """+name)
    dat=c.fetchall()
    conn.commit()
    conn.close()
    return dat
def count():
    conn=sqlite3.connect('edbjoin.db')
    c=conn.cursor()
    c.execute('''select count (p_id) from tom_category; ''')
    count=c.fetchone()
    conn.commit()
    conn.close()
    return count
#submit expense data
def details():
    conn=sqlite3.connect('edbjoin.db')
    c=conn.cursor()
    c.execute(""" create table if not exists """+session['username']+
              """_details (date varchar(20) not null,
                time varchar(15) not null,paymenttype varchar(50) not null,
                transactionid varchar(50) not null,category char not null,
                subcategory char not null,amount double not null,
                note varchar(1000) not null )""")
    conn.commit()
    conn.close() 
def insert():
    conn=sqlite3.connect('edbjoin.db')
    c=conn.cursor()
    c.execute(''' insert into '''+ session['username']+'''_details  values('{}','{}','{}','{}','{}','{}','{}','{}')'''
              .format(request.form['date'],request.form['time'],
                      request.form['paymenttype'],request.form['number'],
                      request.form['category'],request.form['sub'],
                      request.form['money'],request.form['note']))
    conn.commit()
    conn.close()


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('login'))
@app.route('/new_user', methods=['POST','GET'])
def new_visitor():
    insert_visitor()
    return render_template('login.html')
@app.route('/verify_user', methods=['POST','GET'])
def verify_user():
    conn=sqlite3.connect('edbjoin.db')
    c=conn.cursor()
    c.execute('''select * from visitor where username='{}' '''.format(request.form['username']))
    user=c.fetchone()

    if user==None:
        print ('error')
        return redirect(url_for('signin'))
    if user[1]==request.form['password'] and user[0]==request.form['username']:
        session['username']=request.form['username']
        return redirect(url_for('home'))
    conn.close()
    return 'incorrect password'
#profile page
@app.route('/profile')
def profile():
    create_profile()
    
    payment_type()
    category()
    subcategory()
    details()
    ipayment_type()
    icategory_type()
    record()
    return render_template('profile.html')
@app.route('/pdata',methods=['POST','GET'])
def pdata():
    create_profile()
    c=insert_profiledata()
    return redirect(url_for('ehome'))
#expense page

@app.route('/ehome')
def ehome():
    
    dic={}
    category=[]
    subcategory=[]
    data1=display_pt(session['username']+'_paymenttype')
    cat=display_pt(session['username']+'_category')
    scat=display_pt(session['username']+'_subcategory')
    c=len(cat)
    s=len(scat)
    for k in range(c):
        category.append(cat[k])
        li=[]
        for i in range(s):
            k=k+1
            if scat[i][2]==k:
                li.append(scat[i])
            k=k-1
        subcategory.append(li)    
    return render_template('expense.html',category=category,subcategory=subcategory,data1=data1)
@app.route('/expensedata',methods=['POST','GET'])
def expense():
    details()
    insert()
    return redirect(url_for('ehome'))

@app.route('/transaction')
def history():
    conn=sqlite3.connect('edbjoin.db')
    c=conn.cursor()
    c.execute(''' select * from tom_details ''')
    a=c.fetchall()
    
    c.execute(''' select tom_paymenttype.paymenttype from tom_paymenttype
                    INNER JOIN tom_details ON
                    tom_paymenttype.id=tom_details.paymenttype''')
    b=c.fetchall()
    c.execute(''' select tom_category.category  from tom_category
                    INNER JOIN tom_details ON tom_category.p_id=tom_details.category''')
    d=c.fetchall()
    c.execute(''' select tom_subcategory.subcategory from tom_subcategory
                    inner join tom_details on tom_details.category=tom_subcategory.pid and
                    tom_details.category=tom_subcategory.id ''')
    e=c.fetchall()
    lis=[]*len(a[0])
    for x in range(len(a)):         
            li=(a[x][0],a[x][1],b[x][0],a[x][3],d[x][0],e[x][0],a[x][6],a[x][7])
            lis.append(li)
    conn.commit()
    conn.close()
    return render_template('history.html',rows=lis)

@app.route('/filter',methods=['POST','GET'])
def filter():
    s1=request.form['from']
    s2=request.form['to']
    conn=sqlite3.connect('edbjoin.db')
    c=conn.cursor()
    c.execute(""" select * from """+session['username']+"""_details where date>='{}' and date<='{}'""".format(request.form['from'],request.form['to']))
    a=c.fetchall()
    
    c.execute(''' select tom_paymenttype.paymenttype from tom_paymenttype
                    INNER JOIN tom_details ON
                    tom_paymenttype.id=tom_details.paymenttype''')
    b=c.fetchall()
    c.execute(''' select tom_category.category  from tom_category
                    INNER JOIN tom_details ON tom_category.p_id=tom_details.category''')
    d=c.fetchall()
    c.execute(''' select tom_subcategory.subcategory from tom_subcategory
                    inner join tom_details on tom_details.category=tom_subcategory.pid and
                    tom_details.category=tom_subcategory.id ''')
    e=c.fetchall()
    lis=[]
    for x in range(len(a)):         
            li=(a[x][0],a[x][1],b[x][0],a[x][3],d[x][0],e[x][0],a[x][6],a[x][7])
            lis.append(li)
    conn.commit()
    conn.close()
    return render_template('history.html',rows=lis)


def ed():
    conn=sqlite3.connect('edbjoin.db')
    c=conn.cursor()
    c.execute(''' select * from tom_details ''')
    a=c.fetchall()
    
    c.execute(''' select tom_paymenttype.paymenttype from tom_paymenttype
                    INNER JOIN tom_details ON
                    tom_paymenttype.id=tom_details.paymenttype''')
    b=c.fetchall()
    c.execute(''' select tom_category.category  from tom_category
                    INNER JOIN tom_details ON tom_category.p_id=tom_details.category''')
    d=c.fetchall()
    c.execute(''' select tom_subcategory.subcategory from tom_subcategory
                    inner join tom_details on tom_details.category=tom_subcategory.pid and
                    tom_details.category=tom_subcategory.id ''')
    e=c.fetchall()
    lis=[]
    for x in range(len(a)):         
            li=(a[x][0],a[x][1],b[x][0],a[x][3],d[x][0],e[x][0],a[x][6],a[x][7])
            lis.append(li)
    print(a)
    print(lis)    

    conn.commit()
    conn.close()

def oldfilter():
    s1=request.form['from']
    s2=request.form['to']
    conn=sqlite3.connect('edbjoin.db')
    c=conn.cursor()
    c.execute(""" select * from """+session['username']+"""_details where date>='{}' and date<='{}'""".format(request.form['from'],request.form['to']))
    rows = c.fetchall()
    conn.commit()
    conn.close()
    return render_template('history.html',rows=rows)

app.run(debug=True)


