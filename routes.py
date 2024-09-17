from flask import render_template, jsonify, request, session, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from binance import Client

from kyklos.kyklos import Kyklos

def register_routes(app, db, bcrypt):

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'GET':
            return render_template('register.html')
        
        elif request.method == 'POST':
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

            # Check if user already exists
            if User.query.filter_by(username=username).first():
                return jsonify({"status": "error", "message": "Username already exists!"}), 400

            user = User(username=username, password_hash=password_hash)

            db.session.add(user)
            db.session.commit()

            return jsonify({"status": "success", "message": "User created successfully!"}), 201
        
        return jsonify({"status": "error", "message": "Method not allowed!"}), 405

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        
        elif request.method == 'POST':
            try:
                data = request.get_json()
                username = data.get('username')
                password = data.get('password')

                if not username or not password:
                    return jsonify({"status": "error", "message": "Username and password are required!"}), 400

                user = User.query.filter_by(username=username).first()

                if user and bcrypt.check_password_hash(user.password_hash, password):
                    login_user(user)
                    return jsonify({"status": "success", "message": "User logged in successfully!"}), 200
                else:
                    return jsonify({"status": "error", "message": "Invalid credentials!"}), 401

            except Exception as e:
                # Log the error for debugging
                print(f"Error occurred: {e}")
                return jsonify({"status": "error", "message": "An error occurred while processing your request"}), 500

        return jsonify({"status": "error", "message": "Method not allowed!"}), 405


    @app.route('/logout', methods=['GET','POST'])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))
    
    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        if request.method == 'GET':
            user = User.query.get(current_user.uid)
            return render_template('profile.html', user=user)
        
        elif request.method == 'POST':
            phone_number = request.form.get('phone_number')
            binance_api_key = request.form.get('binance_api_key')
            binance_secret_key = request.form.get('binance_secret_key')

            user = User.query.get(current_user.uid)
            user.phone_number = phone_number
            user.binance_api_key = binance_api_key
            user.binance_secret_key = binance_secret_key

            db.session.commit()

            return redirect(url_for('profile'))

    @app.route('/trade', methods=['GET', 'POST'])
    @login_required
    def trade():
        if request.method == 'GET':
            user = User.query.get(current_user.uid)

            API_KEY = user.binance_api_key
            SECRET_KEY = user.binance_secret_key

            client = Client(API_KEY,SECRET_KEY)

            price = client.get_symbol_ticker(symbol="BTCUSDT")
            order_book = client.get_order_book(symbol="BTCUSDT")

            return render_template('trade.html', depth=price, order_book=order_book)
        
        elif request.method == 'POST':
            pass


