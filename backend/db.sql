-- Tạo bảng để lưu trữ thông tin người dùng
CREATE TABLE users (
    -- ID duy nhất cho mỗi người dùng, tự động tăng
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Tên đăng nhập, không được trùng lặp và không được rỗng
    username VARCHAR(100) NOT NULL UNIQUE,
    
    -- Mật khẩu đã được hash (Bcrypt/Argon2 output thường dài)
    hashed_password VARCHAR(255) NOT NULL,
    
    -- Chuỗi "salt" ngẫu nhiên dùng để hash mật khẩu
    salt VARCHAR(255) NOT NULL,
    
    -- (Tùy chọn) Dấu thời gian khi tài khoản được tạo
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- (Tùy chọn) Thêm chỉ mục (index) cho cột username để tăng tốc độ tìm kiếm
CREATE INDEX idx_username ON users (username);