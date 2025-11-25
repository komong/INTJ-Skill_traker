import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12;

// 加密密码
export const hashPassword = async (password) => {
    return await bcrypt.hash(password, SALT_ROUNDS);
};

// 验证密码
export const comparePassword = async (password, hash) => {
    return await bcrypt.compare(password, hash);
};

// 验证密码强度
export const validatePasswordStrength = (password) => {
    // 至少8位，包含大小写字母和数字
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    
    const errors = [];
    
    if (password.length < minLength) {
        errors.push(`密码长度至少${minLength}位`);
    }
    if (!hasUpperCase) {
        errors.push('密码必须包含大写字母');
    }
    if (!hasLowerCase) {
        errors.push('密码必须包含小写字母');
    }
    if (!hasNumber) {
        errors.push('密码必须包含数字');
    }
    
    return {
        valid: errors.length === 0,
        errors
    };
};
