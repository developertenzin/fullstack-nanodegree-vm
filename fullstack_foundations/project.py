from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Making an API Endpoint (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()

    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def restaurantMenuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(menu_item = item.serialize)

@app.route('/')
@app.route('/restaurants/')
def allRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurants/new/', methods=["GET", "POST"])
def newRestaurant():
    if request.method == "POST":
        new_restaurant = Restaurant(name=request.form["name"])
        session.add(new_restaurant)
        session.commit()
        return redirect(url_for('allRestaurants'))
    else:
        return render_template('new_restaurant.html')

@app.route('/restaurants/<int:restaurant_id>/edit/', methods=["GET", "POST"])
def editRestaurant(restaurant_id):
    edited_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == "POST":
        if request.form['name']:
            edited_restaurant.name = request.form['name']
        session.add(edited_restaurant)
        session.commit()
        return redirect(url_for('allRestaurants'))
    else:
        return render_template('edit_restaurant.html', restaurant_id=restaurant_id, edited_restaurant=edited_restaurant)

@app.route('/restaurants/<int:restaurant_id>/delete/', methods=["GET", "POST"])
def deleteRestaurant(restaurant_id):
    selected_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == "POST":
        session.delete(selected_restaurant)
        session.commit()
        return redirect(url_for('allRestaurants'))
    else:
        return render_template('delete_restaurant.html', restaurant_id=restaurant_id, selected_restaurant=selected_restaurant)

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template("menu.html", restaurant=restaurant, items=items)
# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=["GET", "POST"])
def newMenuItem(restaurant_id):
    if request.method == "POST":
        new_item = MenuItem(name=request.form["name"], restaurant_id = restaurant_id)
        session.add(new_item)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template("new_menu_item.html", restaurant_id = restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=["GET", "POST"])
def editMenuItem(restaurant_id, menu_id):
    edited_item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == "POST":
        if request.form['name']:
            edited_item.name = request.form['name']
        session.add(edited_item)
        session.commit()
        flash('Menu Item has been edited!')
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('edit_menu_item.html', restaurant_id = restaurant_id, menu_id = menu_id, i = edited_item)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=["GET", "POST"])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == "POST":
        session.delete(deletedItem)
        session.commit()
        flash("Menu Item has been deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('delete_menu_item.html', restaurant_id=restaurant_id, menu_id=menu_id, i=deletedItem)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=4000)
