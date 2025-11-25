import mysql from 'mysql2/promise';
import dotenv from 'dotenv';

dotenv.config();

// 创建数据库连接池
const pool = mysql.createPool({
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 3306,
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || '',
    database: process.env.DB_NAME || 'skill_tracker',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0,
    enableKeepAlive: true,
    keepAliveInitialDelay: 0,
    charset: 'utf8mb4'
});

// 测试数据库连接
pool.getConnection()
    .then(connection => {
        console.log('✅ MySQL 数据库连接成功');
        connection.release();
    })
    .catch(err => {
        console.error('❌ MySQL 数据库连接失败:', err.message);
        process.exit(1);
    });

export default pool;
