-- Create stored procedure AddBonus
DELIMITER //

CREATE PROCEDURE AddBonus(IN user_id_param INT, IN project_name_param VARCHAR(255), IN score_param INT)
BEGIN
    DECLARE project_id INT;

    -- Check if project exists, otherwise create it
    SELECT id INTO project_id FROM projects WHERE name = project_name_param;
    
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name_param);
        SET project_id = LAST_INSERT_ID();
    END IF;

    -- Add the new correction
    INSERT INTO corrections (user_id, project_id, score) VALUES (user_id_param, project_id, score_param);
END;
//

DELIMITER ;
