import express from 'express';
import { getSkills, saveSkills, syncSkills, exportData, importData } from '../controllers/skillController.js';
import { verifyToken } from '../middleware/auth.js';

const router = express.Router();

// 所有技能数据接口都需要认证
router.use(verifyToken);

// 获取用户技能数据
router.get('/', getSkills);

// 保存用户技能数据
router.put('/', saveSkills);

// 数据同步接口
router.post('/sync', syncSkills);

// 导出数据
router.get('/export', exportData);

// 导入数据
router.post('/import', importData);

export default router;
