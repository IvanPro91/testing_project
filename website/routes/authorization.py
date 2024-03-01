from website.includes.database.database_models import *
from flask_restful import Resource, reqparse
from flask import jsonify
import pathlib
import jwt

resolve_path = str(pathlib.Path().resolve())

class user_login(Resource):
    '''
    Для проверки токена пользователя в дальнейшем использовании, следует создать декоратор проверки токена в запросе.
    '''
    def post(self):
        data = reqparse.request.data
        if len(data) == 0: return jsonify({"status": False, "error": "Data cannot be found!"})

        # Если данные есть, то сериализуем и забираем нужные значения
        json_req_data = reqparse.request.json
        login = json_req_data.get("login", False)
        password = json_req_data.get("password", False)

        # Проверяем данные от пользователя API
        if not login: return jsonify({"status": False, "error": "Error value 'login'"})
        if not password: return jsonify({"status": False, "error": "Error value 'password'"})

        # Ищем пользователя по логину (При этом не даем пользователю понять что есть такой username)
        findUser = Users.query.filter(Users.login == login).first()
        if not findUser: return jsonify({"status": False, "error": "User not found or password not valid"})

        # Если пользователь найден, ищем по паролю, предварительно проверив его.
        chk_password = findUser.check_password(password)
        if not chk_password: return jsonify({"status": False, "error": "User not found or password not valid!"})

        token = jwt.encode({"login": login}, key="secret_key_token")
        return jsonify({"token": token.decode("utf-8")})


class user_registration(Resource):
    def post(self):
        data = reqparse.request.data
        if len(data) == 0: return jsonify({"status": False, "error": "Data cannot be found!"})

        # Если данные есть, то сериализуем и забираем нужные значения
        json_req_data = reqparse.request.json
        username = json_req_data.get("username", False)
        login = json_req_data.get("login", False)
        password = json_req_data.get("password", False)

        # Проверяем данные от пользователя API
        if not username: return jsonify({"status": False, "error": "Error value 'username'"})
        if not login: return jsonify({"status": False, "error": "Error value 'login'"})
        if not password: return jsonify({"status": False, "error": "Error value 'password'"})

        # Ищем пользовательский логон в таблице
        findUser = Users.query.filter(Users.login == login).first()
        if not findUser:
            # Если пользователя нет, то создаем его
            user = Users(username=username, login=login)
            db.session.add(user)
            db.session.commit()
            db.session.flush()

            user.set_password(password)
            db.session.commit()
            return jsonify({"status": True, "msg": "Registration successful"})
        else:
            return jsonify({"status": False, "error": "Login already exists!"})
