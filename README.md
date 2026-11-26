# river-ya 的个人知识工作区

个人知识工作区与博客，正式部署目标为 **https://river-ya.github.io/**。默认中文，英文路径使用 `/en/`。所有页面构建为真实的 `index.html`，不依赖 SPA 路由重写、运行时 Node 服务或数据库。

通过 GitHub Actions 验证和发布，部署状态见仓库 Actions。博客入口为 **https://river-ya.github.io/blog/**；已有项目站点 **https://river-ya.github.io/world-scene/** 独立维护。

## 打开与构建

已经生成的 `dist/` 可直接用静态服务器预览。在本目录运行：

```bash
python scripts/preview.py
```

它会打开 `http://127.0.0.1:4173/`，Ctrl+C 停止。Windows 已配置 Python PATH 时，也可双击 `启动预览.bat`。如果命令名是 `python3` 或 `py -3`，相应替换命令即可。**不要双击 `dist/index.html` 使用 `file://` 打开**，站点的根路径资源和搜索需要 HTTP。

修改内容后重新构建，Python 3.11+：

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.lock
python scripts/validate.py
python scripts/build.py
python scripts/validate.py --output
python -B -m unittest discover -s tests -v
```

使用 Jinja、markdown-it-py、Pygments 和 Python TypedDict 内容契约。依赖版本记录在 `requirements.lock`；本地当前环境中这些渲染依赖已预装。本实现是基于成熟模板与 Markdown 库的轻量静态生成器，不是 Astro/Next 项目。构建无需网络，原论文与课程快照已作为内容数据保存。

## 页面与内容

- 已发布的内容统一收录在博客。首页右侧的 AI、算法、Infra 入口链接到 `/blog/category/` 下的博客分类，中英文旧笔记地址会自动跳转。
- 从导航的“终端”可进入 `/terminal/` 或 `/en/terminal/`。输入 `ls` 列出内容，`cd /ai/computer-vision` 切换分类，`cat diffusion-demo` 阅读正文，`open diffusion-demo` 打开文章页。`search diffusion` 可跨目录搜索。目录来自构建时的博客发布索引。
- AI 计算机视觉目前收录 Diffusion 复现，站内提供完整 Python 源码，Notebook 链接固定到原仓库同一提交。
- 原 AI 时间线与交汇图下架，历史网址跳转到对应笔记页。路线资料仍在 data/。
- 85 个知识节点；日期有事件口径和一手来源。路线是代表性选编，不宣称覆盖截至核验日的所有研究。
- 左程云公开课程的 207 条原目录记录，映射成 82 个算法专题，已发布的专题正文进入博客。
- 博客有独立文章模板、自动目录、代码高亮、表格、图片、引用和原生 MathML 公式。
- 深浅主题、全站本地搜索、语言与筛选状态恢复、终端开场、键盘入口、减少动态效果支持。

没有虚构履历、技能熟练度、阅读量、学习进度或个人文章。同一篇中英文内容按一篇笔记统计。`/demo/article/` 与 `/en/demo/article/` 是明确标记的排版演示，不进入搜索、sitemap 或发布统计。

## 文件结构

```text
data/
  profile.json          姓名、介绍、技能、社交、当前关注节点
  nodes.json            稳定知识节点、日期、来源、先修与跨路线归属
  tracks.json           六个领域、四个家族、建议学习顺序与图谱线型
  relations.json        技术关系、贡献说明、证据链接
  confluences.json      共享交汇节点与输入关系
  articles.json         文章元数据
  algorithms.json       算法专题、课号与主笔记正文文件
  lessons.json          原课号、课名、阶段、固定提交链接
  categories.json       算法专题分组
  course-source.json    课件目录文件名与 blob SHA 快照
  source-audit.json     节点日期核验记录
scripts/
  build.py              静态生成
  models.py             类型契约
  i18n.py               中英文公共文案
  validate.py           内容引用、日期、依赖图、产物链接校验
  prepare_courses.py    根据固定快照重建课程映射（非日常构建）
  browser_check.py      浏览器验收与截图
  preview.py            本地静态预览
