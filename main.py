from src.utils import *
import sqlite3
from flask import Flask, Response, render_template, jsonify, request, redirect, make_response, url_for
app = Flask(__name__)




@app.route("/")
def api():
    if request.cookies.get("auth-usr") == "rajib" or request.cookies.get("auth-usr") == "mehedi":
        return redirect("/order")
    elif request.cookies.get("auth-usr") == "shazin":
        return redirect("/dashboard")
    else:
        return render_template("index.html")

@app.route('/api/auth', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "shazin":
            if password == "shazin45":
                resp = make_response(redirect("/dashboard"))
                resp.set_cookie("auth-usr", "shazin", 24*60*60*30)
                return resp
            else:
                return "Invalid password <a href='/'>Try Again</a>"
        elif username =="rajib":
            if password == "rajib#12":
                resp = make_response(redirect("/order"))
                resp.set_cookie("auth-usr", "rajib", max_age=24 * 60 * 60* 30)
                return resp
            else:
                return "Invalid password <a href='/'>Try Again</a>"
        elif username =="mehedi":
            if password == "mehedi#69":
                resp = make_response(redirect("/order"))
                resp.set_cookie("auth-usr", "mehedi", max_age=24 * 60 * 60* 30)
                return resp
            else:
                return "Invalid password <a href='/'>Try Again</a>"
        else:
            return "Invalid username <a href='/'>Try Again</a>"
    else:
        return 'Method not allowed'

@app.route("/order")
def order():
    if request.cookies.get("auth-usr")  == "rajib" or request.cookies.get("auth-usr") == "mehedi":
        status = request.args.get('status')
        return render_template("order.html",  success=(status == 'success'), user = request.cookies.get("auth-usr"))
    else:
        return redirect("/")

@app.route("/logout")
def logout():
    auth_usr = request.cookies.get("auth-usr")
    if auth_usr == "rajib" or auth_usr == "mehedi" or auth_usr == "shazin":
        resp = make_response(redirect("/"))
        resp.set_cookie("auth-usr", auth_usr, 0)
        return resp
    else:
        return redirect("/")

@app.route("/dashboard")
def dashboard():
    if request.cookies.get("auth-usr")  == "shazin":
        return render_template("dashboard.html")
    else:
        return "Unauthorized page motherfucker"

@app.route('/submit_order', methods=['POST'])
def submit_order():
    try:
        # SQLite3 database connection
        conn = sqlite3.connect('src/db/data.db')
        cursor = conn.cursor()
        # Get form inputs
        link = sanitize_input(request.form['url'])
        line1 = sanitize_input(request.form['line1'])
        line2 = sanitize_input(request.form['line2'])
        duration = int(request.form['duration'])
        order_type = sanitize_input(request.form['type'])

        # Check for empty fields
        if not all([link, line1, line2, duration, order_type]):
            raise ValueError('All fields are required.')

        # Generate a random order ID
        order_id = generate_order_id()
        submitted_by = request.cookies.get("auth-usr")
        # Save the order to the database
        cursor.execute('''INSERT INTO orders (submitted_by, link, type, line1, line2, duration, order_id) 
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', (submitted_by, link, order_type, line1, line2, duration, order_id))
        conn.commit()
        conn.close()

        return redirect("/order?status=success")
    except Exception as e:
        return f'Error: {str(e)}'
    

@app.route('/api/get_orders', methods=['GET'])
def get_orders():
    try:
        conn = sqlite3.connect('src/db/data.db')
        cursor = conn.cursor()
        # Retrieve data from the database
        cursor.execute('''SELECT * FROM orders''')
        orders = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Convert the data to a JSON response
        orders_json = []
        for order in orders:
            order_dict = {
                'id': order[0],
                'submitted_by': order[1],
                'link': order[2],
                'type': order[3],
                'line1': order[4],
                'line2': order[5],
                'duration': order[6],
                'order_id': order[7],
                'complete': order[8]
            }
            orders_json.append(order_dict)

        return jsonify({'orders': orders_json})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/update/status', methods=['POST'])
def update_status():
    data = request.get_json()
    order_id = data.get('id')
    new_status = data.get('complete')
    conn = sqlite3.connect('src/db/data.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET complete = ? WHERE id = ?", (new_status, order_id))
    conn.commit()

    return jsonify({'message': 'Status updated successfully'})

def main():
    app.run()

if __name__ == "__main__":
    main()
