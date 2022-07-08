from flask import Flask
from flask_restx import Api,Resource,fields,Namespace
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db = SQLAlchemy(app)

api = Namespace('cats', description='Cats related operations')

class Cat(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    ids = db.Column(db.String(40),nullable=False)
    name = db.Column(db.String(40),nullable=False)

    def __repr__(self):
        return self.name


cat = api.model('Cat', {
    'id' : fields.Integer(),
    'ids': fields.String(required=True, description='The cat identifier'),
    'name': fields.String(required=True, description='The cat name'),
})


@api.route('/cats')
class Cats(Resource):

    @api.marshal_list_with(cat,code=200,envelope='cats')
    def get(self):

        cats=Cat.query.all()
        return cats


@api.route('/cats<ids>')
@api.param('id', 'The cat identifier')
@api.response(404, 'Cat not found')
class CatResource(Resource):

    @api.marshal_with(cat,code=200,envelope='cat')
    def get(self, ids):
        '''Fetch a cat given its identifier'''
        CATS = Cat.query.filter_by(ids=ids).first()
        return CATS
        api.abort(404)


@app.shell_context_processor
def make_shell_context():
    return {
        'db':db,
        'Cat':Cat

    }


if __name__ == '__main__':
    app.run(debug=True)
