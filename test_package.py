#!/usr/bin/env python3
"""
快速测试包结构是否正确
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

import os

# 测试文件结构
print("测试包文件结构...")
package_dir = "auto_mouse_mover"
required_files = ['__init__.py', '__main__.py', 'move_mouse.py']

all_exist = True
for file in required_files:
    file_path = os.path.join(package_dir, file)
    if os.path.exists(file_path):
        print(f"✅ {file} 存在")
    else:
        print(f"❌ {file} 不存在")
        all_exist = False

if not all_exist:
    print("\n❌ 包结构不完整！")
    sys.exit(1)

# 测试 __init__.py 内容
print("\n测试 __init__.py...")
try:
    with open(os.path.join(package_dir, '__init__.py'), 'r') as f:
        content = f.read()
        if '__version__' in content:
            print("✅ __version__ 定义存在")
        if '__author__' in content:
            print("✅ __author__ 定义存在")
        if 'move_mouse' in content:
            print("✅ move_mouse 导入存在")
except Exception as e:
    print(f"❌ 读取 __init__.py 失败: {e}")
    sys.exit(1)

# 测试 move_mouse.py 内容
print("\n测试 move_mouse.py...")
try:
    with open(os.path.join(package_dir, 'move_mouse.py'), 'r') as f:
        content = f.read()
        if 'def move_mouse' in content:
            print("✅ move_mouse 函数存在")
        if 'def main' in content:
            print("✅ main 函数存在")
except Exception as e:
    print(f"❌ 读取 move_mouse.py 失败: {e}")
    sys.exit(1)

print("\n✅ 包结构测试通过！")
print("   注意: 功能测试需要安装 pyautogui 依赖")
print("   运行 'pip install pyautogui' 后可以测试完整功能")

