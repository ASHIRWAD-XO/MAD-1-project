from flask import Flask ,render_template, redirect,request,session,abort ,jsonify
from models import *


app = Flask(__name__)

app.secret_key='login'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'

db.init_app(app)
app.app_context().push()

#-------------home page----------------------

@app.route('/')
def home():
    return render_template("index.html")

#-----------registraion----------------

@app.route('/influencer_regis')
def i_regis():
    return render_template("influencer_regis.html")

@app.route('/sponsor_regis')
def s_regis():
    return render_template("sponsor_regis.html")


@app.route('/i_regis',methods=['POST','GET'])       #influencer data to database
def influ_regis():
    if (request.form['psw']==request.form['repsw']):
        name=request.form['namee']
        username=request.form['username']
        email=request.form['email']
        psw=request.form['psw']
        number=request.form['number']
        social=request.form['social']
        followers=request.form['followers']
        i1=Influencer(iname=name,usename=username,email=email,password=psw,platform=social,number=number,reach=followers,flag=False)
        db.session.add(i1)
        db.session.commit()
        #print('success')
        return redirect('login')
    else:
        return 'confirmation passwords does not match'

@app.route('/s_regis',methods=['POST','GET'])       #sponsor data to database
def spnsr_regis():
    if (request.form['psw']==request.form['repsw']):
        name=request.form['namee']
        username=request.form['uname']
        email=request.form['email']
        psw=request.form['psw']
        number=request.form['number']
        industry=request.form['industry']
        s1=Sponsor(sname =name,usename =username,email =email,password =psw,industry =industry,number =number,flag =False)
        db.session.add(s1)
        db.session.commit()
        print('success')
        return redirect("login")
    else:
        return 'confirmation passwords does not match'
#-------------------test page----------
@app.route('/test')
def test():
    influ=Influencer.query.all()
    sp=Sponsor.query.all()
    return render_template('testveiw.html',influ=influ,sp=sp)

@app.route('/t2')
def t2():
    influ=Influencer.query.all()
    return render_template("t2.html",camp=influ)

#-------------------general login------------


@app.route('/login')
def genlogin():
    return render_template("general_login.html")


@app.route('/log',methods=['GET','POST'])       #login data
def logdata():
    uname=request.form['uname']
    psw=request.form['psw']
    print(uname,psw)
    
    if Influencer.query.filter_by(usename=uname,password=psw).first():
        session['username']=uname
        return redirect('imain')
    elif Sponsor.query.filter_by(usename=uname,password=psw).first():
        session['username']=uname
        return redirect('smain')
    else:
        return abort(401)
    #return "<0 0> i have to work here"


#----------------------influencer------------

@app.route('/imain')
def imain():
    if 'username' in session:
        data=Influencer.query.filter_by(usename=session['username']).first()
        print(data )
        uname=session['username']
        req=Requests.query.all()
        camp=Campaign.query.filter_by(iname=uname)
        return render_template('influencer_main.html',user=data,camp=camp,request=req)
    else :
        return redirect('login')

@app.route('/ifind')
def ifind():
    if 'username' in session:
        user=Influencer.query.filter_by(usename=session['username']).first()
        camp=Campaign.query.all()
        return  render_template("influencer_find.html",user=user,camp=camp)
    else:
        return redirect('/')

#-------------------sponsor---------------
@app.route('/smain')
def smain():
    if 'username' in session:
        name=session['username']
        user=Sponsor.query.filter_by(usename=name).first()
        activecamp=Campaign.query.filter_by(sname=user.usename)
        req=Requests.query.all()
        return render_template('sponsor_main.html',user=user,activecamp=activecamp,request=req)
    else :
        return redirect('login')
    
    
@app.route('/sfind')
def sfind():
    if 'username' in session:
        influ=Influencer.query.all()
        user=Sponsor.query.filter_by(usename=session['username']).first()
        return  render_template("sponsor_find.html",influ=influ,user=user)
    else:
        return redirect('/')

#----------------------rough--------------
'''


user = User.query.filter_by(username=username, password=password).first()
        if user:
            # Login successful
            session['logged_in'] = True
            session["username"]=username
            return redirect("/home")
        else:
            # Login failed
            error = 'Invalid username or password. Try again'
            return render_template('login.html', error=error)
    return render_template('login.html')'''

#-----------logout---------------

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


