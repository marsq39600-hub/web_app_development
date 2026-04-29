from . import db

class Step(db.Model):
    __tablename__ = 'steps'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)

    @classmethod
    def create(cls, recipe_id, step_number, content):
        new_step = cls(recipe_id=recipe_id, step_number=step_number, content=content)
        db.session.add(new_step)
        db.session.commit()
        return new_step

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.step_number.asc()).all()

    @classmethod
    def get_by_id(cls, step_id):
        return cls.query.get(step_id)

    def update(self, step_number=None, content=None):
        if step_number is not None:
            self.step_number = step_number
        if content is not None:
            self.content = content
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
