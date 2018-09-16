SELECT
  -1 AS turfid,
  voter.voterid AS voterid,
  MAX(voter.address) AS address,
  COALESCE(MAX(voter.resext), '') AS apt,
  MAX(voter.firstname) AS firstname,
  MAX(voter.lastname) AS lastname,
  MAX(voter.gender) AS gender,
  MAX(EXTRACT(YEAR FROM NOW()) - voter.yob) AS age,

  MAX((voter.electiondate='2018-05-08')::integer) AS v_may,
  MAX((voter.electiondate='2017-11-07')::integer) AS v_nov,
  MAX((voter.electiondate='2017-08-08')::integer) AS v_aug,

  -- MAX(FLOOR(voter.resstreetnum/100) * 100) AS prop_street,
  MAX('Lot '||arrowwoodlots.lot) AS prop_street,
  MAX(voter.resstreetnum) AS prop_street_num
  
  
FROM
  voter voter
  LEFT JOIN data.arrowwoodlots ON voter.resstreetnum >= arrowwoodlots.startaddr and voter.resstreetnum <= arrowwoodlots.endaddr AND arrowwoodlots.odd = voter.resstreetnum % 2

WHERE
  voter.streetname LIKE '%ARROWWOOD%'

GROUP BY
  voter.voterid

ORDER BY
  MAX(voter.streetname),
  MAX('Lot '||arrowwoodlots.lot),
  MAX(voter.resstreetnum),
  MAX(voter.resext)
