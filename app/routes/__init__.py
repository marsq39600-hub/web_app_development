from flask import Blueprint

# 建立名為 main 的 Blueprint，負責所有前台路由
main_bp = Blueprint('main', __name__)

# 匯入 main_routes 使裡面的路由能註冊到 Blueprint 內
from . import main_routes
