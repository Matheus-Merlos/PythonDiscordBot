SELECT objectives.name, objectivetypes.description, objectives.xp_gain, objectives.gold_gain, objectives.description 
FROM objectives 
INNER JOIN objectivetypes ON objectives.type_id = objectivetypes.id
ORDER BY objectives.type_id, objectives.xp_gain ASC