import pool from '../config/db.js';
import { hashPassword, comparePassword, validatePasswordStrength } from '../utils/password.js';
import { generateToken } from '../middleware/auth.js';
import { success, error } from '../utils/response.js';

// 用户注册
export const register = async (req, res, next) => {
    const { username, email, password } = req.body;
    
    try {
        // 验证必填字段
        if (!username || !email || !password) {
            return res.status(400).json(error('用户名、邮箱和密码不能为空', 400));
        }
        
        // 验证密码强度
        const passwordValidation = validatePasswordStrength(password);
        if (!passwordValidation.valid) {
            return res.status(400).json(error('密码强度不足', 400, passwordValidation.errors));
        }
        
        // 验证邮箱格式
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            return res.status(400).json(error('邮箱格式不正确', 400));
        }
        
        // 检查用户名是否已存在
        const [existingUsers] = await pool.query(
            'SELECT id FROM users WHERE username = ? OR email = ?',
            [username, email]
        );
        
        if (existingUsers.length > 0) {
            return res.status(409).json(error('用户名或邮箱已被注册', 409));
        }
        
        // 加密密码
        const passwordHash = await hashPassword(password);
        
        // 插入新用户
        const [result] = await pool.query(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            [username, email, passwordHash]
        );
        
        const userId = result.insertId;
        
        // 初始化用户技能数据
        await pool.query(
            'INSERT INTO user_skill_data (user_id, skill_data, version) VALUES (?, ?, ?)',
            [userId, JSON.stringify([]), 1]
        );
        
        // 生成 Token
        const token = generateToken(userId, username, email);
        
        return res.status(201).json(success({
            token,
            user: { id: userId, username, email }
        }, '注册成功'));
        
    } catch (err) {
        next(err);
    }
};

// 用户登录
export const login = async (req, res, next) => {
    const { username, password } = req.body;
    
    try {
        // 验证必填字段
        if (!username || !password) {
            return res.status(400).json(error('用户名和密码不能为空', 400));
        }
        
        // 查询用户（支持用户名或邮箱登录）
        const [users] = await pool.query(
            'SELECT id, username, email, password_hash, last_login_at FROM users WHERE username = ? OR email = ? AND is_active = 1',
            [username, username]
        );
        
        if (users.length === 0) {
            return res.status(401).json(error('用户名或密码错误', 401));
        }
        
        const user = users[0];
        
        // 验证密码
        const isPasswordValid = await comparePassword(password, user.password_hash);
        if (!isPasswordValid) {
            return res.status(401).json(error('用户名或密码错误', 401));
        }
        
        // 更新最后登录时间
        await pool.query(
            'UPDATE users SET last_login_at = NOW() WHERE id = ?',
            [user.id]
        );
        
        // 生成 Token
        const token = generateToken(user.id, user.username, user.email);
        
        return res.json(success({
            token,
            user: {
                id: user.id,
                username: user.username,
                email: user.email,
                lastLoginAt: user.last_login_at
            }
        }, '登录成功'));
        
    } catch (err) {
        next(err);
    }
};

// 验证 Token
export const verifyUser = async (req, res) => {
    // req.user 已经由 verifyToken 中间件设置
    return res.json(success({
        user: {
            id: req.user.userId,
            username: req.user.username,
            email: req.user.email
        }
    }, 'Token 有效'));
};
