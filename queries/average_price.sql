SELECT sum(scout.price) / {} as {} , player.name
  FROM
      (SELECT player.player_id as p_id, player.name as p_name, player.year as p_year,
      scout.match_week as s_round FROM scout
      LEFT JOIN player ON scout.player_id = player.player_id AND scout.year = player.year
      WHERE scout.id = {}) s1, player
LEFT JOIN scout ON player.player_id = scout.player_id AND player.year = scout.year
WHERE player.player_id = s1.p_id AND player.year = p_year
AND scout.match_week < s1.s_round AND scout.match_week >= s1.s_round - {}
GROUP BY player.name;