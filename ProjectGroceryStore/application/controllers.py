from flask import Flask,request,render_template,redirect,url_for
from flask import current_app as app 
from application.models import User,Section ,Products,Order
from application.database import db
from flask_sqlalchemy import SQLAlchemy
from datetime import date,datetime
from sqlalchemy import func,text
    


@app.route("/" , methods=["GET","POST"])

def home():
    if request.method=="GET":
        return render_template("home.html")
    else:
        user_type=request.form.get("user")
        if user_type=="admin":
            return render_template("admin.html")
        else:
            return render_template("user.html")
    

@app.route("/create_admin" , methods=["GET","POST"])
def admin():
    if request.method == "GET":
        return render_template("createadmin.html")
    else:
        full_name=request.form.get("full_name")
        user_name=request.form.get("user_name")
        Email=request.form.get("email")
        print(user_name,Email)
        password=request.form.get("password")
        Role="Admin"
        old_user1=User.query.filter(User.user_name==user_name).first()
        old_user2=User.query.filter(User.Email==Email).first()
        print(old_user1,old_user2)
        if old_user1!=None and old_user2!=None:
            return "Either Email or Username is already used"
        new_user=User(full_name=full_name,user_name=user_name,Email=Email,password=password,Role=Role)
        db.session.add(new_user)
        db.session.commit()
        print(new_user.id,".....................debug.........")
        return redirect(url_for("create_section",admin_id=new_user.id ))
    
@app.route("/user" , methods=["GET","POST"])
def user():
    if request.method == "GET":
        return render_template("createuser.html")
    else:
        full_name=request.form.get("full_name")
        user_name=request.form.get("user_name")
        Email=request.form.get("email")
        password=request.form.get("password")
        Role="user"
        old_user1=User.query.filter(User.user_name==user_name).first()
        old_user2=User.query.filter(User.Email==Email).first()
        if old_user1 or old_user2:
            return "Either Email or Username is already used"
        new_user=User(full_name=full_name,user_name=user_name,Email=Email,password=password,Role=Role)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")
    
@app.route("/getadmin" , methods=["GET","POST"])
def get_admin():
    if request.method=="POST":
        user_name=request.form.get("user_name")
        password=request.form.get("password")
        try:
            user=User.query.filter( User.user_name==user_name, User.password==password,User.Role=="Admin" ).first()
            user_id=user.id
            return redirect(url_for("displaySection" , admin_id=user_id))
        except:
            return "Wrong Username or Password"
        
        #section=Section.query.filter(Section.admin_id==user_id)
        #return render_template("adminSectiondetails.html", Section=section)
    else:
        user=User.query.filter(User.user_name==user_name)
        user_id=user[0].id
        section=Section.query.filter(Section.admin_id==user_id)
        return render_template("adminSectionProductsdetails.html", Section=section)
    
@app.route("/createsection/<admin_id>", methods=["GET","POST"])
def create_section(admin_id):
    if request.method=="GET":
        return render_template("createsection.html")
    else:
        name=request.form.get("name")
        section=Section(name=name,admin_id=admin_id)
        db.session.add(section)
        db.session.commit()
        section=Section.query.filter(Section.admin_id==admin_id)
        #return redirect(url_for("get_admin",))
        return redirect(url_for("displaySection", admin_id=section[0].admin_id))
    
@app.route("/updatesection/<section_id>/<admin_id>",methods=["GET","POST"])
def update_section(section_id,admin_id):
    if request.method=="GET":
        section=Section.query.filter(Section.id==section_id).first()
        name=section.name
        return render_template("updatesection.html",name=name)
    else:
        name=request.form.get("name")
        section=Section.query.filter(Section.id==section_id).first()
        section.name=name
        db.session.commit()
        return redirect(url_for("displaySection", admin_id=section.admin_id))  
      
@app.route("/displaysection/<admin_id>", methods=["GET","POST"])
def displaySection(admin_id):
    try:
        section=Section.query.filter(Section.admin_id==admin_id).all()
        orders=Order.query.filter(Order.admin_id==admin_id,Order.isActive=="yes").all()
        return render_template("adminSectiondetails.html", Section=section,Orders=orders)
    except:
        return render_template("Nosection.html",admin_id=admin_id)

@app.route("/deletesection/<id>/<admin_id>" )
def deletesection(id,admin_id):
    section=Section.query.filter(Section.id==id,Section.admin_id==admin_id)
    admin_id=section[0].admin_id

    for i in section:
        db.session.delete(i)
        db.session.commit()
    
    section=Section.query.filter(Section.admin_id==admin_id)
    products=Products.query.filter(Products.admin_id==admin_id,Products.section_id==id).all()

    for i in products:
        db.session.delete(i)
        db.session.commit()

    return redirect(url_for("displaySection", admin_id=admin_id))



