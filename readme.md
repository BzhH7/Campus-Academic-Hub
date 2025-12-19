# Campus-Course-Insight (基于Web的课程评价与教务辅助系统)

> 一个专注于解决高校选课信息不对称、提升教务数据透明度的分布式课程管理系统。

## 📖 项目背景
本项目旨在构建一个集课程查询、多维评价、信息共享于一体的教务辅助平台。针对现有教务系统仅提供基础元数据而缺乏评价指标的痛点，本系统引入了用户交互层，利用关系型数据库设计，实现了课程数据的结构化存储与高效检索。

核心目标是利用数据库技术优化课程信息的筛选效率，为学生提供基于数据支撑的选课决策依据。

## 🛠 技术栈
* **后端框架**: Spring Boot (遵循 RESTful API 设计规范)
* **持久层**: MyBatis / MySQL 8.0
* **构建工具**: Maven
* **数据模型**: 采用 E-R 模型设计，包含实体(Entity)与业务模型(Model)的分层映射

## 🚀 快速部署与运行

### 1. 数据库配置
请在 `src/main/resources/application.properties` 中配置本地数据库环境。
**注意：出于安全考虑，请务必修改默认的数据库账号密码。**

```properties
server.port=8088

# 数据库驱动配置
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
# 请根据本地时区和编码调整 URL
spring.datasource.url=jdbc:mysql://localhost:3306/nsm?characterEncoding=utf-8&serverTimezone=Asia/Shanghai
spring.datasource.username=root
# TODO: 请替换为你本地数据库的密码
spring.datasource.password=your_password
```

### 2. 环境依赖

详细依赖清单见根目录 `pom.xml`。确保本地已安装 JDK 1.8+ 及 Maven 环境。

### 3. 启动方式

运行入口类： `.\src\main\java\com\bzh\nwpusurvivalmanual\Application.java`

- 服务默认端口：`localhost:8088`
- 接口测试：项目中 `http test` 目录下包含部分 `.http` 请求文件，可使用 IntelliJ IDEA 自带的 HTTP Client 进行接口调试。

## 📂 架构分层说明

本项目采用经典的分层架构设计，确保高内聚低耦合：

| **目录**       | **说明**                                                     |
| -------------- | ------------------------------------------------------------ |
| **controller** | **控制层**：处理前端 HTTP 请求，负责参数校验与响应封装       |
| **service**    | **业务逻辑层**：封装核心业务逻辑，处理事务控制               |
| **mapper**     | **持久层**：基于 MyBatis 的 DAO 接口，负责 SQL 映射与数据库交互 |
| **entity**     | **PO (Persistent Object)**：与数据库表结构一一对应的实体类   |
| **model**      | **VO/DTO**：用于业务传输或视图展示的聚合模型                 |
| **config**     | **全局配置**：包含 CORS 跨域设置、拦截器配置等               |

## 💡 数据库设计亮点

采用了规范化设计（3NF）减少数据冗余。

针对高频查询字段建立了索引优化。
