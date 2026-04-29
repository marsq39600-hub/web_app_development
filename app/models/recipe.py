from . import db
from datetime import datetime

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 與 Ingredient 和 Step 的關聯 (一對多)
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True, cascade="all, delete-orphan")
    steps = db.relationship('Step', backref='recipe', lazy=True, cascade="all, delete-orphan")

    @classmethod
    def create(cls, title, description=None):
        new_recipe = cls(title=title, description=description)
        db.session.add(new_recipe)
        db.session.commit()
        return new_recipe

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, recipe_id):
        return cls.query.get(recipe_id)

    def update(self, title=None, description=None):
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
