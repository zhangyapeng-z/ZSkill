# 原型组件库（25+ 组件）

本文件为「需求PRD到产品原型」Skill 的组件库详细说明。模块三生成原型时按需读取。
组件按 CSS 分组（G1基础/G2演示级/G3-PC端）组织，对应 `assets/prototype-template.html` 中的 CSS/JS 分组标注。

---

## 按需读取索引

| 保真度级别 | 目标端 | 需读取的分组 | 组件数量 |
|-----------|--------|------------|---------|
| 评审级中保真 | 移动端 | G1 基础组件 | 7个 |
| 演示级高保真 | 移动端 | G1 + G2 | 25个 |
| 评审级中保真 | PC端 | G1 + G3 | 13个 |
| 演示级高保真 | PC端 | G1 + G2 + G3 | 31个 |
| 演示级高保真 | 多端 | G1 + G2 + G3 | 31个 |

> HTML 模板中 CSS/JS 已用 `<!-- CSS-GROUP: basic/demo/pc -->` 注释标注分组边界，读取时定位标注截取即可。

---

## 页面类型→组件矩阵（按需选组件，避免逐个判断）

| 页面类型 | 必选组件 | 推荐组件 | 可选组件 |
|---------|---------|---------|---------|
| **列表页** | 卡片、搜索、导航 | 骨架屏、空状态、筛选 | 轮播、标签、分页 |
| **表单页** | 表单、按钮、导航 | 步进器、弹窗、验证 | 开关、日期选择、头像 |
| **详情页** | 卡片、导航、标签 | 预览、分享、步进器 | 评论、评分、Toast |
| **首页/Dashboard** | 导航、TabBar、卡片 | 轮播、搜索、徽标 | 筛选、抽屉 |
| **个人中心** | 导航、TabBar、头像 | 列表、标签、按钮 | 弹窗、开关 |
| **管理后台** | 侧边菜单、数据表格、面包屑 | 页面头部、看板卡片 | 筛选、弹窗 |
| **空状态页** | 空状态、按钮 | 导航 | — |
| **错误页** | 错误状态、按钮 | 导航 | — |

> 使用方式：根据PRD §6 Page Map确定页面类型 → 查本表确定组件 → 从G1/G2/G3分组中读取对应组件CSS/JS。

---

## G1 基础组件（7个 · 所有场景必读）

### 1. 导航栏 `.nav-bar` 【演示级/评审级】
```html
<div class="nav-bar">
  <span class="nav-back" onclick="showPage('home')">←</span>
  <span class="nav-title">页面标题</span>
  <span class="nav-action" onclick="openModal('modal1')">⋯</span>
</div>
```
CSS：高48px，白底，底部1px边框，sticky定位。

### 2. TabBar `.tabbar` 【演示级/评审级】
```html
<div class="tabbar">
  <div class="tab active" onclick="showPage('home')"><span class="tab-icon">🏠</span>首页</div>
  <div class="tab" onclick="showPage('list')"><span class="tab-icon">📋</span>列表</div>
  <div class="tab" onclick="showPage('mine')"><span class="tab-icon">👤</span>我的</div>
</div>
```
CSS：固定底部，375px宽，高56px，白底，顶部1px边框。

### 3. 按钮 `.btn` 【演示级/评审级】
```html
<button class="btn btn-primary" onclick="action()">主要按钮</button>
<button class="btn btn-secondary">次要按钮</button>
<button class="btn btn-danger">危险按钮</button>
<button class="btn btn-disabled" disabled>禁用按钮</button>
<button class="btn btn-block">通栏按钮</button>
```
CSS：圆角8px，padding 10px 20px，过渡动画0.2s。

### 4. 表单 `.form-group` 【演示级/评审级】
```html
<div class="form-group">
  <label>字段名</label>
  <input type="text" placeholder="请输入" />
</div>
<div class="form-group">
  <label>选择项</label>
  <select><option>选项A</option><option>选项B</option></select>
</div>
```
CSS：白底，底部1px分隔线，输入框圆角6px，聚焦时边框变蓝。

