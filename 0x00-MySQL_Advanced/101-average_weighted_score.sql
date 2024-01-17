-- Create stored procedure ComputeAverageWeightedScoreForUsers
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id_var INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight FLOAT;

    -- Create a temporary table to store the results
    CREATE TEMPORARY TABLE IF NOT EXISTS temp_weighted_scores (
        user_id INT,
        weighted_score FLOAT
    );

    -- Create a cursor for the user IDs
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

        -- Calculate total weighted score and insert into temporary table
        INSERT INTO temp_weighted_scores (user_id, weighted_score)
        SELECT user_id_var, IFNULL(SUM(weight * score) / NULLIF(SUM(weight), 0), 0)
        FROM corrections
        JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id_var;
    END LOOP;

    -- Close the cursor
    CLOSE cur;

    -- Update the users table with the computed average scores
    UPDATE users
    SET average_score = (SELECT AVG(weighted_score) FROM temp_weighted_scores WHERE user_id = users.id);

    -- Drop the temporary table
    DROP TEMPORARY TABLE IF EXISTS temp_weighted_scores;
END //

DELIMITER ;
