from flask_restx import Namespace, Resource , abort
from flask import request


users = [
    {"id": 1001, "name": "mina", "age": 30},
    {"id": 1002, "name": "ali", "age": 20},
    {"id": 1003, "name": "sara", "age": 40},
]


api_ns = Namespace("users", description="Users API",path="/api/")



@api_ns.route("/users")
class Users(Resource):
    def get(self):
        return users
    
    def post(self):
        body = request.json
        print(body,'body')
        #simple validation
        if not body : 
            abort(400,"No Input data provided")

        if "name" not in body or "age" not in body:
            abort(400,"name and age are reqired")

        new_id = max(user["id"] for user in users) + 1

        new_user = {
            "id": new_id,
            "name": body.get("name"),
            "age": body.get("age")
        }

        users.append(new_user)

        return new_user,201
    

@api_ns.route("/users/<int:user_id>")
class User(Resource):
    def get(self, user_id):
        for user in users:
            if user["id"] == user_id :
                return user
        
            
        abort(404,"User not found")

    
    def delete(self,user_id):
        for user in users : 
            if user["id"] == user_id :
                users.remove(user)
                return { "message" : "User deleted successfully" }, 200
            
        abort(404,"User not found")


    def put(self,user_id):
        body = request.json

        if not body : 
            abort(400,"No input body provided")

        if "name" not in body or "age" not in body:
            abort(400,"name and age are reqired")

        for user in users:
            if user["id"] == user_id :
                user["name"] = body.get("name")
                user["age"] = body.get("age")
            return user,200
        
        abort(404,"user not found")

    
        