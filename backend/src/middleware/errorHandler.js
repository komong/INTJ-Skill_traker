import { error } from '../utils/response.js';

// 统一错误处理中间件
export const errorHandler = (err, req, res, next) => {
    console.error('❌ 错误:', err);
    
    // 数据库错误
    if (err.code === 'ER_DUP_ENTRY') {
        return res.status(409).json(error('数据已存在', 409, err.sqlMessage));
    }
    
    // 验证错误
    if (err.name === 'ValidationError') {
        return res.status(400).json(error('数据验证失败', 400, err.message));
    }
    
    // 默认错误
    const statusCode = err.statusCode || 500;
    const message = err.message || '服务器内部错误';
    
    res.status(statusCode).json(error(message, statusCode));
};

// 404 处理
export const notFoundHandler = (req, res) => {
    res.status(404).json(error('请求的资源不存在', 404));
};
