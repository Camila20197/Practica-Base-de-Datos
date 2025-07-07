-- Mostrar el nombre y el genero de las canciones que duren 296000 o más del album "Heart of the Night"
SELECT a."Title", t."Name", g."Name"
FROM "Album" a, "Track" t, "Genre" g
WHERE t."AlbumId" = a."AlbumId" AND g."GenreId" = t."GenreId" 
		AND a."Title" LIKE 'Heart of the Night' AND t."Milliseconds" >= 296000 


--Consulta Optimizada
SELECT a."Title", t."Name", g."Name"
FROM "Album" a
JOIN "Track" t ON t."AlbumId" = a."AlbumId"
JOIN "Genre" g ON g."GenreId" = t."GenreId"
WHERE a."Title" LIKE 'Heart of the Night' AND t."Milliseconds" >= 296000 


