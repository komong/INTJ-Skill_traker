import express from 'express';
import { register, login, verifyUser } from '../controllers/authController.js';
import { verifyToken } from '../middleware/auth.js';

const router = express.Router();

// 用户注册
router.post('/register', register);

// 用户登录
router.post('/login', login);

// 验证 Token（需要认证）
router.get('/verify', verifyToken, verifyUser);

export default router;
