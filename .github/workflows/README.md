# GitHub Actions 工作流说明

## 工作流列表

### 1. Lint (`lint.yml`)

**触发条件**：
- 推送到 `main` 或 `develop` 分支
- 创建 Pull Request

**功能**：
- Python 代码检查（flake8, black, pylint, mypy）
- Shell 脚本检查（ShellCheck）
- Markdown 检查（markdownlint）
- YAML 检查（yamllint）
- Batch 脚本检查

### 2. Publish (`publish.yml`)

**触发条件**：
- 推送版本标签（格式：`v*.*.*`，如 `v1.0.0`）
- 手动触发（workflow_dispatch）

**功能**：
- 自动发布到 npm
- 自动发布到 PyPI
- 自动创建 GitHub Release

**所需 Secrets**：
- `NPM_TOKEN`: npm 访问令牌
- `PYPI_TOKEN`: PyPI API 令牌
- `TEST_PYPI_TOKEN` (可选): TestPyPI 令牌

**使用示例**：
```bash
# 创建标签触发发布
git tag v1.0.1
git push origin v1.0.1
```

### 3. Version Bump Helper (`version-bump.yml`)

**触发条件**：手动触发（workflow_dispatch）

**功能**：
- 自动升级版本号（patch/minor/major）
- 更新 `package.json`
- 更新 `pyproject.toml`
- 更新 `auto_mouse_mover/__init__.py`
- 可选创建 Pull Request

**使用步骤**：
1. 访问 GitHub Actions 页面
2. 选择 "Version Bump Helper" 工作流
3. 点击 "Run workflow"
4. 选择版本类型（patch/minor/major）
5. 选择是否创建 Pull Request
6. 运行工作流

### 4. Renovate Auto-Approve (`renovate-auto-approve.yml`)

**触发条件**：Renovate 创建的 Pull Request

**功能**：
- 自动测试 Renovate 的依赖更新
- 测试通过后自动批准 PR（仅限 patch 版本）

## 发布流程示例

### 完整发布流程

1. **开发功能**：
   ```bash
   git checkout -b feature/new-feature
   # ... 开发代码 ...
   git commit -m "feat: add new feature"
   git push origin feature/new-feature
   ```

2. **创建 Pull Request**：
   - 在 GitHub 上创建 PR
   - Lint 工作流会自动运行检查

3. **合并 PR**：
   - 审查并合并 PR 到 main 分支

4. **升级版本**：
   - 方式 A：使用 Version Bump Helper 工作流
   - 方式 B：手动编辑版本文件

5. **创建标签并发布**：
   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```
   - Publish 工作流会自动运行并发布到 npm 和 PyPI

## 配置 Secrets

### 获取 npm Token

1. 访问 https://www.npmjs.com/settings/YOUR_USERNAME/tokens
2. 点击 "Generate New Token"
3. 选择 "Automation" 类型
4. 复制生成的 token
5. 在 GitHub 仓库设置中添加为 Secret：`NPM_TOKEN`

### 获取 PyPI Token

1. 访问 https://pypi.org/manage/account/token/
2. 点击 "Add API token"
3. 输入 token 名称（如：`github-actions`）
4. 选择作用域（整个账户或特定项目）
5. 复制生成的 token（只显示一次！）
6. 在 GitHub 仓库设置中添加为 Secret：`PYPI_TOKEN`

### 配置 Secrets 步骤

1. 访问 GitHub 仓库
2. 点击 "Settings" → "Secrets and variables" → "Actions"
3. 点击 "New repository secret"
4. 输入名称和值
5. 点击 "Add secret"

## 故障排除

### 发布失败

1. **检查 Secrets**：确保所有必需的 Secrets 都已配置
2. **检查版本号**：确保版本号格式正确且未被使用
3. **查看日志**：在 GitHub Actions 中查看详细错误信息

### 版本冲突

如果版本号已存在：
- npm: 需要更新版本号
- PyPI: 无法覆盖已发布的版本，必须使用新版本号

### 权限错误

确保：
- npm token 有发布权限
- PyPI token 有效且未过期
- GitHub token 有创建 Release 的权限

