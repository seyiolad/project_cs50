SELECT DISTINCT people.name
FROM stars AS kb_stars
JOIN movies AS kb_movies ON kb_stars.movie_id = kb_movies.id
JOIN stars AS co_stars ON kb_movies.id = co_stars.movie_id
JOIN people ON co_stars.person_id = people.id
WHERE kb_stars.person_id IN (
  SELECT id FROM people WHERE name = 'Kevin Bacon' AND birth = 1958
)
AND people.id NOT IN (
  SELECT id FROM people WHERE name = 'Kevin Bacon' AND birth = 1958
);
