USE sql_project;
CREATE TABLE IF NOT EXISTS customers (
     id INT NOT NULL AUTO_INCREMENT,
     name VARCHAR(250) NOT NULL UNIQUE,
     address VARCHAR(250) NOT NULL,
     number INT(11) NOT NULL UNIQUE,
     timein DATETIME,
     timeout DATETIME,
     status VARCHAR(11),
     PRIMARY KEY (id)
);