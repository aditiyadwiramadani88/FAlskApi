from flask_api import FlaskAPI,status
from flask import request
from flask_sqlalchemy import SQLAlchemy


app = FlaskAPI(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)

class MydbA(db.Model):
    __tablename__ = 'Blog'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(180))
    def __repr__(self):
        return '<MydbA {}>'.format(self.nama)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        data =  request.data
        query = MydbA(nama=data['nama'])
        db.session.add(query)
        db.session.commit()
        return data, status.HTTP_201_CREATED
    rows = MydbA.query.all()
    data = [{'nama': i.nama} for i in rows]
    return data


@app.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def details(id):
    data = MydbA.query.filter_by(id=id)
    if not data.first():
        return {'msg': "id not fout"}, status.HTTP_404_NOT_FOUND
    if request.method == "PUT":
        data1 = request.data
        data.update({'nama': data1['nama']})
        db.session.commit()
        return data1, status.HTTP_201_CREATED
    elif request.method == "DELETE":
        data.delete()
        db.session.commit()
        return {'msg': 'sucess delete data'}, status.HTTP_204_NO_CONTENT
    return {'nama': data.first().nama}
           
if __name__ == '__main__':
       app.run(threaded=True, port=5000)
    
    
