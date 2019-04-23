select book1, book2, count(*) from Story group by book1, book2 HAVING count(*)>5 ORDER BY count(*);
