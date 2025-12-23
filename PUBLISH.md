# 发布指南

本指南包含将项目发布到 npm 和 PyPI 的详细步骤。

---

# 发布到 npm

## 准备工作

## 准备工作

### 1. 注册 npm 账号

如果还没有 npm 账号，访问 [npmjs.com](https://www.npmjs.com/signup) 注册。

### 2. 登录 npm

```bash
npm login
```

输入你的用户名、密码和邮箱。

### 3. 检查包名可用性

```bash
npm view auto-mouse-mover
```

如果返回 404，说明包名可用。如果已被占用，需要修改 `package.json` 中的 `name` 字段。

## 发布步骤

### 1. 更新版本号

使用语义化版本号（Semantic Versioning）：

```bash
# Patch 版本（修复 bug）
npm version patch

# Minor 版本（新功能）
npm version minor

# Major 版本（破坏性更改）
npm version major
```

或者手动编辑 `package.json` 中的 `version` 字段。

### 2. 测试本地安装

```bash
# 在项目根目录
npm link

# 测试命令
auto-mouse-mover --help
amm --help
```

### 3. 构建和检查

```bash
# 检查将要发布的文件
npm pack --dry-run

# 实际打包（不发布）
npm pack
```

### 4. 发布

```bash
# 发布到 npm
npm publish

# 如果包名包含作用域，需要指定访问权限
npm publish --access public
```

### 5. 验证发布

```bash
# 查看已发布的包信息
npm view auto-mouse-mover

# 测试安装
npm install -g auto-mouse-mover
auto-mouse-mover --help
```

## 发布后

### 1. 创建 Git 标签

```bash
git tag v1.0.0
git push origin v1.0.0
```

### 2. 更新 GitHub Release

在 GitHub 上创建 Release，包含：
- 版本号
- 更新日志
- 下载链接

### 3. 更新文档

确保 README 中的安装说明和示例都是最新的。

## 常见问题

### 包名已被占用

修改 `package.json` 中的 `name` 字段，可以使用：
- 添加作用域：`@your-username/auto-mouse-mover`
- 使用不同的名称

### 发布权限错误

确保：
1. 已登录正确的 npm 账号
2. 包名没有被其他人占用
3. 如果使用作用域包，需要设置 `"access": "public"`

### 版本号冲突

如果版本号已存在，需要更新版本号后再发布。

## 自动化发布（可选）

可以使用 GitHub Actions 自动发布：

1. 创建 `.github/workflows/publish.yml`
2. 配置 npm token 为 GitHub Secret
3. 在发布标签时自动触发发布

## 维护

发布后需要：
- 及时响应 Issue 和 PR
- 定期更新依赖
- 修复 bug 并发布补丁版本
- 添加新功能并发布小版本

---

# 发布到 PyPI

## 准备工作

### 1. 注册 PyPI 账号

如果还没有 PyPI 账号，访问 [pypi.org](https://pypi.org/account/register/) 注册。

**注意**: 需要分别注册：
- **PyPI (生产环境)**: https://pypi.org
- **TestPyPI (测试环境)**: https://test.pypi.org

### 2. 安装构建工具

```bash
pip install --upgrade build twine
```

### 3. 检查包名可用性

```bash
# 检查 PyPI
pip search auto-mouse-mover 2>/dev/null || echo "包名可能可用"

# 或直接访问
# https://pypi.org/project/auto-mouse-mover/
```

如果包名已被占用，需要修改 `pyproject.toml` 中的 `name` 字段。

## 发布步骤

### 1. 更新版本号

编辑 `pyproject.toml` 中的 `version` 字段：

```toml
[project]
version = "1.0.0"  # 更新版本号
```

使用语义化版本号（Semantic Versioning）：
- **Patch** (1.0.0 → 1.0.1): 修复 bug
- **Minor** (1.0.0 → 1.1.0): 新功能
- **Major** (1.0.0 → 2.0.0): 破坏性更改

### 2. 清理旧的构建文件

```bash
rm -rf dist/ build/ *.egg-info/
```

### 3. 构建分发包

```bash
# 使用现代构建工具（推荐）
python -m build

# 这会创建：
# - dist/auto_mouse_mover-1.0.0.tar.gz (源码分发包)
# - dist/auto_mouse_mover-1.0.0-py3-none-any.whl (wheel 包)
```

### 4. 检查构建的包

```bash
# 检查包内容
twine check dist/*

# 查看将要上传的文件
tar -tzf dist/auto_mouse_mover-*.tar.gz
```

### 5. 测试发布到 TestPyPI（推荐）

```bash
# 上传到 TestPyPI
twine upload --repository testpypi dist/*

# 测试安装
pip install --index-url https://test.pypi.org/simple/ auto-mouse-mover

# 测试运行
auto-mouse-mover --help
```

### 6. 发布到 PyPI

```bash
# 上传到 PyPI
twine upload dist/*

# 或者使用 API token（推荐）
# 在 https://pypi.org/manage/account/token/ 创建 token
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-xxxxxxxxxxxxx
twine upload dist/*
```

### 7. 验证发布

```bash
# 查看已发布的包信息
pip show auto-mouse-mover

# 测试安装
pip install auto-mouse-mover

# 测试运行
auto-mouse-mover --help
amm --help

# 测试模块方式运行
python -m auto_mouse_mover --help
```

## 发布后

### 1. 创建 Git 标签

```bash
git tag v1.0.0
git push origin v1.0.0
```

### 2. 更新 GitHub Release

在 GitHub 上创建 Release，包含：
- 版本号
- 更新日志
- PyPI 和 npm 的安装链接

### 3. 更新文档

确保 README 中的安装说明和示例都是最新的。

## 常见问题

### 包名已被占用

修改 `pyproject.toml` 中的 `name` 字段，可以使用：
- 添加下划线：`auto_mouse_mover`
- 使用不同的名称

### 上传权限错误

确保：
1. 已登录正确的 PyPI 账号
2. 包名没有被其他人占用
3. 使用 API token 而不是密码（推荐）

### 版本号冲突

如果版本号已存在，需要更新版本号后再发布。PyPI 不允许覆盖已发布的版本。

### 构建错误

确保：
1. `pyproject.toml` 配置正确
2. 所有必需的文件都在 `MANIFEST.in` 中
3. Python 版本符合要求（>=3.11）

## 自动化发布（可选）

可以使用 GitHub Actions 自动发布：

1. 创建 `.github/workflows/publish-pypi.yml`
2. 配置 PyPI API token 为 GitHub Secret
3. 在发布标签时自动触发发布

## 维护

发布后需要：
- 及时响应 Issue 和 PR
- 定期更新依赖
- 修复 bug 并发布补丁版本
- 添加新功能并发布小版本

## 同时发布到 npm 和 PyPI

如果同时维护两个平台：

```bash
# 1. 更新版本号（两个文件都要更新）
# - package.json (npm)
# - pyproject.toml (PyPI)

# 2. 构建 npm 包
npm pack

# 3. 构建 PyPI 包
python -m build

# 4. 发布到 npm
npm publish

# 5. 发布到 PyPI
twine upload dist/*

# 6. 创建 Git 标签
git tag v1.0.0
git push origin v1.0.0
```

