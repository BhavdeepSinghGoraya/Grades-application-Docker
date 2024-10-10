USE grades_db;

-- Create the grades_table
CREATE TABLE IF NOT EXISTS grades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    grade VARCHAR(10),
    student_name VARCHAR(100)
);

-- Grant all privileges to the user
GRANT ALL PRIVILEGES ON grades_db.* TO 'user'@'%';
FLUSH PRIVILEGES;