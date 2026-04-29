from . import db

class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.String(100), nullable=True)

    @classmethod
    def create(cls, recipe_id, name, quantity=None):
        new_ingredient = cls(recipe_id=recipe_id, name=name, quantity=quantity)
        db.session.add(new_ingredient)
        db.session.commit()
        return new_ingredient

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, ingredient_id):
        return cls.query.get(ingredient_id)

    def update(self, name=None, quantity=None):
        if name is not None:
            self.name = name
        if quantity is not None:
            self.quantity = quantity
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
