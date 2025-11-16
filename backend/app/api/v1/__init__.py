"""API路由模块初始化"""
from fastapi import APIRouter

# 创建空的路由器，后续会在main.py中导入具体路由
router = APIRouter()

# 这些文件会在后续创建
# from . import tender, bidding, document, template, checker, user