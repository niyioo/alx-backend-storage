-- Create stored procedure ComputeAverageWeightedScoreForUsers
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id_var INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN cur;

    -- Loop through all users
    users_loop: LOOP
        -- Fetch the user_id from the cursor
        FETCH cur INTO user_id_var;

        -- Exit the loop if no more users
        IF done THEN
            LEAVE users_loop;
        END IF;

        DECLARE total_weighted_score FLOAT;
        DECLARE total_weight FLOAT;

        -- Calculate total weighted score
        SELECT SUM(weight * score) INTO total_weighted_score
        FROM corrections
        JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id_var;

        -- Calculate total weight
        SELECT SUM(weight) INTO total_weight
        FROM corrections
        JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id_var;

        -- Update average_score in the users table
        UPDATE users
        SET average_score = IFNULL(total_weighted_score / NULLIF(total_weight, 0), 0)
        WHERE id = user_id_var;
    END LOOP;

    -- Close the cursor
    CLOSE cur;
END //

DELIMITER ;
