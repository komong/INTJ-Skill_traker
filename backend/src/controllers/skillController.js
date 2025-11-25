import pool from '../config/db.js';
import { success, error } from '../utils/response.js';

// 获取用户技能数据
export const getSkills = async (req, res, next) => {
    const userId = req.user.userId;
    
    try {
        const [rows] = await pool.query(
            'SELECT skill_data, version, last_modified FROM user_skill_data WHERE user_id = ?',
            [userId]
        );
        
        if (rows.length === 0) {
            // 如果没有数据，创建初始数据
            await pool.query(
                'INSERT INTO user_skill_data (user_id, skill_data, version) VALUES (?, ?, ?)',
                [userId, '[]', 1]
            );
            
            return res.json(success({
                skills: [],
                version: 1,
                lastModified: new Date()
            }, '获取成功'));
        }
        
        const skillData = rows[0];
        let parsedSkills = [];
        
        try {
            parsedSkills = JSON.parse(skillData.skill_data);
        } catch (parseError) {
            // 如果解析失败，返回空数组
            parsedSkills = [];
        }
        
        return res.json(success({
            skills: parsedSkills,
            version: skillData.version,
            lastModified: skillData.last_modified
        }, '获取成功'));
        
    } catch (err) {
        next(err);
    }
};

// 保存用户技能数据
export const saveSkills = async (req, res, next) => {
    const userId = req.user.userId;
    const { skills, version } = req.body;
    
    try {
        // 验证必填字段
        if (!skills) {
            return res.status(400).json(error('技能数据不能为空', 400));
        }
        
        // 验证数据格式
        if (!Array.isArray(skills)) {
            return res.status(400).json(error('技能数据格式错误', 400));
        }
        
        // 获取当前版本号
        const [currentData] = await pool.query(
            'SELECT version FROM user_skill_data WHERE user_id = ?',
            [userId]
        );
        
        let newVersion = 1;
        const skillDataJson = typeof skills === 'string' ? skills : JSON.stringify(skills);
        
        if (currentData.length > 0) {
            const currentVersion = currentData[0].version;
            
            // 版本冲突检测
            if (version && version < currentVersion) {
                return res.status(409).json(error('数据版本冲突，请先同步最新数据', 409, {
                    currentVersion,
                    yourVersion: version
                }));
            }
            
            newVersion = currentVersion + 1;
            
            // 更新数据
            await pool.query(
                'UPDATE user_skill_data SET skill_data = ?, version = ?, last_modified = NOW() WHERE user_id = ?',
                [skillDataJson, newVersion, userId]
            );
        } else {
            // 插入新数据
            await pool.query(
                'INSERT INTO user_skill_data (user_id, skill_data, version) VALUES (?, ?, ?)',
                [userId, skillDataJson, newVersion]
            );
        }
        
        return res.json(success({
            version: newVersion,
            message: '保存成功'
        }, '保存成功'));
        
    } catch (err) {
        next(err);
    }
};

// 数据同步接口（智能合并）
export const syncSkills = async (req, res, next) => {
    const userId = req.user.userId;
    const { localData, localVersion } = req.body;
    
    try {
        // 获取服务器数据
        const [serverData] = await pool.query(
            'SELECT skill_data, version, last_modified FROM user_skill_data WHERE user_id = ?',
            [userId]
        );
        
        // 如果服务器没有数据，直接保存本地数据
        if (serverData.length === 0) {
            const skillDataJson = typeof localData === 'string' ? localData : JSON.stringify(localData);
            await pool.query(
                'INSERT INTO user_skill_data (user_id, skill_data, version) VALUES (?, ?, ?)',
                [userId, skillDataJson, 1]
            );
            
            return res.json(success({
                action: 'uploaded',
                serverData: localData,
                serverVersion: 1
            }, '数据已上传到云端'));
        }
        
        const currentServerData = serverData[0];
        const serverVersion = currentServerData.version;
        const serverSkills = JSON.parse(currentServerData.skill_data);
        
        // 如果本地版本等于服务器版本，说明数据已同步
        if (localVersion === serverVersion) {
            return res.json(success({
                action: 'synced',
                serverData: serverSkills,
                serverVersion
            }, '数据已是最新'));
        }
        
        // 如果本地版本小于服务器版本，需要下载服务器数据
        if (localVersion < serverVersion) {
            return res.json(success({
                action: 'download',
                serverData: serverSkills,
                serverVersion,
                message: '服务器数据更新，请下载最新版本'
            }, '需要更新本地数据'));
        }
        
        // 如果本地版本大于服务器版本（理论上不应该发生，但作为容错处理）
        // 使用本地数据覆盖服务器数据
        const newVersion = serverVersion + 1;
        const skillDataJson = typeof localData === 'string' ? localData : JSON.stringify(localData);
        await pool.query(
            'UPDATE user_skill_data SET skill_data = ?, version = ?, last_modified = NOW() WHERE user_id = ?',
            [skillDataJson, newVersion, userId]
        );
        
        return res.json(success({
            action: 'uploaded',
            serverData: localData,
            serverVersion: newVersion
        }, '本地数据已上传'));
        
    } catch (err) {
        next(err);
    }
};

// 导出数据（JSON格式）
export const exportData = async (req, res, next) => {
    const userId = req.user.userId;
    
    try {
        const [skillData] = await pool.query(
            'SELECT skill_data, version FROM user_skill_data WHERE user_id = ?',
            [userId]
        );
        
        if (skillData.length === 0) {
            return res.status(404).json(error('没有找到数据', 404));
        }
        
        const exportData = {
            version: skillData[0].version,
            exportDate: new Date().toISOString(),
            skills: JSON.parse(skillData[0].skill_data)
        };
        
        res.setHeader('Content-Type', 'application/json');
        res.setHeader('Content-Disposition', `attachment; filename=skill-tracker-backup-${new Date().toISOString().split('T')[0]}.json`);
        
        return res.json(exportData);
        
    } catch (err) {
        next(err);
    }
};

// 导入数据
export const importData = async (req, res, next) => {
    const userId = req.user.userId;
    const { skills, version } = req.body;
    
    try {
        // 验证数据格式
        if (!skills || !Array.isArray(skills)) {
            return res.status(400).json(error('导入数据格式错误', 400));
        }
        
        // 直接覆盖现有数据
        const newVersion = (version || 0) + 1;
        const skillDataJson = typeof skills === 'string' ? skills : JSON.stringify(skills);
        
        const [existingData] = await pool.query(
            'SELECT id FROM user_skill_data WHERE user_id = ?',
            [userId]
        );
        
        if (existingData.length > 0) {
            await pool.query(
                'UPDATE user_skill_data SET skill_data = ?, version = ?, last_modified = NOW() WHERE user_id = ?',
                [skillDataJson, newVersion, userId]
            );
        } else {
            await pool.query(
                'INSERT INTO user_skill_data (user_id, skill_data, version) VALUES (?, ?, ?)',
                [userId, skillDataJson, newVersion]
            );
        }
        
        return res.json(success({
            version: newVersion,
            importedCount: skills.length
        }, '导入成功'));
        
    } catch (err) {
        next(err);
    }
};
