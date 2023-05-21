import os,io,secrets,base64
from random import randint,random
from datetime import date,datetime
from PIL import Image
from calendar import monthrange
from flask import render_template, url_for, flash, redirect, request, jsonify
from energy_system import app,  db, bcrypt
from energy_system.forms import RegistrationForm, LoginForm
from energy_system.models import  User, Meter_Data
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
@login_required
def home():
    today_year = datetime.today().year
    today_month = datetime.today().month
    today_day = datetime.today().day
    if today_day==1 :
        if today_month == 1 :
            today_start_sample = Meter_Data.query.filter_by(Consumer=current_user).filter(Meter_Data.submit_time <= datetime(today_year-1,
                     12,31,23, 59, 59, 999999)).order_by(Meter_Data.submit_time.desc()).first()
        else : 
            today_start_sample = Meter_Data.query.filter_by(Consumer=current_user).filter(Meter_Data.submit_time <= datetime(today_year,
                     today_month-1,monthrange(today_year,today_month-1)[1],23, 59, 59, 999999)).order_by(Meter_Data.submit_time.desc()).first()
    else : 
         today_start_sample = Meter_Data.query.filter_by(Consumer=current_user).filter(Meter_Data.submit_time <= datetime(today_year,
                     today_month,today_day-1,23, 59, 59, 999999)).order_by(Meter_Data.submit_time.desc()).first()

    today_last_sample = Meter_Data.query.filter_by(Consumer=current_user).filter(Meter_Data.submit_time >= datetime(today_year,
                                today_month,today_day)).order_by(Meter_Data.submit_time.desc()).first()
    last_sample = Meter_Data.query.filter_by(Consumer=current_user).order_by(Meter_Data.submit_time.desc()).first()
    

    if today_month == 1 :
        month_start_sample = Meter_Data.query.filter_by(Consumer=current_user).filter(Meter_Data.submit_time <= datetime(today_year-1,
                     12,31,23, 59, 59, 999999)).order_by(Meter_Data.submit_time.desc()).first()
    else : 
        month_start_sample = Meter_Data.query.filter_by(Consumer=current_user).filter(Meter_Data.submit_time <= datetime(today_year,
                     today_month-1,monthrange(today_year,today_month-1)[1],23, 59, 59, 999999)).order_by(Meter_Data.submit_time.desc()).first() 
    
    if today_last_sample == None :
        today_used = 0
        month_last_sample = Meter_Data.query.filter_by(Consumer=current_user).filter(Meter_Data.submit_time <= datetime(today_year,
                                today_month,today_day)).order_by(Meter_Data.submit_time.desc()).first()
        if month_start_sample==None :
            monthly_used=0
        else :
            monthly_used = round(float(month_last_sample.meter_kwh)-float(month_start_sample.meter_kwh),2)
    else :
        today_used =  round((float(today_last_sample.meter_kwh) - float(today_start_sample.meter_kwh)),2)
        monthly_used = round(float(today_last_sample.meter_kwh)-float(month_start_sample.meter_kwh),2)

    img_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    daily_data_kwh = []
    # daily_data_hour =[]
    monthly_data =[]
    monthly_date = []
    monthly_data_kwh =[] 
    monthly_data_datetime=[]   

    #Prepare Monthly Data /////////////////////////
    # first_sample = Meter_Data.query.filter_by(Consumer=current_user).order_by(Meter_Data.submit_time.asc()).first()
    year = 2020
    # month = first_sample.submit_time.month

    # if month == 1:
    #     last_month_end_data = Meter_Data.query.filter_by(Consumer=current_user).filter(Meter_Data.submit_time <= datetime(year-1,12,31,23, 59, 59, 999999)).order_by(Meter_Data.submit_time.desc()).first()    
    # else : 
    #     last_month_end_data = Meter_Data.query.filter_by(Consumer=current_user).filter(Meter_Data.submit_time <= datetime(year,month-1,31,23, 59, 59, 999999)).order_by(Meter_Data.submit_time.desc()).first()    
    # # if last_month_end_data==None :
    #     last_month_end_data = last_month_end_data = Meter_Data.query.filter_by(Consumer=current_user).filter(Meter_Data.submit_time <= datetime(year,month,31,23, 59, 59, 999999)).order_by(Meter_Data.submit_time.asc()).first()    

    for month in range(1,13) :
        if month == 1:
            last_month_end_data = Meter_Data.query.filter_by(Consumer=current_user).filter(Meter_Data.submit_time <= datetime(year-1,12,31,23, 59, 59, 999999)).order_by(Meter_Data.submit_time.desc()).first()    
        else : 
            last_month_end_data = Meter_Data.query.filter_by(Consumer=current_user).filter(Meter_Data.submit_time <= datetime(year,month-1,monthrange(year,month-1)[1],23, 59, 59, 999999)).order_by(Meter_Data.submit_time.desc()).first()    
        for day in range(1,monthrange(year,month)[1]+1) :   
            current_month_end_data = Meter_Data.query.filter_by(Consumer=current_user).filter(Meter_Data.submit_time <= datetime(year,month,day,23, 59, 59, 999999)).order_by(Meter_Data.submit_time.desc()).first()
            if current_month_end_data == None or last_month_end_data==None :
                monthly_data_kwh.append(0)
            else :             
                monthly_data_kwh.append(round(float(current_month_end_data.meter_kwh)-float(last_month_end_data.meter_kwh),2))
            monthly_data_datetime.append(str(year)+"-"+str(month)+"-"+str(day))
            last_month_end_data = current_month_end_data
        monthly_date.append(monthly_data_datetime)
        monthly_data.append(monthly_data_kwh)
        monthly_data_datetime=[]
        monthly_data_kwh=[]

    #Prepare Yearly Data  ///////////////////////////
    # year = 2019
    yearly_data=[]
    yearly_data_kwh=[]
    # yearly_data_datetime=[]
    for x in range(2018,2021) :
        last_month_end_data = Meter_Data.query.filter_by(Consumer=current_user).filter(Meter_Data.submit_time <= datetime(x-1,12,31,23, 59, 59, 999999)).order_by(Meter_Data.submit_time.desc()).first()    
        if last_month_end_data==None :
            last_month_end_data = Meter_Data.query.filter_by(Consumer=current_user).filter(Meter_Data.submit_time <= datetime(x,12,31,23, 59, 59, 999999)).order_by(Meter_Data.submit_time.asc()).first()              
        for month in range(1,13) :
            current_month_end_data = Meter_Data.query.filter_by(Consumer=current_user).filter(Meter_Data.submit_time <= datetime(x,month,monthrange(x,month)[1],23, 59, 59, 999999)).order_by(Meter_Data.submit_time.desc()).first()              
            if current_month_end_data == None or last_month_end_data==None : 
                yearly_data_kwh.append(0)
            else :
                yearly_data_kwh.append(round((float(current_month_end_data.meter_kwh) - float(last_month_end_data.meter_kwh)),2))
            
            last_month_end_data = current_month_end_data
        yearly_data.append(yearly_data_kwh)
        yearly_data_kwh = []


    return render_template('home.html',user=current_user,image_file = img_file,day_used=today_used,month_used=monthly_used,daily_data_kwh=daily_data_kwh,daily_data_datetime=[],
                    monthly_data=monthly_data,monthly_date=monthly_date, current_reading = last_sample.meter_kwh  ,
                    test =[len(monthly_date[0]),len(monthly_data[0])],yearly_data=yearly_data)