templates/              Jinja 页面与共享组件
static/                 CSS、JavaScript、SVG
content/                Markdown 正文
tests/                  内容维护集成测试
dist/                   构建产物
.github/workflows/pages.yml
```

## 修改个人资料与双语文案

编辑 `data/profile.json`。`name`、`intro`、`about` 均为 `{"zh-CN": "中文", "en": "English"}`。当前昵称 `river-ya` 来自指定站点账号，可以修改；没有使用 GitHub 返回的真实姓名或邮箱填充个人经历。

`socials` 只保留想公开的链接。`currentTopics` 填已有节点 ID，例如 `["dit", "nerf"]`；为空时主页显示“关注方向”。技能 `status` 可以为 `null`、`learning`、`practiced`、`independent`，对应不显示程度、学习中、已实践、可独立应用。请仅填写真实状态。

公共界面文案集中在 `scripts/i18n.py`，每项为中文、英文二元组，两种语言自动得到相同的键集合。路线和节点的名称、简介在各自数据文件中维护。URL 决定当前语言，根路径始终为中文，记录的英文偏好只显示快捷入口，不强制跳转。

## 新增一篇真实笔记

1. 新建 `content/dit-note.zh.md`，从 `##` 章节开始即可；误用 `#` 时构建器会降一级，页面仍只保留一个主标题。
2. 在 `data/articles.json` 添加元数据：

```json
{
  "slug": "dit-note",
  "translationKey": "dit-note",
  "locale": "zh-CN",
  "title": "我的 DiT 阅读笔记",
  "summary": "填写真实摘要",
  "status": "published",
  "publishedAt": "2026-10-22",
  "file": "content/dit-note.zh.md",
  "nodeIds": ["dit", "vit", "ldm"],
  "tags": ["Diffusion", "Transformer"]
}
```

日期应改为真实发布日期；尚未完成时使用 `draft`。草稿不会生成公开正文页面，不进入搜索或 sitemap。发布后关联节点、右侧 Dock 对应分类、最近更新、搜索自动联动，无需逐个修改组件。`nodeIds` 实现文章与节点多对多关联。

提供真实英文译文时，另加一条 `locale: "en"` 的文章，使用相同 `translationKey`，正文指向独立 Markdown 文件。slug 可以不同，构建器按实际版本生成 `hreflang` 和语言切换链接。没有英文正文时不生成 `/en/blog/.../`，英文界面展示中文原文入口及缺译提示；在原文页点击 EN 仍保留原文位置并说明缺译。

Markdown 支持常规段落、列表、引用、围栏代码、表格和图片。图片放在 `static/` 后以 `/assets/...` 引用。公式使用原生 MathML，示例见 `content/demo.zh.md`；当前没有 LaTeX 转换器，不能直接把 `$...$` 当作已渲染公式。正文是站点作者维护的可信内容，可使用原生 HTML。

## 为算法专题补正文

例如为二分搜索创建 `content/algorithms/binary-search.zh.md`，然后修改 `data/algorithms.json` 中 `binary-search` 条目：

```json
{
  "contentStatus": "published",
  "mainContentFiles": {"zh-CN": "content/algorithms/binary-search.zh.md"}
}
```

这是需要合并进现有条目的字段片段，不是完整条目。原有 `/knowledge/algorithms/binary-search/` 直接显示正文，canonical 不变；英文页说明缺译并链接原文，不复制中文正文冒充译文。可按“适用问题、核心思想、正确性、复杂度、模板代码、典型题、易错点、总结”组织实际写好的章节。

