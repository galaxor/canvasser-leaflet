SELECT
  testturfs.id,
  MAX(voter_geom.address) AS address,
  MAX(voter_geom.resext) AS apt,
  MAX(voter_geom.firstname) AS firstname,
  MAX(voter_geom.lastname) AS lastname,
  MAX(voter_geom.gender) AS gender,
  MAX(EXTRACT(YEAR FROM NOW()) - voter_geom.yob) AS age,

  MAX((voter_geom.electiondate='2018-05-08')::integer) AS v_may,
  MAX((voter_geom.electiondate='2017-11-07')::integer) AS v_nov,
  MAX((voter_geom.electiondate='2017-08-08')::integer) AS v_aug
  
  
FROM
  testturfs 
  LEFT JOIN voter_geom voter_geom ON ST_Within(voter_geom.geom, testturfs.geom)

GROUP BY
  testturfs.id,
  voter_geom.voterid

ORDER BY
  testturfs.id,

  MAX(voter_geom.prop_street),
  MAX(voter_geom.prop_street_num) % 2,
  MAX(voter_geom.prop_street_num),
  MAX(voter_geom.resext)
