import pool from '../config/db.js';
import { success, error } from '../utils/response.js';

// 记录用户活动
export const logActivity = async (req, res, next) => {
    const userId = req.user.userId;
    const { date, activityType, skillId, details } = req.body;
    
    try {
        const activityDate = date || new Date().toISOString().split('T')[0];
        
        // 检查今天是否已有记录
        const [existing] = await pool.query(
            'SELECT id, activity_count, details FROM activity_logs WHERE user_id = ? AND activity_date = ?',
            [userId, activityDate]
        );
        
        if (existing.length > 0) {
            // 更新现有记录
            const currentCount = existing[0].activity_count;
            const currentDetails = existing[0].details ? JSON.parse(existing[0].details) : [];
            
            const newDetail = {
                time: new Date().toISOString(),
                type: activityType,
                skillId: skillId || null,
                details: details || null
            };
            
            currentDetails.push(newDetail);
            
            await pool.query(
                'UPDATE activity_logs SET activity_count = ?, details = ? WHERE id = ?',
                [currentCount + 1, JSON.stringify(currentDetails), existing[0].id]
            );
        } else {
            // 创建新记录
            const activityDetails = [{
                time: new Date().toISOString(),
                type: activityType,
                skillId: skillId || null,
                details: details || null
            }];
            
            await pool.query(
                'INSERT INTO activity_logs (user_id, activity_date, activity_count, details) VALUES (?, ?, ?, ?)',
                [userId, activityDate, 1, JSON.stringify(activityDetails)]
            );
        }
        
        return res.json(success({ date: activityDate }, '活动记录成功'));
        
    } catch (err) {
        next(err);
    }
};

// 获取热力图数据
export const getHeatmap = async (req, res, next) => {
    const userId = req.user.userId;
    const year = req.query.year || new Date().getFullYear();
    
    try {
        // 获取指定年份的所有活动记录
        const [activities] = await pool.query(
            `SELECT activity_date, activity_count 
             FROM activity_logs 
             WHERE user_id = ? AND YEAR(activity_date) = ?
             ORDER BY activity_date ASC`,
            [userId, year]
        );
        
        // 生成365天的数据（包括没有活动的日期）
        const startDate = new Date(`${year}-01-01`);
        const endDate = new Date(`${year}-12-31`);
        const heatmapData = [];
        
        // 将数据库结果转为 Map 方便查找
        const activityMap = new Map();
        activities.forEach(activity => {
            activityMap.set(activity.activity_date.toISOString().split('T')[0], activity.activity_count);
        });
        
        // 遍历一年中的每一天
        for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
            const dateStr = d.toISOString().split('T')[0];
            const count = activityMap.get(dateStr) || 0;
            
            // 计算热力等级 (0-4)
            let level = 0;
            if (count > 0) {
                if (count <= 2) level = 1;
                else if (count <= 5) level = 2;
                else if (count <= 10) level = 3;
                else level = 4;
            }
            
            heatmapData.push({
                date: dateStr,
                count: count,
                level: level
            });
        }
        
        return res.json(success({
            year: year,
            data: heatmapData
        }, '获取成功'));
        
    } catch (err) {
        next(err);
    }
};