### 5. 列表/卡片 `.card` 【演示级/评审级】
```html
<div class="card" onclick="goDetail()">
  <div class="card-title">标题</div>
  <div class="card-desc">描述文字</div>
  <div class="card-meta">附加信息</div>
</div>
```
CSS：白底，圆角10px，轻微阴影，hover阴影加深。

### 6. 弹窗 `.modal-mask` 【演示级/评审级】
```html
<div class="modal-mask" id="modal1" onclick="closeModal('modal1')">
  <div class="modal" onclick="event.stopPropagation()">
    <div class="modal-title">标题</div>
    <div class="modal-body">内容</div>
    <div class="modal-actions">
      <button class="btn-cancel" onclick="closeModal('modal1')">取消</button>
      <button class="btn-confirm" onclick="confirm()">确认</button>
    </div>
  </div>
</div>
```
CSS：全屏遮罩rgba(0,0,0,0.4)，弹窗宽300px，圆角12px。

### 7. 状态标签 `.tag` 【演示级/评审级】
```html
<span class="tag tag-success">成功</span>
<span class="tag tag-warning">待处理</span>
<span class="tag tag-danger">失败</span>
<span class="tag tag-info">进行中</span>
```
CSS：内联块，圆角4px，padding 2px 8px，不同状态不同背景色。

---

## G2 演示级组件（18个 · 演示级高保真时读取）

### 8. 轮播图 `.carousel` 【演示级】
```html
<div class="carousel" id="carousel1">
  <div class="carousel-track">
    <div class="carousel-slide" style="background:#DBEAFE;">轮播图1</div>
    <div class="carousel-slide" style="background:#D1FAE5;">轮播图2</div>
    <div class="carousel-slide" style="background:#FEF3C7;">轮播图3</div>
  </div>
  <div class="carousel-dots">
    <span class="dot active" onclick="carouselGoTo(0)"></span>
    <span class="dot" onclick="carouselGoTo(1)"></span>
    <span class="dot" onclick="carouselGoTo(2)"></span>
  </div>
</div>
```
**CSS要点**：overflow hidden，slide横向排列，dots绝对定位底部居中。
**交互JS**：自动轮播3秒切换，点击dots跳转，`carouselGoTo(index)` 函数控制。
**使用示例**：首页Banner运营位、商品图片轮播。

### 9. 步进器 `.stepper` 【演示级/评审级】
```html
<div class="stepper">
  <button class="stepper-btn" onclick="stepperChange(this,-1)">−</button>
  <input class="stepper-input" type="text" value="1" readonly />
  <button class="stepper-btn" onclick="stepperChange(this,1)">+</button>
</div>
```
**CSS要点**：横向排列，按钮36x36px圆角6px，输入框居中宽40px。
**交互JS**：`stepperChange(el, delta)` 加减数值，最小1最大99，超出范围按钮置灰。
**使用示例**：兑换数量选择、购物车数量。

### 10. 搜索栏 `.search-bar` 【演示级/评审级】
```html
<div class="search-bar">
  <span class="search-icon">🔍</span>
  <input class="search-input" type="text" placeholder="搜索商品" oninput="onSearch(this.value)" />
  <button class="search-btn" onclick="doSearch()">搜索</button>
</div>
```
**CSS要点**：圆角20px，灰底#F3F4F6，聚焦时边框变蓝。
**交互JS**：`onSearch(value)` 输入时实时过滤列表，`doSearch()` 提交搜索。
**使用示例**：商品搜索、列表筛选。

### 11. 筛选器 `.filter-bar` 【演示级/评审级】
```html
<div class="filter-bar">
  <div class="filter-item active" onclick="filterList(this,'all')">全部</div>
  <div class="filter-item" onclick="filterList(this,'coupon')">优惠券</div>
  <div class="filter-item" onclick="filterList(this,'physical')">实物</div>
  <div class="filter-item" onclick="filterList(this,'rights')">权益</div>
  <div class="filter-sort" onclick="toggleSort()">排序 ⬇</div>
</div>
```
**CSS要点**：横向排列，active项蓝色+底部2px蓝线，可横向滚动。
**交互JS**：`filterList(el, type)` 切换筛选条件并过滤列表项。
**使用示例**：商品列表筛选、订单筛选。

