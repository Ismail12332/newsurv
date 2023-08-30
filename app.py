from flask import Flask, render_template, request, session, redirect
from pymongo import MongoClient
import secrets
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.secret_key = secrets.token_hex(16)  # Генерируем случайный ключ из 16 байт (32 символа)
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.my_database

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            session['first_name'] = request.form.get("first_name")
            session['last_name'] = request.form.get("last_name")
            session['city'] = request.form.get("city")
            session['phone'] = request.form.get("phone")
            session['post'] = request.form.get("post")

            return redirect("/page2")  # Перенаправляем на вторую страницу
        
        return render_template("home.html")

    @app.route('/page2', methods=["GET", "POST"])
    def page2():
        if request.method == "POST":
            fields = ["selected_choice_1", "selected_choice_2", "selected_choice_3"]
            custom_fields = ["custom_choice_1", "custom_choice_2", "custom_choice_3"]

            data = {
                "first_name": session.get('first_name'),
                "last_name": session.get('last_name'),
                "city": session.get('city'),
                "phone": session.get('phone'),
                "post": session.get('post')
            }

            for field, custom_field in zip(fields, custom_fields):
                selected_choice = request.form.get(field)
                custom_choice = request.form.get(custom_field)
                data[field] = custom_choice if custom_choice else selected_choice

            app.db.order.insert_one(data)
            print("Entry added:", data)

        return render_template("page2.html", data=session)  # Передаем данные сессии в шаблон

    if __name__ == "__main__":
        app.run(debug=True)
    return app