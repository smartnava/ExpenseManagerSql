from flask import Flask,request,session,render_template,redirect,url_for,flash
import sqlite3

app=Flask(__name__)
app.secret_key='uytf7tfjshcvslkjshfwei3u923kheh23kj389120dmcns'
sqlite3.connect(r"F:\expense\eManager.db")

def fn(name):
    conn=sqlite3.connect('eManager.db') 
    c=conn.cursor()
    c.execute(name)
    conn.commit()
    conn.close()
def ifn(name,record):
    conn=sqlite3.connect('eManager.db') 
    c=conn.cursor()
    r=record
    print(name)
    c.executemany(name,r)
    conn.commit()
    conn.close()
def rfn(name):
    conn=sqlite3.connect('eManager.db') 
    c=conn.cursor()
    c.execute(name)
    user=c.fetchone()
    conn.commit()
    conn.close()
    return user
def rfn1(name):
    conn=sqlite3.connect('eManager.db') 
    c=conn.cursor()
    c.execute(name)
    user=c.fetchall()
    conn.commit()
    conn.close()
    return user

def record():
    monthly_payment=[(1,'rent',1),(2,'phone recharge',1),(3,'TV recharges',1),(4,'app subscription',1),(5,'internet',1),(6,'gas',1),(7,'security',1),(8,'Elecricity bill',1)]
    groceries= [(1,'food',2),(2,'baby needs',2),(3,'household supplies',2),(4,'toiletries',2)]
    transportation=[(1,'fuel',3),(2,'auto/taxi',3),(3,'transit',3),(4,'parking',3),(5,'rentals',3),(6,'tolls',3)]
    health_care=[(1,'medical premiums',4),(2,'medication',4),(3,'ENT care',4),(4,'suplements',4)]
    insurance=[(1,'2-wheeler insurence',5),(2,'4-wheeler insurence',5),(3,'life insurence',5),(4,'credit card',5),(5,'housing loans',5),(6,'leases',5),(7,'government debt',5),(8,'personal debt',5)]
    bussiness_expenses=[(1,'materials',6),(2,'labour',6),(3,'taxes',6),(4,'professional or administration fees',6),(5,'human resources',6),(6,'uniform and clothings',6),(7,'parties',6),(8,'maintanance charge',6)]
    name=""" insert into """+session['username']+ """_s
            (id,subcategory,pid) values(?,?,?)"""
    ifn(name,monthly_payment)
    ifn(name,groceries)
    ifn(name,transportation)
    ifn(name,health_care)
    ifn(name,insurance)
    ifn(name,bussiness_expenses)
    
def bfun():
    fn(''' create table if not exists visitor
                (username varchar(20) not null primary key,
                password varchar(20) not null) ''')
    fn('''create table if not exists profile (
        name varchar(90) not null ,
        dob varchar(10) not null ,
        email varchar(40) not null primary key ,
        gender char(10) not null , 
        contact no integer(20) not null,
        username varchar(20) REFERENCES visitor(username));''')

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

#insert sign-in data
@app.route('/new_user', methods=['POST','GET'])
def new_visitor():
    bfun()
    fn(''' insert into visitor values('{}','{}')'''.format(request.form['username'],request.form['password']))
    return redirect(url_for('home'))
#verify log-in data
@app.route('/verify_user', methods=['POST','GET'])
def verify_user():
    user=rfn('''select * from visitor where username='{}' '''.format(request.form['username']))
    if user==None:
        print ('error')
        return redirect(url_for('home'))
    if user[1]==request.form['password'] and user[0]==request.form['username']:
        session['username']=request.form['username']
        return redirect(url_for('home'))
    return 'incorrect password'
#profile page
@app.route('/profile')
def profile():
    fn(""" create table if not exists profile (
        name varchar(90) not null ,
        dob varchar(10) not null ,
        email varchar(40) not null primary key ,
        gender char(10) not null , 
        contact no integer(20) not null,
        username varchar(20) REFERENCES visitor(username));
        """)
    fn(""" create table if not exists """+session['username']+
              """_p (id int primary key,paymenttype varchar(50) not null)""")
    fn(""" create table if not exists """+session['username']+
              """_c (p_id int primary key,category varchar(50) not null)""")
    fn(""" create table if not exists """+session['username']+ """_s
           (id int not null ,subcategory varchar(50) not null primary key,
            pid int not null ,FOREIGN KEY(pid) REFERENCES tom_category(p_id))""")
    fn(""" create table if not exists """+session['username']+
              """_d (date varchar(20) not null,
                time varchar(15) not null,paymenttype varchar(50) not null,
                transactionid varchar(50) not null,category char not null,
                subcategory char not null,amount double not null,
                note varchar(1000) not null )""")
    rec=[(1,"monthly payments"),(2,'grocery'),(3,'Transportation'),(4,'Medical Expenses'),(5,'Insurence and Loans'),(6,'Bussiness Expenses')] 
    ifn('''insert into '''+session['username']+ '''_c (p_id,category) values(?,?)''',rec)
    records=[(1,"cash"),(2,'credit card'),(3,'debit card'),(4,'phonepe'),(5,'googlepay'),(6,'bank account')]
    ifn('''insert into '''+session['username']+'''_p values(?,?)''',records)
    record()
    return render_template('profile.html')
