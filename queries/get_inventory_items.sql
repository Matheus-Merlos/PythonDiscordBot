SELECT item.name, COUNT(*) AS quantity 
FROM inventarioitem
INNER JOIN item ON inventarioitem.item_id = item.id
WHERE inventarioitem.player_id = ?
AND inventarioitem.current_durability > 0
GROUP BY item.name
ORDER BY item.name ASC;