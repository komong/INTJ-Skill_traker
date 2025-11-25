import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';

// 导入路由
import authRoutes from './src/routes/auth.js';
import skillRoutes from './src/routes/skills.js';
import activityRoutes from './src/routes/activity.js';

// 导入中间件
import { errorHandler, notFoundHandler } from './src/middleware/errorHandler.js';

// 导入数据库连接（会自动测试连接）
import './src/config/db.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// ====================================
// 中间件配置
// ====================================

// 安全头
app.use(helmet());

// CORS 跨域配置（允许所有来源）
app.use(cors({
    origin: true,  // 允许所有来源并返回请求的 origin
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true  // 允许携带凭证
}));

// 解析 JSON 请求体
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// 请求日志
app.use((req, res, next) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
    next();
});

// ====================================
// 路由配置
// ====================================

// 健康检查
app.get('/health', (req, res) => {
    res.json({ 
        success: true, 
        message: 'Skill Tracker API is running',
        timestamp: new Date().toISOString()
    });
});

// API 路由
app.use('/api/auth', authRoutes);
app.use('/api/skills', skillRoutes);
app.use('/api/activity', activityRoutes);

// ====================================
// 错误处理
// ====================================

// 404 处理
app.use(notFoundHandler);

// 统一错误处理
app.use(errorHandler);

// ====================================
// 启动服务器
// ====================================

app.listen(PORT, () => {
    console.log(`
╔═══════════════════════════════════════════╗
║   🚀 Skill Tracker API Server Started    ║
╠═══════════════════════════════════════════╣
║   📡 Port: ${PORT}                         
║   🌍 Environment: ${process.env.NODE_ENV || 'development'}
║   📝 API Docs: http://localhost:${PORT}/health
╚═══════════════════════════════════════════╝
    `);
});

// 优雅关闭
process.on('SIGTERM', () => {
    console.log('📛 收到 SIGTERM 信号，正在优雅关闭服务器...');
    process.exit(0);
});

process.on('SIGINT', () => {
    console.log('\n📛 收到 SIGINT 信号，正在优雅关闭服务器...');
    process.exit(0);
});