@app.route("/displayProduct/<section_id>/<admin_id>" , methods=["GET"])
def displayProducts(section_id,admin_id):
    if type(section_id)=='str':
        section_id=int(section_id)
        admin_id=int(admin_id)
    if request.method=="GET":
        
        print(section_id,admin_id)
        products=Products.query.filter(Products.section_id== section_id,Products.admin_id==admin_id).all()
        if products:
            return render_template("productsAdmin.html", Products=products, admin_id=admin_id , section_id=section_id)
        else:
            return render_template("NoProducts.html",admin_id=admin_id,section_id=section_id)
   
    
@app.route("/addProduct/<admin_id>/<section_id>" , methods=["GET","POST"])
def addProduct(admin_id,section_id):
    admin_id=admin_id
    section_id=section_id
    if request.method=="GET":
        return render_template ("getProducts.html",admin_id=admin_id,section_id=section_id)
    if request.method=="POST":
        name=request.form.get("name")
        manufacture_date=request.form.get("man_Date")
        description=request.form.get("description")
        expiry_date=request.form.get("expiry_date")
        rate=request.form.get("rate")
        Unit=request.form.get("Unit")
        Quantity=request.form.get("Quantity")
        image=request.files['image']
        product=Products(name=name,manufacture_date=manufacture_date,expiry_date=expiry_date,rate=rate,section_id=section_id ,admin_id=admin_id,description=description,Unit=Unit,Quantity=Quantity)
        db.session.add(product)
        db.session.commit()

        lastAdded=Products.query.order_by(Products.id.desc()).all()
        id=str(lastAdded[0].id)
        image.filename=id+".jpeg"
        image.save('static/' + image.filename)
        products=Products.query.filter(Products.section_id== section_id,Products.admin_id==admin_id).all()
      
        return redirect(url_for("displayProducts",section_id=products[0].section_id,admin_id=products[0].admin_id))

@app.route("/updateProduct/<id>" , methods=["GET","POST"])
def updateProduct(id):
    if request.method=="GET":
        product=Products.query.filter(Products.id== id).first()
        return render_template("update_product.html",product=product)
    elif request.method=="POST":
        
        product=Products.query.filter(Products.id==id).first()
        product.name=request.form.get("name")
        product.description=request.form.get("description")
        product.rate=int(request.form.get("rate"))
        product.Unit=request.form.get("unit")
        product.Quantity=int(request.form.get("quantity"))
        db.session.commit()
    
        id=product.id
        image=request.files['image']
        print(image.filename,"........////")
        print(type(image.filename))
        if(image.filename !=  ""):
            image.filename=str(id)+".jpeg"
            image.save('static/' + image.filename)
        return redirect(url_for("displayProducts",section_id=product.section_id , admin_id=product.admin_id))


@app.route("/deleteProduct/<id>" , methods=["GET","POST"])
def deleteProduct(id):
    product=Products.query.filter(Products.id==id).first()
    section_id=product.section_id
    admin_id=product.admin_id
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for("displayProducts",section_id=section_id,admin_id=admin_id))




@app.route("/page1" , methods=["GET","POST"])
def page():
    if request.method=="GET":
        user_name=request.args.get("user_name")
        password=request.args.get("password")
        
        try:
            user=User.query.filter(User.user_name==user_name, User.password==password,User.Role=="user").first()
            user_id=user.id
            lastAdded=Products.query.order_by(Products.id.desc()).all()
            last_ten=lastAdded[:10]
            product_id=[]
                
            return render_template("page1.html", user_id=user_id,list=last_ten)
        except:
            return "Username or password is incorrect"
        
@app.route("/secondarypage1/<user_id>" , methods=["GET","POST"])
def secondary_page(user_id):    
    if request.method=="GET":
        lastAdded=Products.query.order_by(Products.id.desc()).all()
        last_ten=lastAdded[:10]      
        return render_template("page1.html", user_id=user_id,list=last_ten)
    
    

