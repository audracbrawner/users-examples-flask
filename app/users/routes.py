from flask_restx import Namespace, Resource, abort, fields, Api
from flask import request, Blueprint


# Blueprint
users_bp = Blueprint("users", __name__)

# RESTX API attached to blueprint
api = Api(users_bp, title="Users API", version="1.0")

api_ns = Namespace("users", description="Users API",path="/api/")

users = [
    {"id": 1001, "name": "mina", "age": 30},
    {"id": 1002, "name": "ali", "age": 20},
    {"id": 1003, "name": "sara", "age": 40},
]





user_model = api_ns.model("User",{
    "name" : fields.String(required=True, description="User name"),
    "age" : fields.Integer(required=True, description="User age")
})


@api_ns.route("/users")
class Users(Resource):
    def get(self):
        return users
    
    @api_ns.expect(user_model, validate=True)
    def post(self):
        body = request.json

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

    @api_ns.expect(user_model, validate=True)
    def put(self,user_id):
        body = request.json

        for user in users:
            if user["id"] == user_id :
                user["name"] = body.get("name")
                user["age"] = body.get("age")
            return user,200
    

    
        