-- 用户与管理员
CREATE TABLE `user` (`sno` VARCHAR(10) PRIMARY KEY, `sname` VARCHAR(20), `credit` INT);
CREATE TABLE `manager` (`id` INT PRIMARY KEY, `password` VARCHAR(20));
INSERT INTO `manager` VALUES (1, '123456');

-- 课程核心表
CREATE TABLE `course` (
  `cno` VARCHAR(20) PRIMARY KEY, `cname` VARCHAR(100), `tname` VARCHAR(40),
  `dname` VARCHAR(20), `cclf` VARCHAR(20), `credit` INT, `csche` VARCHAR(300),
  `exam` VARCHAR(10), `length` INT, `slimit` INT, `campus` VARCHAR(10), `description` VARCHAR(500)
);

-- 标签与关系（图谱用）
CREATE TABLE `clabel` (`cno` VARCHAR(20), `label` VARCHAR(20), PRIMARY KEY(`cno`, `label`));
CREATE TABLE `crelation` (`fcno` VARCHAR(20), `scno` VARCHAR(20), `value` FLOAT, PRIMARY KEY(`fcno`, `scno`));

-- 论坛帖子表
CREATE TABLE `forum_post` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(100), `content` TEXT, `author` VARCHAR(50),
  `tag` VARCHAR(20), `create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP, `view_count` INT DEFAULT 0
);