### 12. 空状态 `.state-empty` 【演示级/评审级】
```html
<div class="state-empty">
  <div class="state-empty-icon">📦</div>
  <div class="state-empty-text">暂无商品</div>
  <button class="btn btn-secondary" onclick="goHome()">去首页看看</button>
</div>
```
**CSS要点**：居中布局，图标48px灰色，文案14px灰色，按钮间距16px。
**使用示例**：空列表、无搜索结果、无订单。

### 13. 加载态 `.state-loading` 【演示级/评审级】
```html
<div class="state-loading">
  <div class="spinner"></div>
  <div class="state-loading-text">加载中...</div>
</div>
```
**CSS要点**：spinner用CSS动画旋转，居中布局。
**交互JS**：数据请求时显示，完成后隐藏。
**使用示例**：页面加载、列表加载更多。

### 14. 骨架屏 `.skeleton` 【演示级】
```html
<div class="skeleton">
  <div class="skeleton-line" style="width:60%"></div>
  <div class="skeleton-line" style="width:90%"></div>
  <div class="skeleton-line" style="width:75%"></div>
</div>
<div class="skeleton-card">
  <div class="skeleton-block" style="width:80px;height:80px"></div>
  <div class="skeleton-lines">
    <div class="skeleton-line" style="width:70%"></div>
    <div class="skeleton-line" style="width:50%"></div>
  </div>
</div>
```
**CSS要点**：灰块#E5E7EB背景，渐变扫光动画（从左到右）。
**交互JS**：页面加载时显示骨架屏，数据就绪后切换为真实内容。
**使用示例**：列表加载、详情页加载。

### 15. ActionSheet `.action-sheet` 【演示级/评审级】
```html
<div class="action-sheet-mask" id="sheet1" onclick="closeActionSheet('sheet1')">
  <div class="action-sheet" onclick="event.stopPropagation()">
    <div class="action-sheet-item" onclick="shareTo('wechat')">分享到微信</div>
    <div class="action-sheet-item" onclick="shareTo('moment')">分享到朋友圈</div>
    <div class="action-sheet-item" onclick="copyLink()">复制链接</div>
    <div class="action-sheet-cancel" onclick="closeActionSheet('sheet1')">取消</div>
  </div>
</div>
```
**CSS要点**：底部弹出，从下滑入动画，每项高48px，取消项有间距。
**交互JS**：`openActionSheet(id)` / `closeActionSheet(id)` 控制开关。
**使用示例**：分享、更多操作、筛选弹层。

### 16. 步进条 `.steps` 【演示级/评审级】
```html
<div class="steps">
  <div class="step active">
    <div class="step-num">1</div>
    <div class="step-label">选择商品</div>
  </div>
  <div class="step-line active"></div>
  <div class="step active">
    <div class="step-num">2</div>
    <div class="step-label">确认兑换</div>
  </div>
  <div class="step-line"></div>
  <div class="step">
    <div class="step-num">3</div>
    <div class="step-label">兑换成功</div>
  </div>
</div>
```
**CSS要点**：横向排列，已完成步骤蓝色，未完成灰色，连线横线。
**交互JS**：通过JS动态更新 `active` class 控制进度。
**使用示例**：兑换流程、注册引导、认证流程。

### 17. 顶部标签页 `.tabs-top` 【演示级/评审级】
```html
<div class="tabs-top">
  <div class="tabs-top-item active" onclick="switchTopTab(this,'tab1')">详情</div>
  <div class="tabs-top-item" onclick="switchTopTab(this,'tab2')">评价</div>
  <div class="tabs-top-item" onclick="switchTopTab(this,'tab3')">推荐</div>
</div>
<div class="tabs-top-content">
  <div class="tab-pane active" id="tab1">详情内容</div>
  <div class="tab-pane" id="tab2">评价内容</div>
  <div class="tab-pane" id="tab3">推荐内容</div>
</div>
```
**CSS要点**：横向排列sticky定位，active项蓝色+底部蓝线，内容区切换显示。
**交互JS**：`switchTopTab(el, paneId)` 切换标签和内容。
**使用示例**：详情页Tab切换、分类切换。

