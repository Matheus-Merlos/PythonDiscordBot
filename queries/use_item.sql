UPDATE inventarioitem
SET current_durability = current_durability - 1
WHERE item_id = ? AND player_id = ? AND current_durability > 0
LIMIT 1;