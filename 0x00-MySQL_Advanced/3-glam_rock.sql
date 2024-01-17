-- List Glam rock bands ranked by longevity
SELECT band_name,
       IF(splitted[2] != '0', 2022 - CAST(splitted[2] AS SIGNED), 0) AS lifespan
FROM metal_bands,
     SPLIT_STR(formed, '-', 3) AS splitted
WHERE FIND_IN_SET('Glam rock', style) > 0
ORDER BY lifespan DESC;