### 18. Toast提示 `.toast` 【演示级/评审级】
```html
<!-- 标准化Toast样式 -->
<div id="toast" class="toast">提示文字</div>
```
**CSS要点**：固定居中，深色半透明背景，圆角8px，2秒后淡出。
**交互JS**：`toast(msg)` 函数显示消息并2秒后自动隐藏。
**使用示例**：提交成功、收藏成功、操作反馈。

### 19. 开关 `.switch` 【演示级/评审级】
```html
<div class="switch-row">
  <span class="switch-label">消息通知</span>
  <div class="switch active" onclick="toggleSwitch(this)">
    <div class="switch-knob"></div>
  </div>
</div>
```
**CSS要点**：宽44px高24px圆角12px，active时绿色背景，knob滑动。
**交互JS**：`toggleSwitch(el)` 切换 active class。
**使用示例**：设置页、偏好设置。

### 20. 徽标 `.badge` 【演示级/评审级】
```html
<span class="badge badge-dot"></span>
<span class="badge badge-num">3</span>
<span class="badge badge-num">99+</span>
```
**CSS要点**：红色#EF4444背景，圆点8px，数字min-width 16px高16px圆角8px。
**使用示例**：消息未读、购物车数量、Tab红点。

### 21. 滑动操作 `.swipe-cell` 【演示级】
```html
<div class="swipe-cell">
  <div class="swipe-content" ontouchstart="swipeStart(event)" ontouchmove="swipeMove(event)" ontouchend="swipeEnd(event)">
    列表项内容
  </div>
  <div class="swipe-actions">
    <button class="swipe-action swipe-collect">收藏</button>
    <button class="swipe-action swipe-delete">删除</button>
  </div>
</div>
```
**CSS要点**：内容区可滑动露出操作按钮，操作按钮绝对定位右侧。
**交互JS**：`swipeStart/swipeMove/swipeEnd` 控制滑动距离，超过阈值露出操作区。
**使用示例**：订单删除、列表项操作。

### 22. 头像组 `.avatar-group` 【演示级/评审级】
```html
<div class="avatar-group">
  <div class="avatar" style="background:#DBEAFE;color:#1E40AF;">张</div>
  <div class="avatar" style="background:#D1FAE5;color:#065F46;">李</div>
  <div class="avatar" style="background:#FEF3C7;color:#92400E;">王</div>
  <div class="avatar avatar-more">+5</div>
</div>
```
**CSS要点**：头像32px圆形，重叠margin-left -8px，最后显示"+N"。
**使用示例**：用户信息、评论者头像、参与者列表。

### 23. 图片预览 `.image-preview` 【演示级】
```html
<div class="image-preview-mask" id="preview1" onclick="closePreview('preview1')">
  <img src="商品大图URL" class="image-preview-img" />
</div>
```
**CSS要点**：全屏黑色遮罩，图片居中max-width 90%，支持双击放大。
**交互JS**：`openPreview(url)` / `closePreview(id)` 控制开关。
**使用示例**：商品图片、凭证图片。

### 24. 加载更多 `.load-more` 【演示级/评审级】
```html
<div class="load-more" onclick="loadMore()">
  <span class="load-more-text">加载更多</span>
  <span class="load-more-icon">↓</span>
</div>
```
**CSS要点**：居中文案，灰色文字，点击后变为加载动画。
**交互JS**：`loadMore()` 追加列表数据，加载完显示"没有更多了"。
**使用示例**：长列表、订单历史。

### 25. 抽屉 `.drawer` 【演示级/评审级】
```html
<div class="drawer-mask" id="drawer1" onclick="closeDrawer('drawer1')">
  <div class="drawer" onclick="event.stopPropagation()">
    <div class="drawer-header">
      <span class="drawer-title">高级筛选</span>
      <span class="drawer-close" onclick="closeDrawer('drawer1')">✕</span>
    </div>
    <div class="drawer-body">
      <!-- 筛选内容 -->
    </div>
    <div class="drawer-footer">
      <button class="btn btn-secondary" onclick="resetFilter()">重置</button>
      <button class="btn btn-primary" onclick="applyFilter()">确定</button>
    </div>
  </div>
</div>
```
**CSS要点**：右侧滑入面板，宽300px或80%宽，从右滑入动画。
**交互JS**：`openDrawer(id)` / `closeDrawer(id)` 控制开关。
**使用示例**：高级筛选、侧边设置。