#--------------admin---------------

@app.route('/admin')
def admin():
    return render_template("admin_login.html")


@app.route('/adminlog',methods=['GET','POST'])
def adminlogin():
    uname=request.form['uname']
    psw=request.form['psw']
    print(uname,psw)
    if (uname=='ashirwad' and psw=='9430855605'):
        session['username']=uname
        return redirect('adminhome')
    else:
        #return '''You are not admin.Please login into influencer or sponsor page'''
        #401- is for unauth access
        return abort(401)

@app.route('/adminhome')
def adminhome():
    if 'username' in session:
        camp=Campaign.query.all()
        iflag=Influencer.query.filter_by(flag=1)
        sflag=Sponsor.query.filter_by(flag=1)
        cflag=Campaign.query.filter_by(flag=1)
        return render_template("admin_main.html",camp=camp,iflag=iflag,sflag=sflag,cflag=cflag)
    else:
        return redirect('/admin')#change to home later


@app.route('/adminfind')
def adminfind():
    if 'username' in session:
        spon=Sponsor.query.all()
        influ=Influencer.query.all()
        camp=Campaign.query.all()
        return  render_template("admin_find.html",influ=influ,camp=camp,spon=spon)
    else:
        return redirect('/admin')#change to home later


#-------------------------flag------------------------------
@app.route('/flag',methods=['GET','POST'])
def flag():
    if 'username' in session:
        data=list(request.form['flagvalue'].split(','))
        flagvalue=data[0]
        uname=data[1]
        if Influencer.query.filter_by(usename=uname).first():
            i=Influencer.query.filter_by(usename=uname).first()
            i.flag=flagvalue
            db.session.commit()
            print('success')
        elif Sponsor.query.filter_by(usename=uname).first():
            s=Sponsor.query.filter_by(usename=uname).first()
            s.flag=flagvalue
            db.session.commit()
            print('success')
        else :
            c=Campaign.query.filter_by(campaignid=uname).first()
            c.flag=flagvalue
            db.session.commit()
            print('success')
        
        #print(flagvalue,data)
        
        return redirect('/adminhome')
    else:
        return redirect('/admin')
    
@app.route('/flagfind',methods=['GET','POST'])
def flagfind():
    if 'username' in session:
        data=list(request.form['flagvalue'].split(','))
        flagvalue=data[0]
        uname=data[1]
        if Influencer.query.filter_by(usename=uname).first():
            i=Influencer.query.filter_by(usename=uname).first()
            i.flag=flagvalue
            db.session.commit()
            print('success')
        elif Sponsor.query.filter_by(usename=uname).first():
            s=Sponsor.query.filter_by(usename=uname).first()
            s.flag=flagvalue
            db.session.commit()
            print('success')
        else :
            c=Campaign.query.filter_by(campaignid=uname).first()
            c.flag=flagvalue
            db.session.commit()
            print('success')
        
        #print(flagvalue,data)
        
        return redirect('/adminfind')
    else:
        return redirect('/admin')

#--------------------campaign------------------------
@app.route('/addcampaign')
def addcamp():
    return render_template("campaign_form.html")

@app.route('/campaign')
def camp():
    if 'username' in session:
        name=session['username']
        user=Sponsor.query.filter_by(usename=name).first()
        camp=Campaign.query.filter_by(sname=user.usename)
        print(session['username'])
        print(user.usename,camp)
        return render_template("campaign.html",user=user,camp=camp)
    else:
        return redirect('/')


@app.route('/campdata',methods=['POST','GET'])       #influencer data to database
def camp_data():
    if 'username' in session:
        if session['username']==request.form['sname']:
            cname=request.form['cname']
            budget=request.form['budget']
            desc=request.form['desc']
            job=request.form['job']
            sname=request.form['sname']
            startdate=request.form['startdate']
            enddate=request.form['enddate']
            public=request.form['state']
            c1=Campaign(sname=sname,cname=cname,budget=budget,desc=desc,startdate=startdate,enddate=enddate,public=public,job=job,flag=False)
            db.session.add(c1)
            db.session.commit()
            #print(cname,budget,desc,job,sname,startdate,enddate,public)
            print('success')
            return redirect('/campaign')
        else:
            return f"Enter correct sponsor name"


#--------------------------------------------------------------------------



if __name__=="__main__":
    app.run(debug=True ,port=8000)