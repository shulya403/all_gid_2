SELECT * FROM all_gid_2.nb_products AS pd
INNER JOIN (SELECT DISTINCT fk_products FROM 
(SELECT * FROM all_gid_2.nb_products_has_nb_classes AS mtm1
WHERE fk_classes in (1, 3, 10)) AS mtm2) 
AS mtm
ON pd.id = mtm.fk_products;