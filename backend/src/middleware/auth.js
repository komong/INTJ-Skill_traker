import jwt from 'jsonwebtoken';
import dotenv from 'dotenv';
import { error } from '../utils/response.js';

dotenv.config();

const JWT_SECRET = process.env.JWT_SECRET || 'default_secret_key';

// 生成 JWT Token
export const generateToken = (userId, username, email) => {
    return jwt.sign(
        { userId, username, email },
        JWT_SECRET,
        { expiresIn: process.env.JWT_EXPIRES_IN || '24h' }
    );
};

// 验证 Token 中间件
export const verifyToken = (req, res, next) => {
    // 从 Authorization header 获取 token
    const authHeader = req.headers.authorization;
    
    if (!authHeader) {
        return res.status(401).json(error('未提供认证令牌', 401));
    }
    
    // Bearer token 格式
    const token = authHeader.startsWith('Bearer ') 
        ? authHeader.slice(7) 
        : authHeader;
    
    try {
        const decoded = jwt.verify(token, JWT_SECRET);
        req.user = decoded; // 将用户信息添加到请求对象
        next();
    } catch (err) {
        if (err.name === 'TokenExpiredError') {
            return res.status(401).json(error('认证令牌已过期', 401));
        } else if (err.name === 'JsonWebTokenError') {
            return res.status(401).json(error('无效的认证令牌', 401));
        } else {
            return res.status(401).json(error('认证失败', 401));
        }
    }
};
