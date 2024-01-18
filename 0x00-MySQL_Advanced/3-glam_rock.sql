-- List Glam rock bands ranked by longevity
SELECT band_name,
       IFNULL(SUBSTRING_INDEX(formed, '-', -1) != '0', 2022 - CAST(SUBSTRING_INDEX(formed, '-', -1) AS SIGNED), 0) AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', IFNULL(style, "")) > 0
ORDER BY lifespan DESC;