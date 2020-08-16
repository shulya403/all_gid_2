SELECT *
FROM all_gid_2.nb_vardata
JOIN
(SELECT * FROM all_gid_2.nb_products AS pd
JOIN all_gid_2.nb_products_has_nb_classes AS mtm
ON pd.id = mtm.fk_products
WHERE fk_classes in (1, 3, 10)) AS jn
ON jn.fk_products=nb_vardata.fk_products
WHERE nb_vardata.`month` = '2020-05-01';