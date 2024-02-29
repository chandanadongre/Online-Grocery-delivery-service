from flask import Flask,redirect,render_template,request,flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

local_server = True
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Dongre101@localhost/your_database'
db = SQLAlchemy(app)

#database connection
# local_server = True
# app = Flask(__name__)
# app.secret_key = "dbmsproject"

# #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/databasename'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Dongre101@localhost/Grocery'
# db = SQLAlchemy(app)

class customer(db.Model):
    CustomerID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(255), nullable=False)
    LastName = db.Column(db.String(255), nullable=False)
    EmailID = db.Column(db.String(255), nullable=False)
    Username = db.Column(db.String(255), nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    PhoneNo = db.Column(db.String(255), nullable=False)
    Address = db.Column(db.String(255), nullable=False)

class deliverydriver(db.Model):
    DeliveryID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    EmailID = db.Column(db.String(255), nullable=False)
    VehicleInfo = db.Column(db.String(255), nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    PhoneNo = db.Column(db.String(255), nullable=False)
    Address = db.Column(db.String(255), nullable=False)

class Product(db.Model):
    ProductID = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(255), nullable=False)
    Price = db.Column(db.Numeric(10, 2), nullable=True)  # Assuming Price can be null
    QuantityInStock = db.Column(db.Integer, nullable=True)  # Assuming QuantityInStock can be null
    Description = db.Column(db.Text, nullable=True)

class order(db.Model):
    OrderID = db.Column(db.Integer, primary_key=True)
    DeliveryAddress = db.Column(db.String(255), nullable=False)
    CustomerID = db.Column(db.Integer, db.ForeignKey('customer.CustomerID'), nullable=False)  # Assuming there's a 'customer' table
    Amount = db.Column(db.Numeric(10, 2), nullable=False)
    OrderDateTime = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    OrderStatus = db.Column(db.String(50), nullable=False)
    # order_items = db.relationship('orderitem', backref='order', lazy=True)

class orderitem(db.Model):
    OrderItemID = db.Column(db.Integer, primary_key=True)
    OrderID = db.Column(db.Integer,db.ForeignKey('order.OrderID'))
    Quantity = db.Column(db.Integer)
    ProductID = db.Column(db.Integer,db.ForeignKey('Product.ProductID'))
    TotalAmount = db.Column(db.Float)

class admins(db.Model):
    AdminID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(255), nullable=False)
    LastName = db.Column(db.String(255), nullable=False)
    EmailID = db.Column(db.String(255), nullable=False)
    Username = db.Column(db.String(255), nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    PhoneNo = db.Column(db.String(255), nullable=False)
    Address = db.Column(db.String(255), nullable=False)

class deliveryassignment(db.Model):
    AssignmentID = db.Column(db.Integer, primary_key=True)
    OrderID = db.Column(db.Integer,db.ForeignKey('Order.OrderID'),nullable=False)
    DeliveryID = db.Column(db.Integer,db.ForeignKey('delivery.DeliveryID') ,nullable=False)
    DeliveryAddress = db.Column(db.String(255), nullable=False)
    AssignmentDateTime = db.Column(db.DateTime, nullable=False)

class transaction(db.Model):
    TransactionID = db.Column(db.Integer, primary_key=True)
    OrderID = db.Column(db.Integer, db.ForeignKey('order.OrderID'), nullable=False)  # Assuming there's an 'order' table
    PaymentDateTime = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    Amount = db.Column(db.Numeric(10, 2), nullable=True)  # Assuming Amount can be null
    PaymentMethod = db.Column(db.String(50), nullable=True)  # Assuming PaymentMethod can be null
    PaymentStatus = db.Column(db.String(50), nullable=True)

#User Login and Authentication Starts
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/admin")
def admin_view():
    return render_template("Admin.html")

@app.route("/customer")
def customer_view():
    return render_template("User.html")

@app.route("/delivery_person")
def delivery_person_view():
    return render_template("Delivery.html")

@app.route("/login_process", methods=["POST"])
def login_process():
    user_type = request.form["user_type"]

    if user_type == "admin":
        return redirect("/admin")
    elif user_type == "customer":
        return redirect("/customer")
    elif user_type == "delivery":
        return redirect("/delivery_person")
    else:
        return "Invalid user type"

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/delivery_login", methods=["POST"])
def delivery_login():
    username = request.form["username"]
    password = request.form["password"]

    # Check if the username and password match a customer record
    Driver = deliverydriver.query.filter_by(Name=username, Password=password).first()

    if Driver:
        return redirect("/driver_home")
    else:
        flash("Invalid username or password. Please try again.", "error")
        return redirect(request.referrer)  # Redirect back to the previous page

@app.route("/admin_login", methods=["POST"])
def admin_login():
    username = request.form["username"]
    password = request.form["password"]

    # Check if the username and password match a customer record
    Admin = admins.query.filter_by(Username=username, Password=password).first()

    if Admin:
        return redirect("/admin_home")
    else:
        flash("Invalid username or password. Please try again.", "error")
        return redirect(request.referrer)  # Redirect back to the previous page 

@app.route("/signup_process", methods=["POST"])
def signup_process():
    role = request.form["role"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]
    phoneno = request.form["phoneno"]
    address = request.form["address"]

    try:
        if role == "customer":
            ID = customer.query.count()
            new_customer = customer(
                CustomerID = ID + 1,
                FirstName=firstname,
                LastName=lastname,
                EmailID=email,
                Username=username,
                Password=password,
                PhoneNo=phoneno,
                Address=address
            )
            db.session.add(new_customer)
            db.session.commit()

        elif role == "delivery":
            ID = deliverydriver.query.count()
            new_delivery_person = deliverydriver(
                DeliveryID = ID +1,
                Name=firstname + " " + lastname,
                EmailID=email,
                VehicleInfo="",  # Add the vehicle information if available
                Password=password,
                PhoneNo=phoneno,
                Address=address
            )
            db.session.add(new_delivery_person)

        elif role == "admin":
            # Add code to handle admin registration if needed
            ID = admins.query.count()
            new_admin = admins(
                AdminID = ID +1,
                FirstName=firstname,
                LastName=lastname,
                EmailID=email,
                Username=username,
                Password=password,
                PhoneNo=phoneno,
                Address=address
            )
            db.session.add(new_admin)

        else:
            flash("Invalid role selected. Please try again.", "error")
            return redirect("/signup")  # Redirect back to the signup page if an invalid role is selected

        db.session.commit()
        flash("User registered successfully!", "success")
        return redirect("/login")  # Redirect to the login page after successful signup

    except Exception as e:
        print(e)
        flash("An error occurred while registering. Please try again.", "error")
        return redirect("/signup")  # Redirect back to the signup page in case of an error

#User login and authentication ends here

#Customer page starts here
@app.route("/customer_login", methods=["POST"])
def customer_login():
    username = request.form["username"]
    password = request.form["password"]

    # Check if the username and password match a customer record
    Customer = customer.query.filter_by(Username=username, Password=password).first()

    if Customer:
        # Store the customer's information in the session
        session['customer_id'] = Customer.CustomerID
        session['customer_username'] = Customer.Username
        session['customer_name'] = f"{Customer.FirstName} {Customer.LastName}"

        # Print the session for debugging
        print(session)

        return redirect("/customer_home")  # Redirect to the customer home page
    else:
        flash("Invalid username or password. Please try again.", "error")
        return redirect(request.referrer)  # Redirect back to the previous page

from main import app, Product 
@app.route("/customer_home")
def customer_home():
    # Retrieve the username from the session with a default value of None
    username = session.get("customer_username")

    # Fetch products from the Product table
    products = Product.query.all()

    # Pass the username and products to the template for rendering
    return render_template("customer_home.html", username=username, products=products)

@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    selected_product = Product.query.get(product_id)

    if selected_product:
        # Initialize the cart in the session if not already present
        if 'cart' not in session:
            session['cart'] = []

        # Check if the product is already in the cart
        for item in session['cart']:
            if item['id'] == selected_product.ProductID:
                flash('Product already in cart', 'info')
                return redirect(url_for("customer_home"))

        # Add the selected product to the cart
        session['cart'].append({
            'id': selected_product.ProductID,
            'name': selected_product.ProductName,
            'price': float(selected_product.Price),
            'quantity': 1  # Default quantity is set to 1
        })
        flash('Item added to cart successfully', 'success')
        return redirect(url_for("customer_home"))
    else:
        # Handle the case where the product is not found
        return render_template('product_not_found.html')

@app.route("/view_cart")
def view_cart():
    # Retrieve the cart from the session
    cart = session.get('cart', [])
    for item in cart:
        item['price'] = float(item['price'])
    # Calculate the total price of items in the cart
    total_price = sum(item['price'] for item in cart)

    # Pass the cart and total_price to the template for rendering
    return render_template("view_cart.html", cart=cart, total_price=total_price)


@app.route('/update_quantity/<int:product_id>', methods=['POST'])
def update_quantity(product_id):
    new_quantity = int(request.form.get(f'quantity_{product_id}', 1))
    remove_item = request.form.get('remove_item', False)

    cart = session.get('cart', [])
    selected_product = next((item for item in cart if item['id'] == product_id), None)

    if selected_product:
        if new_quantity > 0:            
            selected_product['quantity'] = new_quantity
            # flash('Quantity updated successfully')
            
        # if new_quantity == 0:
        #     # Remove the item from the session
        #     cart = session.get('cart', [])
        #     updated_cart = [item for item in cart if item['id'] != product_id]
        #     session['cart'] = updated_cart
        #     flash(f'The product {selected_product["name"]} is removed from the cart', 'info')

        if remove_item.lower() == 'true':            
            updated_cart = [item for item in cart if item['id'] != product_id]
            session['cart'] = updated_cart
            # flash(f'The product {selected_product["name"]} is removed from the cart', 'info')

    # Recalculate total price
    total_price = calculate_total_price(cart)
    return render_template('view_cart.html', cart=cart, total_price=total_price)

def calculate_total_price(cart):
    return sum(item['price'] * item['quantity'] for item in cart)


@app.route('/clear_cart')
def clear_cart():
    # Clear the cart when the "Clear the Cart" button is clicked
    session.pop('cart', None)
    # flash('Cart cleared successfully')
    return redirect(url_for('view_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Perform any necessary actions when the form is submitted
        # For example, process the order and clear the cart
        flash('Thank you for shopping!', 'success')
        session.pop('cart', None)  # Clear the cart

        # Redirect to the 'continue_shopping' route
        return redirect(url_for('continue_shopping'))

    # Retrieve the cart information from the session
    cart = session.get('cart', [])
    for item in cart:
        item['price'] = float(item['price'])

    # Calculate the total price of items in the cart
    total_price = sum(item['price'] * item['quantity'] for item in cart)

    # Pass the cart and total_price to the template for rendering
    return render_template('checkout.html', cart=cart, total_price=total_price)

# @app.route('/checkout', methods=['GET', 'POST'])
# def checkout():
#     if request.method == 'POST':
#         # Retrieve the cart information from the session
#         cart = session.get('cart', [])

#         # Calculate the total price of items in the cart
#         total_price = sum(item['price'] * item['quantity'] for item in cart)

#         # Get other relevant information for the order
#         delivery_address = request.form.get('delivery_address')  # Adjust as needed
#         customer_id = request.form.get('customer_id')  # Adjust as needed
#         order_date_time = datetime.now()  # Assuming you import datetime
#         order_status = 'Completed'  # You might want to handle order status differently

#         # Create an Order instance and add it to the database
#         orders = order(
#             DeliveryAddress=delivery_address,
#             CustomerID=customer_id,
#             Amount=total_price,
#             OrderDateTime=order_date_time,
#             OrderStatus=order_status
#         )

#         db.session.add(orders)
#         db.session.commit()

#         flash('Thank you for shopping!', 'success')
#         session.pop('cart', None)  # Clear the cart

#         return redirect(url_for('continue_shopping'))

#     cart = session.get('cart', [])
#     for item in cart:
#         item['price'] = float(item['price'])

#     total_price = sum(item['price'] * item['quantity'] for item in cart)

#     return render_template('checkout.html', cart=cart, total_price=total_price)




#Customer page ends here

#Inventory Management Starts
@app.route("/admin_home")
def admin_home():
    return render_template("admin_home.html")

@app.route("/inventory_management", methods=["GET", "POST"])
def handle_CRUD():
    selected_table = request.form["table_select"]
    crud_operation = request.form["crud_operation"]

    # Redirect to the appropriate route based on the selected table and CRUD operation
    return redirect((f"{crud_operation}_{selected_table}"))

# Placeholder routes for each CRUD operation on the 'product' table (adjust as needed)
@app.route("/view_<table_name>")
def view_product(table_name):
    # Define a mapping between table names and corresponding models
    table_model_mapping = {
        "product": Product, 
        "admins" : admins,
        "customer" : customer,
        "deliverydriver" : deliverydriver,
        "order" : order,
        "orderitem" : orderitem,
        "deliveryassignment" : deliveryassignment,
        "transaction" : transaction
    }
    # Check if the requested table_name is valid
    if table_name in table_model_mapping:
        # Fetch all records from the specified table
        records = table_model_mapping[table_name].query.all()
        # Render the template with the fetched data
        return render_template("view_table.html", table_name=table_name, records=records)

@app.route("/add_<table_name>", methods=["GET", "POST"])
def add_record(table_name):
    # Define a mapping between table names and corresponding models
    table_model_mapping = {
        "product": Product,
        "admins": admins,
        "deliverydriver": deliverydriver,
        "deliveryassignment": deliveryassignment,
    }

    if table_name in table_model_mapping:
        # Get the model for the specified table_name
        model = table_model_mapping[table_name]

        # Get the columns of the model
        columns = [column.name for column in model.__table__.columns]

        if request.method == "POST":
            try:
                # Extract form data from the request
                form_data = {column: request.form[column] for column in columns}
                print(form_data)

                # Create a new record and add it to the database
                new_record = model(**form_data)
                db.session.add(new_record)
                db.session.commit()

                return "Record added successfully!"
            except Exception as e:
                # Handle exceptions (e.g., validation errors, database errors)
                print(e)
                db.session.rollback()  # Rollback changes in case of an error
                return f"Error: {str(e)}"

        else:
            return render_template("add_record.html", table_name=table_name, columns=columns)

    else:
        return "Table not found", 404

@app.route("/edit_product", methods=["GET","POST"])
def edit_product():
    # Define a mapping between table names and corresponding models
    table_model_mapping = {
        "product": Product
    }

    if request.method == "GET":
        # Display a form to select the product ID for editing
        return render_template("select_product.html", table_name="product")

    elif request.method == "POST":
        # Handle the form submission to get the selected product ID
        product_id = request.form.get("product_id")

        if product_id:
            # Redirect to the edit page for the selected product
            return redirect(f"/edit/{product_id}")
        else:
            # If no product ID is provided, display an error or redirect to the selection page
            return "Please select a product for editing."

@app.route("/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product_details(product_id):

    # Define a mapping between table names and corresponding models
    

    # Get the product by ID
    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        # Handle form submission to update product details
        try:
            # Update product fields based on the form data
            product.ProductName = request.form.get("product_name", product.ProductName)
            product.Price = float(request.form.get("price", product.Price))
            product.QuantityInStock = int(request.form.get("quantity_in_stock", product.QuantityInStock))
            product.Description = request.form.get("description", product.Description)

            # Commit the changes to the database
            db.session.commit()
            
            return "Updated Product Successfully"
        
        except Exception as e:
            # Handle validation errors or other exceptions
            db.session.rollback()
            return f"Error: {str(e)}"

    # Render the edit form with the current product details
    return render_template("edit_product_details.html", product=product)
  

@app.route("/delete_product", methods=["GET", "POST"])
def delete_product():
    # Add logic for deleting a product
    # Define a mapping between table names and corresponding models
    table_model_mapping = {
        "product": Product
    }

    if request.method == "GET":
        # Display the page to select the product for deletion
        return render_template("select_product_for_deletion.html")

    elif request.method == "POST":
        # Handle the form submission to get the selected product ID for deletion
        product_id = request.form.get("product_id")

        if product_id:
            # Redirect to the delete page for the selected product
            return redirect(f"/delete/{product_id}")
        else:
            # If no product ID is provided, display an error or redirect back to the selection page
            return "Please select a product for deletion."

@app.route("/delete/<int:product_id>", methods=["GET", "POST"])
def delete_product_confirm(product_id):
    if request.method == "GET":
        # Display the confirmation page
        return render_template("delete_product_details.html", product_id=product_id)

    elif request.method == "POST":
        # Handle the form submission to delete the product with the given ID
        table_model_mapping = {
            "product": Product
        }
        product_to_delete = Product.query.get(product_id)

        if product_to_delete:
            try:
                # Delete the product from the database
                db.session.delete(product_to_delete)
                db.session.commit()
                flash("Product deleted successfully!", "success")
                return "Product deleted successfully"
            except Exception as e:
                print(e)
                db.session.rollback()
                flash("An error occurred while deleting the product. Please try again.", "error")
                
        else:
            flash("Product not found.", "error")
            return "Product not found"

    # Return a response for all cases
    return redirect(url_for("inventory_management"))

    

#Inventory Management Ends


@app.route("/logout", methods=["POST"])
def logout():
    # Clear the session
    session.clear()

    # Redirect to the login page
    return redirect("/login")

# Flask route for the account page
# @app.route('/account')
# def account():
#     return render_template('account.html')

@app.route('/account')
def account():
    user_id=session.get("customer_id")
    # Fetch a sample user from the database
    sample_customer = customer.query.filter_by(CustomerID=user_id).first()

    # Pass the user details to the template
    return render_template('account.html', customer=sample_customer)
app.run(debug=True)