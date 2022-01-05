UPDATE all_gid_2.txt_ratings SET txt_ratings.article_keywords=REPLACE(`article_keywords`, 'Game=yes', 'Gamer=yes') WHERE `article_keywords` LIKE '%Game=yes%';
UPDATE all_gid_2.txt_ratings SET txt_ratings.article_html_body=REPLACE(`article_html_body`, 'Game=yes', 'Gamer=yes') WHERE `article_html_body` LIKE '%Game=yes%';
UPDATE all_gid_2.txt_ratings SET txt_ratings.article_keywords=REPLACE(`article_keywords`, 'Curved=yes', 'Curved_scr=yes') WHERE `article_keywords` LIKE '%Curved=yes%';
UPDATE all_gid_2.txt_ratings SET txt_ratings.article_html_body=REPLACE(`article_html_body`, 'Curved=yes', 'Curved_scr=yes') WHERE `article_html_body` LIKE '%Curved=yes%';