@app.route("/search" , methods=["GET","POST"])
def search():
    
    if request.method=="GET":
        user_id=request.args.get("user_id")
        q=request.args.get("search")
        query="%"+q+"%"
        results=Products.query.filter(Products.description.like(query)).all()
        if results:
            return render_template("search.html",results=results , user_id=user_id)
        return render_template("NoCategory.html",user_id=user_id)
    
    else:
        submit=request.form.get("submit")
        quantity=int(request.form.get("quantity"))
        user_id=(request.form.get("user_id"))
        product_id=int(request.form.get("product_id"))
        product=Products.query.filter(Products.id == product_id).first()
        admin_id=(product.admin_id)
        rate=(product.rate)
        price=rate*quantity
        if submit=="AddToCart":
            isActive="Yes"
            newQuantitiy=product.Quantity-quantity
            cart_exist=Order.query.filter(Order.product_id==product_id,Order.isActive=="Yes").first()
            if newQuantitiy<=0:
                return render_template("outofStock.html",Quantity=product.Quantity,name=product.name,user_id=user_id)
            if cart_exist==None:
                order =Order(admin_id=admin_id,user_id=user_id,product_id=product_id,rate=rate,Quantity=quantity,Price=price,isActive=isActive)
                db.session.add(order)
                db.session.commit()
                
            else:
                cart_exist.Quantity=cart_exist.Quantity+quantity
                cart_exist.Price=cart_exist.Quantity*rate
                db.session.commit()
            product.Quantity=newQuantitiy
            db.session.commit()
            return redirect(url_for("my_carts",user_id=user_id))
        else:
            today = date.today()
            d1 = today.strftime("%d/%m/%Y")
            now = datetime.now()
            newQuantitiy=product.Quantity-quantity
            isActive="No"
            order =Order(admin_id=admin_id,user_id=user_id,product_id=product_id,rate=rate,Quantity=quantity,Price=price,isActive=isActive,Date=d1,transaction_id=now)
            db.session.add(order)
            db.session.commit()
            order_id=order.id
            return redirect(url_for("direct_order",order_id=order_id))
    

@app.route("/my_orders/<user_id>", methods=["GET","POST"])
def myorders(user_id):
    if request.method=="GET":
        orders=Order.query.filter(Order.user_id==user_id,Order.isActive=="No").all()
        productname=[]
        orders=Order.query.filter(Order.user_id==user_id,Order.isActive=="No").all()
        total_cost=0
        for i in orders:
            product=Products.query.filter(Products.id==i.product_id).first()
            productname.append(product.name)
            total_cost+=i.Price
        tupleList=[]
        for i in range(len(orders)):
            x=(productname[i],orders[i].rate,orders[i].Quantity,orders[i].Price,orders[i].Date)
            tupleList.append(x)
        return render_template("Myorders.html",list=tupleList,user_id=user_id,total_cost=total_cost)
        
    else:
        return redirect(url_for("secondary_page", user_id=user_id))
 


@app.route("/my_carts/<user_id>", methods=["GET","POST"])
def my_carts(user_id):
    if request.method=="GET":
        carts=Order.query.filter(Order.user_id==user_id,Order.isActive=="Yes")
        tupleList=[]
        total_cost=0
        for i in carts:
            product=Products.query.filter(Products.id==i.product_id).first()
            total_cost+=i.Price
            x=(product.name,i.rate,i.Quantity,i.Price,i.id)
            tupleList.append(x)
        return render_template("myCarts.html",list=tupleList,user_id=user_id,total_cost=total_cost)
    else:
        return redirect(url_for("secondary_page", user_id=user_id))


@app.route("/confirm_order/<user_id>")
def confirm_order(user_id):
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    now = datetime.now()
    order=Order.query.filter(Order.user_id==user_id,Order.isActive=="Yes").all()
    for i in order:
        i.isActive="No"
        i.Date=d1
        i.transaction_id=now
        db.session.commit()
    return redirect(url_for("see_order",user_id=order[0].user_id))
    #return render_template("ordersucess.html",user_id=order[0].user_id)
@app.route("/see_order/<user_id>")
def see_order(user_id):
    return render_template("ordersucess.html",user_id=user_id)


@app.route("/remove_cart/<order_id>") 
def remove_cart(order_id):
    order=Order.query.filter(Order.id==order_id).first()
    user_id=order.user_id
    quantity=order.Quantity
    product_id=order.product_id
    db.session.delete(order)
    product=Products.query.filter(Products.id==product_id).first()
    product.Quantity=product.Quantity+quantity
    db.session.commit()
    return redirect(url_for("my_carts",user_id=user_id))
@app.route("/direct_order/<order_id>")
def direct_order(order_id):
    order=Order.query.filter(Order.id==order_id).first()
    product=Products.query.filter(Products.id==order.product_id).first()
    name=product.name
    return render_template("buy_now.html",name=name,order=order)
     






    