// 获取统计数据
export const getStats = async (req, res, next) => {
    const userId = req.user.userId;
    
    try {
        // 1. 总活动天数
        const [totalDaysResult] = await pool.query(
            'SELECT COUNT(DISTINCT activity_date) as total_days FROM activity_logs WHERE user_id = ?',
            [userId]
        );
        const totalDays = totalDaysResult[0].total_days || 0;
        
        // 2. 总活动次数
        const [totalActivitiesResult] = await pool.query(
            'SELECT SUM(activity_count) as total_activities FROM activity_logs WHERE user_id = ?',
            [userId]
        );
        const totalActivities = totalActivitiesResult[0].total_activities || 0;
        
        // 3. 当前连续打卡天数
        const [recentActivities] = await pool.query(
            `SELECT activity_date 
             FROM activity_logs 
             WHERE user_id = ? 
             ORDER BY activity_date DESC 
             LIMIT 365`,
            [userId]
        );
        
        let currentStreak = 0;
        if (recentActivities.length > 0) {
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            let checkDate = new Date(today);
            
            for (let i = 0; i < recentActivities.length; i++) {
                const activityDate = new Date(recentActivities[i].activity_date);
                activityDate.setHours(0, 0, 0, 0);
                
                if (activityDate.getTime() === checkDate.getTime()) {
                    currentStreak++;
                    checkDate.setDate(checkDate.getDate() - 1);
                } else {
                    break;
                }
            }
        }
        
        // 4. 最长连续打卡天数
        let longestStreak = 0;
        if (recentActivities.length > 0) {
            let tempStreak = 1;
            
            for (let i = 0; i < recentActivities.length - 1; i++) {
                const currentDate = new Date(recentActivities[i].activity_date);
                const nextDate = new Date(recentActivities[i + 1].activity_date);
                
                const dayDiff = Math.floor((currentDate - nextDate) / (1000 * 60 * 60 * 24));
                
                if (dayDiff === 1) {
                    tempStreak++;
                } else {
                    longestStreak = Math.max(longestStreak, tempStreak);
                    tempStreak = 1;
                }
            }
            longestStreak = Math.max(longestStreak, tempStreak);
        }
        
        // 5. 本周活动次数
        const [weekActivitiesResult] = await pool.query(
            `SELECT SUM(activity_count) as week_activities 
             FROM activity_logs 
             WHERE user_id = ? AND activity_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)`,
            [userId]
        );
        const weekActivities = weekActivitiesResult[0].week_activities || 0;
        
        // 6. 本月活动次数
        const [monthActivitiesResult] = await pool.query(
            `SELECT SUM(activity_count) as month_activities 
             FROM activity_logs 
             WHERE user_id = ? AND YEAR(activity_date) = YEAR(CURDATE()) AND MONTH(activity_date) = MONTH(CURDATE())`,
            [userId]
        );
        const monthActivities = monthActivitiesResult[0].month_activities || 0;
        
        return res.json(success({
            totalDays,
            totalActivities,
            currentStreak,
            longestStreak,
            weekActivities,
            monthActivities
        }, '获取统计数据成功'));
        
    } catch (err) {
        next(err);
    }
};

// 获取最近活动记录
export const getRecentActivities = async (req, res, next) => {
    const userId = req.user.userId;
    const limit = parseInt(req.query.limit) || 7;
    
    try {
        const [activities] = await pool.query(
            `SELECT activity_date, activity_count, details 
             FROM activity_logs 
             WHERE user_id = ? 
             ORDER BY activity_date DESC 
             LIMIT ?`,
            [userId, limit]
        );
        
        const formattedActivities = activities.map(activity => ({
            date: activity.activity_date,
            count: activity.activity_count,
            details: activity.details ? JSON.parse(activity.details) : []
        }));
        
        return res.json(success({ activities: formattedActivities }, '获取成功'));
        
    } catch (err) {
        next(err);
    }
};

// 获取某一天的详细活动
export const getDayDetails = async (req, res, next) => {
    const userId = req.user.userId;
    const { date } = req.params;
    
    try {
        const [activities] = await pool.query(
            'SELECT activity_count, details FROM activity_logs WHERE user_id = ? AND activity_date = ?',
            [userId, date]
        );
        
        if (activities.length === 0) {
            return res.json(success({
                date,
                count: 0,
                details: []
            }, '该日期无活动记录'));
        }
        
        const activity = activities[0];
        
        return res.json(success({
            date,
            count: activity.activity_count,
            details: activity.details ? JSON.parse(activity.details) : []
        }, '获取成功'));
        
    } catch (err) {
        next(err);
    }
};
