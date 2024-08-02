from flask import Flask,jsonify,request
from config import Config
# from model import User,db
from model import db,User


#--------------------------------------------------------------------------------------------------------------------------------------------------------

app= Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error':'not found','message':'The requested URL was not found on the server.'}),404



#------get user data from database-------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/users')
def users():
    users= User.query.all()
    #return jsonify({"name":'test user'})
    return jsonify([user.to_dist() for user in users])

#-------save user data on database-------------------------------------------------------------------------------------------------------------------------------------

@app.route('/users', methods=['POST'])
def create_users():
    data = request.get_json()
    new_user=User(username=data['username'],email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    #users= User.query.all()
    #return jsonify({"name":'test user'})
    return jsonify(new_user.to_dist()),201

#------get user by id----------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/users/<int:user_id>',methods=['GET'])
def get_user(user_id):
    user= User.query.get_or_404(user_id)
    return jsonify(user.to_dist())


#-------update-user-----------------------------------------------------------------------------------------------------------------------------------------------
    
@app.route('/users/<int:user_id>',methods=['PUT'])
def update_user(user_id):
    data=request.get_json()
    user=User.query.get_or_404(user_id)
    user.username=data['username']
    user.email=data['email']
    db.session.commit()
    return jsonify(user.to_dist())
    


#--------delete user from database--------------------------------------------------------------------------------------------------------------------------

@app.route('/users/<int:user_id>',methods=['DELETE'])
def delete_user(user_id):
    user= User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify("user delete sussfully....")






#-------create table on database---------------------------------------------------------------------------------------------------------------------------------------------------

if __name__== '__main__':
    with app.app_context(): 
        db.create_all()        #aut create table inside the database
    app.run(debug=True, port=5001)
