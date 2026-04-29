from flask import render_template, request, redirect, url_for, flash
from . import main_bp
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient
from app.models.step import Step
from app.models import db

@main_bp.route('/')
def index():
    recipes = Recipe.get_all()
    return render_template('index.html', recipes=recipes)

@main_bp.route('/recipe/create', methods=['GET', 'POST'])
def create_recipe():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        if not title:
            flash('菜名為必填欄位', 'error')
            return render_template('create.html')

        new_recipe = Recipe.create(title=title, description=description)

        ingredient_names = request.form.getlist('ingredient_name[]')
        ingredient_quantities = request.form.getlist('ingredient_quantity[]')
        for name, qty in zip(ingredient_names, ingredient_quantities):
            if name.strip():
                Ingredient.create(recipe_id=new_recipe.id, name=name.strip(), quantity=qty.strip())

        step_contents = request.form.getlist('step_content[]')
        for idx, content in enumerate(step_contents, start=1):
            if content.strip():
                Step.create(recipe_id=new_recipe.id, step_number=idx, content=content.strip())

        flash('食譜新增成功！', 'success')
        return redirect(url_for('main.index'))
        
    return render_template('create.html')

@main_bp.route('/recipe/<int:id>')
def recipe_detail(id):
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜', 'error')
        return redirect(url_for('main.index'))
    return render_template('detail.html', recipe=recipe)

@main_bp.route('/recipe/<int:id>/edit', methods=['GET', 'POST'])
def edit_recipe(id):
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜', 'error')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        if not title:
            flash('菜名為必填欄位', 'error')
            return render_template('edit.html', recipe=recipe)

        recipe.update(title=title, description=description)

        # Clear old ingredients and steps
        for ing in recipe.ingredients:
            ing.delete()
        for step in recipe.steps:
            step.delete()

        # Re-add
        ingredient_names = request.form.getlist('ingredient_name[]')
        ingredient_quantities = request.form.getlist('ingredient_quantity[]')
        for name, qty in zip(ingredient_names, ingredient_quantities):
            if name.strip():
                Ingredient.create(recipe_id=recipe.id, name=name.strip(), quantity=qty.strip())

        step_contents = request.form.getlist('step_content[]')
        for idx, content in enumerate(step_contents, start=1):
            if content.strip():
                Step.create(recipe_id=recipe.id, step_number=idx, content=content.strip())

        flash('食譜更新成功！', 'success')
        return redirect(url_for('main.recipe_detail', id=recipe.id))

    return render_template('edit.html', recipe=recipe)

@main_bp.route('/recipe/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    recipe = Recipe.get_by_id(id)
    if recipe:
        recipe.delete()
        flash('食譜已刪除', 'success')
    return redirect(url_for('main.index'))
