-- Create stored procedure ComputeAverageWeightedScoreForUsers
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Create a temporary table to store the results
    CREATE TEMPORARY TABLE IF NOT EXISTS temp_weighted_scores (
        user_id INT,
        weighted_score FLOAT
    );

    -- Calculate total weighted score and insert into temporary table
    INSERT INTO temp_weighted_scores (user_id, weighted_score)
    SELECT users.id, IFNULL(SUM(projects.weight * corrections.score) / NULLIF(SUM(projects.weight), 0), 0)
    FROM users
    LEFT JOIN corrections ON users.id = corrections.user_id
    LEFT JOIN projects ON corrections.project_id = projects.id
    GROUP BY users.id;

    -- Update the users table with the computed average scores
    UPDATE users
    SET average_score = (SELECT AVG(weighted_score) FROM temp_weighted_scores WHERE user_id = users.id);

    -- Drop the temporary table
    DROP TEMPORARY TABLE IF EXISTS temp_weighted_scores;
END //

DELIMITER ;
