// 统一响应格式
export const success = (data = null, message = '操作成功') => {
    return {
        success: true,
        message,
        data
    };
};

export const error = (message = '操作失败', code = 500, details = null) => {
    return {
        success: false,
        message,
        code,
        details
    };
};
