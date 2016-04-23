-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE database tournament;
\c tournament;

CREATE TABLE players(
  ID serial primary key,
  Name text
);

CREATE TABLE matches(
  ID serial,
  Outcome text
);


INSERT INTO players (name) VALUES
  ('Tenzin Phuljung'),
  ('Rafeh Qazi'),
  ('Alvaro Font'),
  ('Thinktop Thoriyoki'),
  ('Conor Mcgregor');

SELECT * FROM players;

INSERT INTO matches VALUES (1, 'win');
INSERT INTO matches VALUES (1, 'win');
INSERT INTO matches VALUES (1, 'win');
INSERT INTO matches VALUES (1, 'loss');

INSERT INTO matches VALUES (3, 'win');
INSERT INTO matches VALUES (3, 'win');
INSERT INTO matches VALUES (3, 'win');
INSERT INTO matches VALUES (3, 'win');
INSERT INTO matches VALUES (3, 'win');
INSERT INTO matches VALUES (3, 'win');


INSERT INTO matches VALUES (5, 'win');
INSERT INTO matches VALUES (5, 'win');

SELECT * FROM matches;

SELECT players.id, players.name, matches.Outcome
FROM players
JOIN matches
ON players.id = matches.id;

SELECT inw.id, inw.name, inw.num_of_wins, nm.num_of_matches FROM (
  SELECT winners.id, winners.name, count(*) as num_of_wins FROM (
    SELECT demo.id, demo.name, demo.outcome FROM (
      SELECT players.id, players.name, matches.Outcome
      FROM players
      JOIN matches
      ON players.id = matches.id
    ) as demo where demo.outcome = 'win'
  ) as winners GROUP BY winners.id, winners.name
) as inw
JOIN (
  SELECT combo.id, combo.name, count(*) as num_of_matches FROM (
    SELECT players.id, players.name, matches.Outcome
    FROM players
    JOIN matches
    ON players.id = matches.id
  ) as combo GROUP BY combo.id, combo.name
) as nm
ON inw.id = nm.id;




/*SELECT combo.id, combo.name, count(*) as num_of_matches FROM (
  SELECT players.id, players.name, matches.Outcome
  FROM players
  JOIN matches
  ON players.id = matches.id
) as combo GROUP BY combo.id, combo.name;*/

\c vagrant;
