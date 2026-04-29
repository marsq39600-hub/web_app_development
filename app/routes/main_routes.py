from flask import render_template, request, redirect, url_for, flash
from . import main_bp
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient
from app.models.step import Step
from app.models import db

@main_bp.route('/')
def index():
    """
    處理首頁請求，取得所有食譜並渲染列表。
    輸入: 無
    處理: 呼叫 Recipe.get_all()
    輸出: 渲染 templates/index.html
    """
    pass

@main_bp.route('/recipe/create', methods=['GET', 'POST'])
def create_recipe():
    """
    處理新增食譜請求。
    GET: 渲染 templates/create.html 顯示空白表單。
    POST: 接收表單資料，寫入 DB (Recipe 主檔及關聯的 Ingredient, Step)，成功後重導向至首頁。
    """
    pass

@main_bp.route('/recipe/<int:id>')
def recipe_detail(id):
    """
    處理單一食譜詳情請求。
    輸入: URL 的食譜 id
    處理: 呼叫 Recipe.get_by_id(id) 撈取相關資料。
    輸出: 渲染 templates/detail.html，若找不到則回傳 404 錯誤或重導向至首頁。
    """
    pass

@main_bp.route('/recipe/<int:id>/edit', methods=['GET', 'POST'])
def edit_recipe(id):
    """
    處理編輯食譜請求。
    GET: 呼叫 Recipe.get_by_id(id) 取得舊資料，渲染 templates/edit.html 帶入表單。
    POST: 接收更新後資料，更新 DB 並重新建立關聯子表單，完成後重導向至詳情頁。
    """
    pass

@main_bp.route('/recipe/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    處理刪除食譜請求。
    輸入: URL 的食譜 id
    處理: 呼叫 Recipe.get_by_id(id) 並執行 delete() 方法，藉由資料庫關聯 (CASCADE) 刪除底下材料與步驟。
    輸出: 重導向至首頁。
    """
    pass
