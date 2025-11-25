-- ========================================
-- Skill Tracker 数据库初始化脚本
-- ========================================
-- 创建时间: 2025-11-25
-- 说明: 用于初始化用户认证与技能追踪系统的数据库表
-- ========================================

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS skill_tracker 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

USE skill_tracker;

-- ========================================
-- 1. 用户表 (users)
-- ========================================
-- 存储用户基本信息和认证凭据
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户唯一标识',
    username VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名（唯一）',
    email VARCHAR(100) UNIQUE NOT NULL COMMENT '邮箱地址（唯一）',
    password_hash VARCHAR(255) NOT NULL COMMENT 'bcrypt加密后的密码哈希',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
    last_login_at TIMESTAMP NULL COMMENT '最后登录时间',
    is_active TINYINT(1) DEFAULT 1 COMMENT '账户是否激活（1=激活，0=禁用）',
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- ========================================
-- 2. 用户技能数据表 (user_skill_data)
-- ========================================
-- 存储用户的完整技能进度数据（JSON格式）
DROP TABLE IF EXISTS user_skill_data;

CREATE TABLE user_skill_data (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录唯一标识',
    user_id INT NOT NULL COMMENT '关联的用户ID',
    skill_data JSON NOT NULL COMMENT '完整的技能数据（JSON格式，包含所有skills、levels、criteria、logs）',
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后修改时间',
    version INT DEFAULT 1 COMMENT '数据版本号（用于冲突检测）',
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_last_modified (last_modified)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户技能数据表';

-- ========================================
-- 3. 活动日志表 (activity_logs)
-- ========================================
-- 记录用户每日的活跃度（用于生成热力图）
DROP TABLE IF EXISTS activity_logs;

CREATE TABLE activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录唯一标识',
    user_id INT NOT NULL COMMENT '关联的用户ID',
    activity_date DATE NOT NULL COMMENT '活动日期',
    activity_count INT DEFAULT 0 COMMENT '当天的活动次数（勾选标准、添加日志等）',
    details JSON COMMENT '详细活动记录（JSON格式）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_date (user_id, activity_date) COMMENT '一个用户一天只有一条记录',
    INDEX idx_user_date (user_id, activity_date),
    INDEX idx_activity_date (activity_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户活动日志表';

-- ========================================
-- 4. 数据库版本控制表 (db_versions)
-- ========================================
-- 记录数据库schema的版本变更历史
DROP TABLE IF EXISTS db_versions;

CREATE TABLE db_versions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    version VARCHAR(20) NOT NULL COMMENT '版本号（如 1.0.0）',
    description TEXT COMMENT '版本描述',
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '执行时间',
    
    INDEX idx_version (version)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='数据库版本记录表';

-- 插入初始版本记录
INSERT INTO db_versions (version, description) 
VALUES ('1.0.0', '初始数据库结构：用户表、技能数据表、活动日志表');

-- ========================================
-- 5. 创建测试用户（可选，仅用于开发测试）
-- ========================================
-- 密码: Test@1234 (bcrypt hash)
-- 注意: 生产环境需要删除此测试数据

INSERT INTO users (username, email, password_hash, is_active) 
VALUES (
    'testuser',
    'test@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5uyT3Y7gEJhda',
    1
) ON DUPLICATE KEY UPDATE username=username;

-- 为测试用户插入初始技能数据
INSERT INTO user_skill_data (user_id, skill_data, version)
SELECT 
    id,
    '[]' as skill_data,
    1 as version
FROM users 
WHERE username = 'testuser'
ON DUPLICATE KEY UPDATE skill_data=skill_data;

-- ========================================
-- 6. 创建常用查询视图（可选）
-- ========================================

-- 用户统计视图：显示用户的基本统计信息
CREATE OR REPLACE VIEW user_stats AS
SELECT 
    u.id,
    u.username,
    u.email,
    u.created_at,
    u.last_login_at,
    COALESCE(SUM(al.activity_count), 0) as total_activities,
    COALESCE(COUNT(DISTINCT al.activity_date), 0) as active_days,
    usd.version as data_version,
    usd.last_modified as last_skill_update
FROM users u
LEFT JOIN activity_logs al ON u.id = al.user_id
LEFT JOIN user_skill_data usd ON u.id = usd.user_id
WHERE u.is_active = 1
GROUP BY u.id, u.username, u.email, u.created_at, u.last_login_at, usd.version, usd.last_modified;

-- ========================================
-- 7. 数据库权限设置（推荐）
-- ========================================
-- 创建专用数据库用户（生产环境推荐）
-- 注意: 请修改密码为强密码

-- CREATE USER IF NOT EXISTS 'skill_tracker_user'@'localhost' IDENTIFIED BY 'your_strong_password_here';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON skill_tracker.* TO 'skill_tracker_user'@'localhost';
-- FLUSH PRIVILEGES;

-- ========================================
-- 初始化完成提示
-- ========================================
SELECT '✅ 数据库初始化完成！' as status;
SELECT COUNT(*) as total_tables FROM information_schema.tables WHERE table_schema = 'skill_tracker';
