-- 1. Drop & recreate the database
DROP DATABASE IF EXISTS product_inventory;
CREATE DATABASE product_inventory;
USE product_inventory;

-- 2. Create the table
CREATE TABLE tshirt_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100),
    brand VARCHAR(50),
    category VARCHAR(50),
    price DECIMAL(10,2),
    quantity_in_stock INT,
    quantity_sold INT,
    discount_percentage DECIMAL(5,2),
    location VARCHAR(100)
);

-- 3. Create the procedure to insert 1000 random rows
DELIMITER $$

CREATE PROCEDURE generate_large_tshirt_data()
BEGIN
    DECLARE i INT DEFAULT 0;

    WHILE i < 1000 DO
        INSERT INTO tshirt_info (
            product_name, brand, category, price,
            quantity_in_stock, quantity_sold, discount_percentage, location
        )
        VALUES (
            CONCAT('T-Shirt ', FLOOR(1 + RAND() * 9999)),
            ELT(FLOOR(1 + RAND() * 5), 'Nike', 'Adidas', 'Puma', 'Reebok', 'Under Armour'),
            ELT(FLOOR(1 + RAND() * 4), 'Sportswear', 'Casual', 'Formal', 'Outdoor'),
            ROUND(199 + (RAND() * 801), 2),  -- price between 199–1000
            FLOOR(1 + RAND() * 500),         -- stock between 1–500
            FLOOR(0 + RAND() * 300),         -- sold between 0–300
            ROUND(RAND() * 50, 2),           -- discount between 0–50%
            ELT(FLOOR(1 + RAND() * 6), 'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Pune')
        );
        SET i = i + 1;
    END WHILE;
END$$

DELIMITER ;

-- 4. Call the procedure
CALL generate_large_tshirt_data();

-- 5. Optional: Drop the procedure after use
DROP PROCEDURE generate_large_tshirt_data;


SELECT * FROM tshirt_info;