@app.route("/update", methods=['POST'])
def update():
    uid = request.form['meter_id']
    
    if len(uid) > 5:
        uid = '0'+str(uid)
    user = User.query.filter_by(meter_id=uid).first()
    today_year = datetime.today().year
    today_month = datetime.today().month
    today_day = datetime.today().day
    last_sample = Meter_Data.query.filter_by(Consumer=user).order_by(Meter_Data.submit_time.desc()).first()
    
    if request.form['current_reading'] == str(last_sample.meter_kwh) :
        return jsonify({'update' : 'no'})

    else :
        if today_day==1 :
            if today_month == 1 :
                today_start_sample = Meter_Data.query.filter_by(Consumer=user).filter(Meter_Data.submit_time <= datetime(today_year-1,
                        12,31,23, 59, 59, 999999)).order_by(Meter_Data.submit_time.desc()).first()
            else : 
                today_start_sample = Meter_Data.query.filter_by(Consumer=user).filter(Meter_Data.submit_time <= datetime(today_year,
                        today_month-1,monthrange(today_year,today_month-1)[1],23, 59, 59, 999999)).order_by(Meter_Data.submit_time.desc()).first()
        else : 
            today_start_sample = Meter_Data.query.filter_by(Consumer=user).filter(Meter_Data.submit_time <= datetime(today_year,
                        today_month,today_day-1,23, 59, 59, 999999)).order_by(Meter_Data.submit_time.desc()).first()
        today_used =  round((float(last_sample.meter_kwh) - float(today_start_sample.meter_kwh)),2)

        if today_month == 1 :
            month_start_sample = Meter_Data.query.filter_by(Consumer=user).filter(Meter_Data.submit_time <= datetime(today_year-1,
                        12,31,23, 59, 59, 999999)).order_by(Meter_Data.submit_time.desc()).first()
        else : 
            month_start_sample = Meter_Data.query.filter_by(Consumer=user).filter(Meter_Data.submit_time <= datetime(today_year,
                        today_month-1,monthrange(today_year,today_month-1)[1],23, 59, 59, 999999)).order_by(Meter_Data.submit_time.desc()).first() 
        monthly_used = round(float(last_sample.meter_kwh)-float(month_start_sample.meter_kwh),2)

        

        return jsonify({'update' : 'yes', 'month_used' : monthly_used,'day_used':today_used,'current_reading':last_sample.meter_kwh})

