from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


db = SQLAlchemy()

catch = db.Table(
    'catch',
    db.Column('poke_id', db.Integer, db.ForeignKey('pokemon.id'), nullable=False),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    wins= db.Column(db.Integer)
    losses = db.Column(db.Integer)
    caught = db.relationship('Pokemon', secondary='catch', backref= 'caught', lazy ='dynamic')

#as an example for backref
#with the post below
# p1 = Post()
# p1.author
    def catch_poke(self, pokemon):
        self.caught.append(pokemon)
        db.session.commit()

    def release(self, pokemon):
        self.caught.remove(pokemon)
        db.session.commit()

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.wins = 0
        self.losses = 0
        #self.password = password   ---OLD  not hashed

    def saveUser(self):
        db.session.add(self)
        db.session.commit()
    
    def win(self):
        self.wins += 1
        db.session.commit()
    
    def lose(self):
        self.losses += 1
        db.session.commit()

    
class Pokemon(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    ability= db.Column(db.String)
    front_shiny = db.Column(db.String)
    base_atk = db.Column(db.Integer)
    base_hp = db.Column(db.Integer)
    base_def = db.Column(db.Integer)
    isCaught = db.Column(db.Boolean, default=False)
    caught_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = True)

    def gotCaught(self):
        self.isCaught= not self.isCaught
        db.session.commit()

    def __init__(self, front_shiny, name, ability, base_hp, base_atk, base_def):
        self.front_shiny = front_shiny               
        self.name = name
        self.ability = ability
        self.base_hp = base_hp
        self.base_atk = base_atk
        self.base_def = base_def

    def convertDict(self):
        return {"Name": self.name,
                 "Ability": self.ability,
                 "Front Shiny": self.front_shiny,
                 "Base ATK": self.base_atk,
                 "Base HP": self.base_hp,
                 "Base DEF": self.base_def}
    def savePokemon(self):
        db.session.add(self)
        db.session.commit()

    # def caughtBy(self,user_id):
    #     self.caught_by.append(user_id)
    #     db.session.commit()