@app.route('/pdata',methods=['POST','GET'])
def pdata():
    fn(""" insert into profile  values('{}','{}','{}','{}','{}','{}')""".format(request.form['name'],request.form['dob'],request.form['email'],request.form['gender'],request.form['contact'],session['username']))
    return redirect(url_for('ehome'))
@app.route('/ehome')
def ehome():
    
    dic={}
    category=[]
    subcategory=[]
    data1=rfn1(""" select * from """+session['username']+'_p')
    cat=rfn1(""" select * from """+session['username']+'_c')
    scat=rfn1(""" select * from """+session['username']+'_s')
    print(scat)
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
    fn(''' insert into '''+ session['username']+'''_d  values('{}','{}','{}','{}','{}','{}','{}','{}')'''
              .format(request.form['date'],request.form['time'],
                      request.form['paymenttype'],request.form['number'],
                      request.form['category'],request.form['sub'],
                      request.form['money'],request.form['note']))
    return redirect(url_for('ehome'))
@app.route('/transaction')
def history():
    lis=rfn1(''' select 
                    date,time,'''+ session['username']+'''_p.paymenttype,transactionid,'''+ session['username']+'''_c.category,'''+ session['username']+'''_s.subcategory,amount,note
                    from 
                    '''+ session['username']+'''_d
                    join 
                    '''+ session['username']+'''_p on '''+ session['username']+'''_p.id='''+ session['username']+'''_d.paymenttype
                    join 
                    '''+ session['username']+'''_c on '''+ session['username']+'''_c.p_id='''+ session['username']+'''_d.category
                    join 
                    '''+ session['username']+'''_s on  '''+ session['username']+'''_s.id='''+ session['username']+'''_d.subcategory and '''+ session['username']+'''_s.pid='''+ session['username']+'''_c.p_id ''')
    return render_template('history.html',rows=lis)
@app.route('/filter',methods=['POST','GET'])
def filter():
    if(request.form['type']=='date'):
        lis=rfn1(''' select 
                    date,time,'''+ session['username']+'''_p.paymenttype,transactionid,'''+ session['username']+'''_c.category,'''+ session['username']+'''_s.subcategory,amount,note
                    from 
                    '''+ session['username']+'''_d
                    join 
                    '''+ session['username']+'''_p on '''+ session['username']+'''_p.id='''+ session['username']+'''_d.paymenttype
                    join 
                    '''+ session['username']+'''_c on '''+ session['username']+'''_c.p_id='''+ session['username']+'''_d.category
                    join 
                    '''+ session['username']+'''_s on  '''+ session['username']+'''_s.id='''+ session['username']+'''_d.subcategory and '''+ session['username']+'''_s.pid='''+ session['username']+'''_c.p_id 
                      where date>='{}' and date<='{}' '''.format(request.form['from'],request.form['to']))
    else:
        if 'paymenttype'==request.form['type']:
            a=session['username']+'_p.paymenttype'
        elif 'category'==request.form['type']:
            a=session['username']+'_c.category'
        else:
            a=session['username']+'_s.subcategory'
        print(a)
        lis=rfn1('''select 
                    date,time,'''+ session['username']+'''_p.paymenttype,transactionid,'''+ session['username']+'''_c.category,'''+ session['username']+'''_s.subcategory,amount,note
                    from 
                    '''+ session['username']+'''_d
                    join 
                    '''+ session['username']+'''_p on '''+ session['username']+'''_p.id='''+ session['username']+'''_d.paymenttype
                    join 
                    '''+ session['username']+'''_c on '''+ session['username']+'''_c.p_id='''+ session['username']+'''_d.category
                    join 
                    '''+ session['username']+'''_s on '''+ session['username']+'''_s.id='''+ session['username']+'''_d.subcategory and '''+ session['username']+'''_s.pid='''+ session['username']+'''_c.p_id 
                      where {}='{}' '''.format(a,request.form['value']))
    return render_template('history.html',rows=lis)
app.run(debug=True)



