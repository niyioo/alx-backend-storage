-- Create a function SafeDiv
DELIMITER $$ ;

CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS DECIMAL(10, 10)
DETERMINISTIC
BEGIN
    IF b = 0 THEN
        RETURN 0;
    ELSE
        RETURN a / b;
    END IF;
END;$$

DELIMITER ;