@app.route("/meter")
def meter():
    submit_id = request.args.get('id')
    auth_code = request.args.get('code')
    up_kwh = request.args.get('kwh')
    user = User.query.filter_by(meter_id=submit_id).first()
    # meter_user = Meter_Data.query.filter_by(submit_id=submit_id).order_by(Meter_Data.submit_time.desc()).first()
    if user.auth_code==auth_code:
        update_meter = Meter_Data(submit_id=user.meter_id, meter_kwh=up_kwh, user_id=user.id, submit_time = datetime.now())
        db.session.add(update_meter)
        db.session.commit()
        return 'Updated:' + str( up_kwh )
    else:
        return 'Update Error!'

    return "complete"


# @app.route("/info")
# def info():
#     submit_id = request.args.get('id')
#     auth_code = request.args.get('code')
#     user = User.query.filter_by(meter_id=submit_id).first()
#     meter_user = Meter_Data.query.filter_by(submit_id=submit_id).order_by(Meter_Data.submit_time.desc()).first()
#     if user.auth_code==auth_code:
#         return meter_user.meter_kwh
#     else:
#         return 'Auth Error!'
    
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)

    return picture_fn

@app.route("/add_meter", methods=['GET', 'POST'])
def add_meter():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        else:
            picture_file = 'default.jpg'
            
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(meter_id=form.meter_id.data,name=form.name.data,phone=form.phone.data, 
                            email=form.email.data, address=form.address.data, image_file=picture_file, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        update_meter = Meter_Data(submit_id=user.meter_id, meter_kwh=0, user_id=user.id)
        db.session.add(update_meter)
        db.session.commit()
        flash('New account has been created! Enabled to log in', 'success')
        return redirect(url_for('user_login'))
    return render_template('add_meter.html', title='Register', form=form)


@app.route("/user_login", methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(meter_id=form.meter_id.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful! Please check Meter ID and password', 'danger')
    return render_template('user_login.html', title='Login', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_login'))


# @app.route("/user_dashboard")
# @login_required
# def user_dashboard():  
#     img_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
#     current_reading = Meter_Data.query.filter_by(Consumer=current_user).order_by(Meter_Data.submit_time.desc()).first()
#     bill =  float(current_reading.meter_kwh) * 5.00
    

#     return render_template('user_dashboard.html', title='Dashboard - '+current_user.meter_id , user=current_user,
#                                              image_file=img_file, current_reading=current_reading, bill = bill)

# @app.route("/uses_history")
# @login_required
# def uses_history():
#     meter_uses = Meter_Data.query.filter_by(Consumer=current_user).order_by(Meter_Data.submit_time.asc()).all()
#     daily_uses = []
    
#     kwh_list = []
#     time_list= []
#     pre_kwh = 0.00
#     for meter_use in meter_uses:
#             if meter_use.submit_time.date() == date.today():
#                 time_list.append(meter_use.submit_time.strftime("%Y-%m-%d %H:%M:%S"))
#                 kwh_list.append(abs(float(meter_use.meter_kwh) - pre_kwh))
#                 pre_kwh = float(meter_use.meter_kwh)

#     return render_template('uses_history.html', title='Uses History', meter_uses=meter_uses, user=current_user,
#                                             kwh_list=kwh_list,time_list=time_list,daily_uses=daily_uses,LEN_TEST=len(time_list))
  

@app.route("/payment")
@login_required
def payment():
    return render_template('payment.html', title ='Energy Meter - Bill Payment')

@app.route("/notifications")
@login_required
def notifications():
    return render_template('notifications.html')

# @app.route("/load")
# def load():
#     user = User.query.filter_by(meter_id='0170875').first()
#     up_kwh = 0
#     if user == None:
#         user =  User.query.all()
#         return str(user)

#     for i in range(1,25):
#         update_meter = Meter_Data(submit_id=user.meter_id, meter_kwh=up_kwh, user_id=user.id, submit_time = datetime(2020,11,i))
#         db.session.add(update_meter)
#         db.session.commit()
#         up_kwh=up_kwh+0.5

#     return "complete load"

# @app.route("/test")
# def test():
#     test = 'test'
#     return test
