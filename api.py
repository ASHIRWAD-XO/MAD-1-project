from flask_restful import Resource , Api 
from flask import josnify, Flask,request

app=Flask(__name__)
api=Api(app)

class somthing(Resource):
    def post(self):
        return jsonify({'x':'y'})
    
    def get(self):
        return jsonify({'x':'y'})
    

class Square(Resource): 
  
    def get(self, num): 
  
        return jsonify({'square': num**2}) 
  
  
# adding the defined resources along with their corresponding urls 
api.add_resource(somthing, '/') 
api.add_resource(Square, '/square/<int:num>') 
  
  
# driver function 
if __name__ == '__main__': 
  
    app.run(debug = True) 