import express from 'express';
import { logActivity, getHeatmap, getStats, getRecentActivities, getDayDetails } from '../controllers/activityController.js';
import { verifyToken } from '../middleware/auth.js';

const router = express.Router();

// 所有活动接口都需要认证
router.use(verifyToken);

// 记录活动
router.post('/log', logActivity);

// 获取热力图数据
router.get('/heatmap', getHeatmap);

// 获取统计数据
router.get('/stats', getStats);

// 获取最近活动
router.get('/recent', getRecentActivities);

// 获取某天的详细活动
router.get('/day/:date', getDayDetails);

export default router;
