-- Cuantos artistas tienen más de 9 albumnes
SELECT ar."Name", COUNT(al."ArtistId") as cant_albunes
FROM "Album" al
JOIN "Artist" ar ON ar."ArtistId" = al."ArtistId"
GROUP BY ar."Name"
HAVING COUNT(al."ArtistId") > 9
ORDER BY cant_albunes ASC

-- Listar los clientes que residen en Canada 
SELECT c."CustomerId", c."FirstName", c."LastName"
FROM "Invoice" i
JOIN "Customer" c ON c."CustomerId" = i."CustomerId"
WHERE c."CustomerId" IN (
SELECT "CustomerId"
FROM "Invoice"
WHERE "BillingCountry" LIKE 'Canada' 
)

-- Obtener las canciones más largas que el promedio de duración
SELECT t."Name", t."Milliseconds"
FROM "Track" t
WHERE t."Milliseconds" > (
    SELECT AVG("Milliseconds") FROM "Track"
)
ORDER BY t."Milliseconds" DESC;

-- Clientes que no realizaron compras durante el 2013
SELECT c."CustomerId", c."FirstName"
FROM "Customer" c
JOIN "Invoice" i ON i."CustomerId" = c."CustomerId"
WHERE NOT EXISTS(
SELECT i."InvoiceDate"
FROM "Invoice" i
WHERE i."InvoiceDate" BETWEEN '2013-01-01 00:00:00' AND '2013-12-31 00:00:00'
)

-- Canciones que pertenecen al genero "Alternative"
SELECT t."Name", t."Composer"
FROM "Track" t
JOIN "Genre" g ON g."GenreId" = t."GenreId"
WHERE EXISTS(
SELECT 1
FROM "Genre" g
WHERE g."Name" LIKE 'Alternative'
)

-- Cuantas canciones hay en la playlist "Classical 101 - Deep Cuts"
SELECT pl."Name", COUNT(t."Name")
FROM "Playlist" pl
JOIN "PlaylistTrack" plt ON plt."PlaylistId" = pl."PlaylistId" 
JOIN "Track" t ON t."TrackId" = plt."TrackId"
WHERE pl."Name" LIKE 'Classical 101 - Deep Cuts'
GROUP BY pl."Name"