课程原名保持中文，英文页对其标明来源。课程阶段与网站学习定位分开，课程目录数量不表示视频发布数量或本人的学习进度。来源固定为提交 `20a7e5229acb7af3f61c98b63ad3444216425606`，提交日期 2026-10-21，核对日期 2026-10-22。[官方仓库快照](https://github.com/algorithmzuo/algorithm-journey/tree/20a7e5229acb7af3f61c98b63ad3444216425606/ppt)。

`prepare_courses.py` 是课程数据初始化工具，会覆盖生成文件，不用于日常加笔记。更新官方课程目录时先保留人工维护的正文路径、状态与先修配置，再合并新快照；普通构建不抓取远程课程，也不会覆盖这些配置。

## 笔记分类和源码

在 `data/articles.json` 中设置 `status: published`，并填写真实发布日期和标签。AI、算法、Infra 标签匹配对应分类，关联 AI 节点或算法条目的文章也自动归类。计算机视觉节点或 `计算机视觉`、`Computer vision` 标签会将文章列入 AI 的计算机视觉子目录。同一作品的译文共享分类，列表按 `updatedAt` 或 `publishedAt` 倒序排列。

已发布且有 Markdown 正文的算法专题自动成为博客文章，地址为 `/blog/algorithm-<slug>/`。文章字段 `sourceFile` 可指向 `static/source/` 中的 Python 或 C++ 文件，正文可链接同一份高亮源码供下载。

## GitHub Pages 发布

1. 在 `river-ya` 账号下创建或确认 **`river-ya.github.io`** 仓库；如果已有站点，先检查并保留原资料，再合并本项目文件。不要覆盖未知内容。
2. 将源码放入仓库根目录，**务必包含 `.github/workflows/pages.yml`、数据、模板、正文与依赖锁文件**。不要把整个项目套在额外一级目录下。普通网页拖拽上传容易遗漏 `.github`，建议用 Git 或 GitHub Desktop。
3. 打开仓库 **Settings → Pages → Build and deployment → Source → GitHub Actions**。
4. 推送默认分支，或在默认分支手动运行 `Validate and deploy GitHub Pages`。
5. 工作流会安装依赖、检查内容、运行维护测试、生成静态文件、检查链接、安装 Chromium、做浏览器验收，再上传 Pages artifact 并部署。PR 和非默认分支仅验证，不部署。
6. 成功后直接访问 `/`、`/en/`、`/knowledge/nodes/dit/`、`/en/knowledge/ai/families/diffusion/`、`/knowledge/algorithms/binary-search/` 并刷新，检查资源与语言切换。

工作流使用 `contents: read`，部署作业另有 `pages: write`、`id-token: write`，并使用 `github-pages` environment。origin 为 `https://river-ya.github.io`，资源从 `/assets/` 加载，**不使用 `/river-ya.github.io/` 子路径，不添加 CNAME**。`dist/404.html` 是独立静态 404 页。

本次核实的 Actions 版本：checkout v6、setup-python v6、configure-pages v5、upload-pages-artifact v4、deploy-pages v4，均通过官方 Git refs 确认存在。[官方 Pages 工作流说明](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。每次默认分支更新均须通过检查后部署，实际结果以 Actions 运行记录为准。

## 验证与已知限制

静态检查、8 项内容维护测试和浏览器验收由 Actions 自动执行。浏览器检查会在 `evidence/` 下输出 JSON 报告和截图。

浏览器验收可在普通本机运行：

```bash
python -m pip install -r requirements-browser.lock
python -m playwright install chromium
python scripts/browser_check.py
# 只复验开场动画：
python scripts/browser_check.py --intro-only
# 复验 Dock、分类跳转与旧时间线地址：
python scripts/dock_check.py
```

脚本通过 Playwright 把 `dist/` 的原始文件提供给隔离测试域名，检查 375、768、1440px 布局、语言恢复、搜索、主题、路线返回、算法课号、交汇图、开场、减少动态效果、关闭 JavaScript 与存储不可用情形。验收结果写入 `evidence/browser-results.json`，截图保存在 `evidence/`。这里的测试域名不是线上部署地址。

**本次复验：** 运行环境已允许 Chromium 启动，真实浏览器交互检查通过，375、768、1440px 的页面与开屏截图已生成。开屏为全视口纯黑背景，终端文字区域居中，桌面 22px / 手机 18px，采用高对比度提示符、等宽字体、两屏终端流程：先逐字输入 `ssh river_ya@192.0.2.24`，连接成功后展示奶龙字符画，再输入 `clear` 清屏；第二屏输入 `npm run start` 并显示启动回显，终端画面随后碎裂下落，主页模块依次入场；下方模块滚动进入视口时出现（全程约 10.5 秒，可随时跳过，支持减少动态效果）；可通过页脚“重播开场”查看，或播放 `evidence/intro-transition.webm`。尚未进行线上部署验证。文章、个人资料细节、技能程度仍由本人补充。


## 独立博客

主导航、主页按钮与页脚的“博客”入口通往 `/blog/`，英文版为 `/en/blog/`。River’s Log 使用独立页头、页脚和样式表。博客首页、归档、搜索、标签、FAQ 和文章正文采用 Lil’Log 风格的单栏布局。博客主题初次跟随系统，手动选择后单独记忆。

发布文章仍使用 `data/articles.json` 和 Markdown 正文：将文章状态设为 `published`，填写真实 `publishedAt`、`locale`、`translationKey`、`tags` 后重新构建，即会自动进入博客列表、年份归档及标签计数。草稿与演示不进入正式列表；同一文章的中英文版本按当前界面语言优先显示，缺译时链接原文并标明原文语言。文章 slug 不能使用 `archive`、`tags`、`search`、`faq`。

博客专项检查：`python scripts/blog_check.py`。测试中的样例文章只在临时目录构建，不会发布到实际网站。

同一账号可以同时拥有个人站点 `https://river-ya.github.io/`（仓库 `river-ya/river-ya.github.io`）和项目站点 `https://river-ya.github.io/world-scene/`（仓库 `river-ya/world-scene`）。博客是个人站点的 `/blog/` 子页面，不需要单独仓库或域名。本项目资源使用根路径，不配置 CNAME。
