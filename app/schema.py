instructions = [
    'SET FOREIGN_KEY_CHECKS=0;',
    'DROP TABLE IF EXISTS email;',
    'SET FOREIGN_KEY_CHECKS=1;',
    """CREATE TABLE IF NOT EXISTS email (
            id INT PRIMARY KEY AUTO_INCREMENT,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            content TEXT NOT NULL
    );"""
]