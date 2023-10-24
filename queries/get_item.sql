SELECT item.name, item.price, itemtypes.description, item.durability, item.description 
FROM item 
INNER JOIN itemtypes ON item.id_type = itemtypes.id WHERE item.name = ?;