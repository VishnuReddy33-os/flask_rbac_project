-- Database schema for RBAC Application

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'user'
);

-- Students table
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    course TEXT NOT NULL
);

-- Insert default admin user (password: admin123)
INSERT INTO users (username, password, role) 
VALUES ('admin', 'scrypt:32768:8:1$DZwLZ3wQ8nY5vT1U$abcd1234...', 'admin')
ON CONFLICT(username) DO NOTHING;

-- Insert sample students
INSERT INTO students (name, email, course) VALUES 
('John Doe', 'john@example.com', 'Python'),
('Jane Smith', 'jane@example.com', 'Flask'),
('Bob Johnson', 'bob@example.com', 'JavaScript');