---

## G3 PC端组件（6个 · 目标端含PC时读取）

### 26. 侧边菜单 `.sidebar-menu` 【演示级/评审级】
```html
<div class="sidebar-menu">
  <div class="sidebar-logo">后台管理</div>
  <div class="sidebar-item active">
    <span class="sidebar-icon">📊</span>数据看板
  </div>
  <div class="sidebar-item">
    <span class="sidebar-icon">📦</span>商品管理
  </div>
  <div class="sidebar-item">
    <span class="sidebar-icon">📋</span>订单管理
  </div>
</div>
```
**CSS要点**：固定左侧200px，深色背景#1F2937，白色文字，active项蓝色高亮。
**使用示例**：后台管理左侧导航。

### 27. 数据表格 `.data-table` 【演示级/评审级】
```html
<table class="data-table">
  <thead>
    <tr><th>订单号</th><th>商品</th><th>积分</th><th>状态</th><th>操作</th></tr>
  </thead>
  <tbody>
    <tr><td>ORD001</td><td>优惠券A</td><td>500</td><td><span class="tag tag-success">已完成</span></td><td><a>查看</a></td></tr>
    <tr><td>ORD002</td><td>实物B</td><td>1200</td><td><span class="tag tag-warning">待发货</span></td><td><a>查看</a></td></tr>
  </tbody>
</table>
```
**CSS要点**：白底，表头灰底#F9FAFB，行hover#F3F4F6，1px边框。
**使用示例**：后台列表数据展示。

### 28. 面包屑 `.breadcrumb` 【演示级/评审级】
```html
<div class="breadcrumb">
  <span class="breadcrumb-item">首页</span>
  <span class="breadcrumb-sep">/</span>
  <span class="breadcrumb-item">商品管理</span>
  <span class="breadcrumb-sep">/</span>
  <span class="breadcrumb-current">商品列表</span>
</div>
```
**CSS要点**：横向排列，分隔符灰色，当前项深色加粗。
**使用示例**：PC端层级导航。

### 29. 页面头部 `.page-header` 【演示级/评审级】
```html
<div class="page-header">
  <div class="page-header-title">商品管理</div>
  <div class="page-header-actions">
    <button class="btn btn-secondary">导出</button>
    <button class="btn btn-primary">新增商品</button>
  </div>
</div>
```
**CSS要点**：flex布局，标题左对齐18px加粗，操作按钮右对齐。
**使用示例**：PC端页面标题+操作区。

### 30. 看板卡片 `.dashboard-card` 【演示级/评审级】
```html
<div class="dashboard-card">
  <div class="dashboard-card-icon">📊</div>
  <div class="dashboard-card-info">
    <div class="dashboard-card-label">总兑换数</div>
    <div class="dashboard-card-value">1,286</div>
    <div class="dashboard-card-trend up">↑ 12.5% vs 上周</div>
  </div>
</div>
```
**CSS要点**：白底圆角12px阴影，flex布局，数值24px加粗，趋势绿色↑红色↓。
**使用示例**：数据看板指标卡片。

### 31. 多列表单 `.form-grid` 【演示级/评审级】
```html
<div class="form-grid">
  <div class="form-grid-item">
    <label>商品名称</label>
    <input type="text" placeholder="请输入" />
  </div>
  <div class="form-grid-item">
    <label>积分价格</label>
    <input type="number" placeholder="请输入" />
  </div>
  <div class="form-grid-item">
    <label>商品类型</label>
    <select><option>优惠券</option><option>实物</option></select>
  </div>
  <div class="form-grid-item">
    <label>库存数量</label>
    <input type="number" placeholder="请输入" />
  </div>
</div>
```
**CSS要点**：CSS Grid 2列布局，间距16px，表单项含label+input。
**使用示例**：PC端多列表单布局。
