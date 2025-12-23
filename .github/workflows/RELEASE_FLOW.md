# 自动发布流程说明 / Auto Release Flow Documentation

## 工作流程概览 / Workflow Overview

```
提交代码 (Conventional Commits)
    ↓
release-please.yml 检测到新提交
    ↓
创建 Release PR (包含版本更新和 CHANGELOG)
    ↓
合并 Release PR
    ↓
release-please 自动创建 GitHub Release 和 tag (v*.*.*)
    ↓
触发 publish.yml (通过 push tags 或 release published 事件)
    ↓
┌─────────────────┬─────────────────┐
│  publish-npm    │  publish-pypi   │
│  (发布到 npm)   │  (发布到 PyPI)  │
└─────────────────┴─────────────────┘
    ↓
触发 build-release-assets.yml (通过 push tags 或 release published 事件)
    ↓
构建各平台可执行文件并上传到 GitHub Releases
```

## 详细说明 / Detailed Explanation

### 1. release-please.yml

**触发条件：**
- `push` 到 `main` 分支
- 手动触发 (`workflow_dispatch`)

**功能：**
- 检测符合 Conventional Commits 规范的提交
- 根据提交类型决定版本号（`feat:` → minor, `fix:` → patch, `BREAKING CHANGE` → major）
- 创建 Release PR，包含：
  - 版本号更新（`package.json`, `pyproject.toml`, `auto_mouse_mover/__init__.py`）
  - CHANGELOG 更新

**合并 PR 后：**
- release-please 自动创建 GitHub Release
- 自动创建 tag（格式：`v*.*.*`）

### 2. publish.yml

**触发条件：**
- `push` tags（`v*.*.*`）- 当 release-please 创建 tag 时触发
- `release` published - 当 release-please 创建 release 时触发
- `workflow_dispatch` - 手动触发

**包含的 Jobs：**

#### publish-npm (第 18-73 行)
- **功能：** 发布到 npm
- **步骤：**
  1. 提取版本号
  2. 更新 `package.json` 版本
  3. 安装依赖
  4. 构建包
  5. 发布到 npm
  6. 验证发布

#### publish-pypi (第 74-146 行)
- **功能：** 发布到 PyPI
- **步骤：**
  1. 提取版本号
  2. 更新 `pyproject.toml` 和 `auto_mouse_mover/__init__.py` 版本
  3. 安装构建工具
  4. 构建 Python 包
  5. 检查包
  6. 发布到 PyPI
  7. 验证发布

#### create-release (第 148-213 行)
- **功能：** 创建或更新 GitHub Release
- **依赖：** `publish-npm` 和 `publish-pypi`
- **说明：** 如果 release-please 已经创建了 release，这个 job 会更新它

### 3. build-release-assets.yml

**触发条件：**
- `push` tags（`v*.*.*`）
- `release` published
- `workflow_dispatch` - 手动触发

**功能：**
- 为 Windows、macOS、Linux 构建可执行文件
- 使用 PyInstaller 打包
- 上传构建产物到 GitHub Releases

## 完整流程示例 / Complete Flow Example

1. **开发者提交代码：**
   ```bash
   git commit -m "feat: add new feature"
   git push origin main
   ```

2. **release-please 检测到提交：**
   - 运行 `release-please.yml`
   - 创建 Release PR（例如：`chore: release 1.1.0`）

3. **合并 Release PR：**
   - release-please 自动创建：
     - GitHub Release: `v1.1.0`
     - Git tag: `v1.1.0`

4. **触发发布工作流：**
   - `publish.yml` 被触发（通过 `push tags` 或 `release published` 事件）
   - 并行运行：
     - `publish-npm` → 发布到 npm
     - `publish-pypi` → 发布到 PyPI
   - `build-release-assets.yml` 被触发
     - 构建各平台可执行文件
     - 上传到 GitHub Releases

5. **完成：**
   - npm: `npm install -g auto-mouse-mover@1.1.0`
   - PyPI: `pip install auto-mouse-mover==1.1.0`
   - GitHub Releases: 可下载可执行文件

## 关键文件位置 / Key File Locations

- **发布到 npm 的 job:** `.github/workflows/publish.yml` → `publish-npm` (第 18-73 行)
- **发布到 PyPI 的 job:** `.github/workflows/publish.yml` → `publish-pypi` (第 74-146 行)
- **构建可执行文件:** `.github/workflows/build-release-assets.yml`
- **版本管理:** `.github/workflows/release-please.yml`

## 注意事项 / Notes

1. **需要配置 Secrets：**
   - `NPM_TOKEN` - npm 发布令牌
   - `PYPI_TOKEN` - PyPI 发布令牌

2. **release-please 不会自动发布：**
   - release-please 只负责版本管理和创建 Release PR
   - 实际的发布（npm/PyPI）由 `publish.yml` 完成

3. **触发机制：**
   - 当 release-please 创建 tag 时，`publish.yml` 通过 `push tags` 事件触发
   - 当 release-please 创建 release 时，`publish.yml` 通过 `release published` 事件触发

