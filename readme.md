# Campus-Academic-Hub

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![SpringBoot](https://img.shields.io/badge/SpringBoot-2.7-green.svg) ![Vue](https://img.shields.io/badge/Vue.js-3.0-42b883.svg) ![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)

> 一个集课程评价、知识图谱可视化、校园学术论坛于一体的现代化教务辅助系统。
> 旨在打破选课信息差，构建透明、活跃的校园学术社区。

数据库大作业

## ✨ 核心特性

* **🎓 课程洞察系统**：基于多维标签（如“人工智能”、“Web开发”）的课程检索与评价。
* **🕸️ 知识图谱可视化**：自动分析课程间的先修/后继关系，生成交互式动态图谱（支持自动发现新标签）。
* **💬 校园论坛 (Forum)**：卡片式布局的轻量级社区，支持发帖、分类讨论（交易/求助/闲聊）。
* **🛡️ 评论审核流**：引入管理员审核机制，确保社区言论合规。

## 🛠️ 技术架构

| 模块       | 技术选型                  | 说明                                         |
| :--------- | :------------------------ | :------------------------------------------- |
| **前端**   | Vue 3 + Vite + TypeScript | 采用 Composition API，Element Plus UI 组件库 |
| **后端**   | Spring Boot 2.7           | 遵循 RESTful 规范，MyBatis Plus 持久层框架   |
| **数据库** | MySQL 8.0                 | 关系型数据存储，支持高并发查询               |
| **可视化** | ECharts 5.0               | 渲染高性能的力导向图（Force Graph）          |

## 🚀 从零开始启动指南

### 1. 环境准备
确保本地已安装以下环境：
* **JDK 1.8+**
* **MySQL 8.0+**
* **Node.js 16.0+**
* **Python 3.x** (仅用于生成模拟测试数据，可选)

### 2. 数据库初始化

请登录 MySQL，创建一个名为 `nsm` 的数据库，并执行初始化 SQL。

```sql
CREATE DATABASE nsm CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE nsm;
-- (此处请导入项目根目录下的 nsm_init.sql，或使用下方提供的建表语句)
```

### 3. 后端启动 (Server)

1. 修改配置文件 `src/main/resources/application.properties`：

   Properties

   ```
   spring.datasource.url=jdbc:mysql://localhost:3306/nsm?characterEncoding=utf-8&serverTimezone=Asia/Shanghai
   spring.datasource.username=root
   spring.datasource.password=你的数据库密码  <-- 必须修改这里
   ```

2. 使用 IDEA 打开项目，运行 `NwpuSurvivalManualApplication.java`。

3. 看到 `Started NwpuSurvivalManualApplication` 即启动成功（端口 8088）。

### 4. 前端启动 (Client)

Bash

```
cd web
npm install     # 安装依赖
npm run dev     # 启动开发服务器
```

访问终端显示的地址（通常是 `http://localhost:5173`）。

### 5. ⚡ 数据极速填充 

为了展示最佳效果，建议使用 Python 脚本生成“百万级”模拟数据，而非手动录入。

1. 进入 `crawler` 目录。
2. 安装依赖：`pip install mysqlclient faker`。
3. 依次运行脚本：
   - `python mock_courses.py`：生成 100+ 门逼真的计算机课程。
   - `python insertRelation.py`：构建课程间的先修关系网。
   - `python fix_graph.py`：自动注入“人工智能”、“Web开发”等标签，激活首页知识图谱。

------

## 📂 目录结构说明

```
Campus-Academic-Hub/
├── crawler/                # [数据工程] Python 数据生成与处理脚本
├── http test/              # [测试] API 接口测试文件
├── src/                    # [后端] Spring Boot 核心代码
│   ├── controller/         # 控制层 (Rest API)
│   ├── entity/             # 实体类 (POJO)
│   ├── mapper/             # 持久层 (MyBatis)
│   └── service/            # 业务逻辑层
├── web/                    # [前端] Vue3 + ElementPlus 工程
│   ├── src/
│   │   ├── api/            # Axios 请求封装
│   │   ├── components/     # 公共组件 (Header, Sidebar)
│   │   ├── views/          # 页面视图 (Dashboard, Forum, CourseTable)
│   │   └── store/          # Pinia 状态管理
└── readme.md               # 项目说明文档
```

## 🤝 贡献与反馈

