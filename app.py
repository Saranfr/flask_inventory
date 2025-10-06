from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Product, Location, ProductMovement
from forms import ProductForm, LocationForm, ProductMovementForm
from sqlalchemy import func
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products_list():
    products = Product.query.all()
    return render_template('products_list.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
def products_add():
    form = ProductForm()
    if form.validate_on_submit():
        existing = Product.query.get(form.product_id.data)
        if existing:
            flash('Product ID already exists!', 'danger')
            return render_template('product_form.html', form=form, action='Add')
        
        product = Product(
            product_id=form.product_id.data,
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('products_list'))
    
    return render_template('product_form.html', form=form, action='Add')

@app.route('/products/edit/<product_id>', methods=['GET', 'POST'])
def products_edit(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    form.product_id.render_kw = {'readonly': True}
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products_list'))
    
    return render_template('product_form.html', form=form, action='Edit', product=product)

@app.route('/products/view/<product_id>')
def products_view(product_id):
    product = Product.query.get_or_404(product_id)
    movements = ProductMovement.query.filter_by(product_id=product_id).order_by(ProductMovement.timestamp.desc()).all()
    return render_template('product_view.html', product=product, movements=movements)

@app.route('/locations')
def locations_list():
    locations = Location.query.all()
    return render_template('locations_list.html', locations=locations)

@app.route('/locations/add', methods=['GET', 'POST'])
def locations_add():
    form = LocationForm()
    if form.validate_on_submit():
        existing = Location.query.get(form.location_id.data)
        if existing:
            flash('Location ID already exists!', 'danger')
            return render_template('location_form.html', form=form, action='Add')
        
        location = Location(
            location_id=form.location_id.data,
            name=form.name.data
        )
        db.session.add(location)
        db.session.commit()
        flash('Location added successfully!', 'success')
        return redirect(url_for('locations_list'))
    
    return render_template('location_form.html', form=form, action='Add')

@app.route('/locations/edit/<location_id>', methods=['GET', 'POST'])
def locations_edit(location_id):
    location = Location.query.get_or_404(location_id)
    form = LocationForm(obj=location)
    form.location_id.render_kw = {'readonly': True}
    
    if form.validate_on_submit():
        location.name = form.name.data
        db.session.commit()
        flash('Location updated successfully!', 'success')
        return redirect(url_for('locations_list'))
    
    return render_template('location_form.html', form=form, action='Edit', location=location)

@app.route('/locations/view/<location_id>')
def locations_view(location_id):
    location = Location.query.get_or_404(location_id)
    movements_in = ProductMovement.query.filter_by(to_location=location_id).order_by(ProductMovement.timestamp.desc()).all()
    movements_out = ProductMovement.query.filter_by(from_location=location_id).order_by(ProductMovement.timestamp.desc()).all()
    return render_template('location_view.html', location=location, movements_in=movements_in, movements_out=movements_out)

@app.route('/movements')
def movements_list():
    movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    return render_template('movements_list.html', movements=movements)

@app.route('/movements/add', methods=['GET', 'POST'])
def movements_add():
    form = ProductMovementForm()
    
    products = Product.query.all()
    locations = Location.query.all()
    
    form.product_id.choices = [(p.product_id, f"{p.product_id} - {p.name}") for p in products]
    form.from_location.choices = [('', 'None')] + [(l.location_id, f"{l.location_id} - {l.name}") for l in locations]
    form.to_location.choices = [('', 'None')] + [(l.location_id, f"{l.location_id} - {l.name}") for l in locations]
    
    if form.validate_on_submit():
        existing = ProductMovement.query.get(form.movement_id.data)
        if existing:
            flash('Movement ID already exists!', 'danger')
            return render_template('movement_form.html', form=form, action='Add')
        
        movement = ProductMovement(
            movement_id=form.movement_id.data,
            product_id=form.product_id.data,
            from_location=form.from_location.data if form.from_location.data else None,
            to_location=form.to_location.data if form.to_location.data else None,
            qty=form.qty.data,
            timestamp=form.timestamp.data if form.timestamp.data else datetime.now()
        )
        db.session.add(movement)
        db.session.commit()
        flash('Product movement added successfully!', 'success')
        return redirect(url_for('movements_list'))
    
    return render_template('movement_form.html', form=form, action='Add')

@app.route('/movements/edit/<movement_id>', methods=['GET', 'POST'])
def movements_edit(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    form = ProductMovementForm(obj=movement)
    form.movement_id.render_kw = {'readonly': True}
    
    products = Product.query.all()
    locations = Location.query.all()
    
    form.product_id.choices = [(p.product_id, f"{p.product_id} - {p.name}") for p in products]
    form.from_location.choices = [('', 'None')] + [(l.location_id, f"{l.location_id} - {l.name}") for l in locations]
    form.to_location.choices = [('', 'None')] + [(l.location_id, f"{l.location_id} - {l.name}") for l in locations]
    
    if form.validate_on_submit():
        movement.product_id = form.product_id.data
        movement.from_location = form.from_location.data if form.from_location.data else None
        movement.to_location = form.to_location.data if form.to_location.data else None
        movement.qty = form.qty.data
        movement.timestamp = form.timestamp.data if form.timestamp.data else movement.timestamp
        db.session.commit()
        flash('Product movement updated successfully!', 'success')
        return redirect(url_for('movements_list'))
    
    return render_template('movement_form.html', form=form, action='Edit', movement=movement)

@app.route('/movements/view/<movement_id>')
def movements_view(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    return render_template('movement_view.html', movement=movement)

@app.route('/report/balance')
def report_balance():
    balance_data = db.session.query(
        Product.product_id,
        Product.name.label('product_name'),
        Location.location_id,
        Location.name.label('location_name'),
        func.sum(
            db.case(
                (ProductMovement.to_location == Location.location_id, ProductMovement.qty),
                else_=0
            )
        ).label('qty_in'),
        func.sum(
            db.case(
                (ProductMovement.from_location == Location.location_id, ProductMovement.qty),
                else_=0
            )
        ).label('qty_out')
    ).select_from(Product).join(
        ProductMovement, Product.product_id == ProductMovement.product_id
    ).join(
        Location,
        db.or_(
            ProductMovement.to_location == Location.location_id,
            ProductMovement.from_location == Location.location_id
        )
    ).group_by(
        Product.product_id,
        Product.name,
        Location.location_id,
        Location.name
    ).all()
    
    balance_list = []
    for row in balance_data:
        balance_list.append({
            'product_id': row.product_id,
            'product_name': row.product_name,
            'location_id': row.location_id,
            'location_name': row.location_name,
            'qty': (row.qty_in or 0) - (row.qty_out or 0)
        })
    
    return render_template('report_balance.html', balance=balance_list)

def init_db():
    with app.app_context():
        db.create_all()
        
        if Product.query.count() == 0:
            products = [
                Product(product_id='P001', name='Laptop', description='Dell Laptop 15 inch'),
                Product(product_id='P002', name='Mouse', description='Wireless Mouse'),
                Product(product_id='P003', name='Keyboard', description='Mechanical Keyboard'),
                Product(product_id='P004', name='Monitor', description='24 inch LED Monitor')
            ]
            db.session.add_all(products)
            
            locations = [
                Location(location_id='L001', name='Main Warehouse'),
                Location(location_id='L002', name='Retail Store A'),
                Location(location_id='L003', name='Retail Store B'),
                Location(location_id='L004', name='Service Center')
            ]
            db.session.add_all(locations)
            
            db.session.commit()
            
            movements = [
                ProductMovement(movement_id='M001', product_id='P001', from_location=None, to_location='L001', qty=50, timestamp=datetime(2025, 10, 1, 9, 0)),
                ProductMovement(movement_id='M002', product_id='P002', from_location=None, to_location='L001', qty=100, timestamp=datetime(2025, 10, 1, 9, 30)),
                ProductMovement(movement_id='M003', product_id='P003', from_location=None, to_location='L001', qty=80, timestamp=datetime(2025, 10, 1, 10, 0)),
                ProductMovement(movement_id='M004', product_id='P004', from_location=None, to_location='L001', qty=30, timestamp=datetime(2025, 10, 1, 10, 30)),
                ProductMovement(movement_id='M005', product_id='P001', from_location='L001', to_location='L002', qty=10, timestamp=datetime(2025, 10, 2, 11, 0)),
                ProductMovement(movement_id='M006', product_id='P002', from_location='L001', to_location='L002', qty=20, timestamp=datetime(2025, 10, 2, 11, 30)),
                ProductMovement(movement_id='M007', product_id='P001', from_location='L001', to_location='L003', qty=15, timestamp=datetime(2025, 10, 2, 14, 0)),
                ProductMovement(movement_id='M008', product_id='P003', from_location='L001', to_location='L003', qty=25, timestamp=datetime(2025, 10, 2, 14, 30)),
                ProductMovement(movement_id='M009', product_id='P004', from_location='L001', to_location='L002', qty=8, timestamp=datetime(2025, 10, 3, 9, 0)),
                ProductMovement(movement_id='M010', product_id='P002', from_location='L001', to_location='L004', qty=15, timestamp=datetime(2025, 10, 3, 9, 30)),
                ProductMovement(movement_id='M011', product_id='P001', from_location='L002', to_location='L003', qty=3, timestamp=datetime(2025, 10, 3, 13, 0)),
                ProductMovement(movement_id='M012', product_id='P003', from_location='L001', to_location='L002', qty=20, timestamp=datetime(2025, 10, 3, 13, 30)),
                ProductMovement(movement_id='M013', product_id='P004', from_location='L001', to_location='L003', qty=7, timestamp=datetime(2025, 10, 4, 10, 0)),
                ProductMovement(movement_id='M014', product_id='P002', from_location='L002', to_location=None, qty=5, timestamp=datetime(2025, 10, 4, 10, 30)),
                ProductMovement(movement_id='M015', product_id='P001', from_location='L003', to_location=None, qty=2, timestamp=datetime(2025, 10, 4, 14, 0)),
                ProductMovement(movement_id='M016', product_id='P003', from_location='L002', to_location='L004', qty=10, timestamp=datetime(2025, 10, 4, 14, 30)),
                ProductMovement(movement_id='M017', product_id='P004', from_location='L002', to_location='L004', qty=3, timestamp=datetime(2025, 10, 5, 9, 0)),
                ProductMovement(movement_id='M018', product_id='P002', from_location='L001', to_location='L003', qty=25, timestamp=datetime(2025, 10, 5, 9, 30)),
                ProductMovement(movement_id='M019', product_id='P001', from_location='L001', to_location='L004', qty=5, timestamp=datetime(2025, 10, 5, 11, 0)),
                ProductMovement(movement_id='M020', product_id='P003', from_location='L003', to_location='L001', qty=5, timestamp=datetime(2025, 10, 5, 11, 30)),
                ProductMovement(movement_id='M021', product_id='P004', from_location='L003', to_location=None, qty=4, timestamp=datetime(2025, 10, 5, 15, 0)),
                ProductMovement(movement_id='M022', product_id='P002', from_location='L004', to_location='L002', qty=8, timestamp=datetime(2025, 10, 6, 10, 0))
            ]
            db.session.add_all(movements)
            db.session.commit()
            
            print("Database initialized with sample data!")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
