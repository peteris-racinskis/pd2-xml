SELECT ref_name, ref_lname FROM penalties
SELECT firstname, lastname FROM referees INNER JOIN games ON referees.firstname=games.ref_name AND referees.lastname=games.ref_lname