from flask_restx import  Namespace, Resource , fields, reqparse
from flask import request
from app.books.models import Book
from app.main import db


books_ns = Namespace("books", description="Books operations")


# Book model for validation & Swagger
book_model = books_ns.model("Book", {
    "title": fields.String(required=True, description="Book title"),
    "author": fields.String(required=True, description="Book author"),
    "price": fields.Float(required=True, description="Book price")
})

delete_parser = reqparse.RequestParser()
delete_parser.add_argument(
    "id",
    type=int,
    required=True,
    help="Book ID is required",
    location="args"
)

@books_ns.route("/<int:book_id>")
class SingleBook(Resource):

    def get(self, book_id):
        book = Book.query.get(book_id)

        if not book:
            return {
                "message": "Book not found",
                "code": "20004"
            }, 404

        return  book.to_dict() , 200
    
    @books_ns.expect(book_model, validate=True)
    def put(self,book_id):
        book = Book.query.get(book_id)
        
        print(type(book))
        
        if not book:
            return {
                "message": "Book not found",
                "code": "20004"
            }, 404

        body = request.json

        try :
            book.title = body.get('title')
            book.author = body.get('author')
            book.price = body.get('price')

            db.session.commit()

            return {
                "message" : "Book updated successfully",
                "data" : book.to_dict(),
                "code" : "10003"
            },200
        except :
            db.session.rollback()
            return {
                "message" : "Internal Server Error",
                "code" : "20001",
            },500

@books_ns.route("")
class Books(Resource):
    def get(self):
        books = Book.query.all()
        return [book.to_dict() for book in books]
    

    @books_ns.expect(book_model, validate=True)
    def post(self):
        body = request.json


        try:
            # Create new book instance
            new_book = Book(
                title=body.get("title"),
                author=body.get("author"),
                price=body.get("price")
            )

            # Add to database
            db.session.add(new_book)
            db.session.commit()

            return { 
                "message" : "Book Created Successfully" , 
                "data" : { "id" : new_book.to_dict()["id"]} , 
                "code" : "10001" 
            }, 201
        except:
            db.session.rollback()
            return {
                "message" : "Internal Server Error",
                "code" : ""
            }, 500
        
    @books_ns.expect(delete_parser)
    def delete(self):
        book_id = request.args.get("id", type=int)
        
        if not book_id:
            return {
                "message": "Book id is required",
                "code": "20005"
            }, 400
        
        book = Book.query.get(book_id)

        if not book:
            return {
                "message": "Book not found",
                "code": "20004"
            }, 404
        
        try:
            db.session.delete(book)
            db.session.commit()
            return {
                "message": "Book deleted successfully",
                "data": book_id,
                "code": "10004"
            }, 200
        except :
            db.session.rollback()
            return{
                "message": "Internal Server Error",
                "code": "20001"
            },500
            

