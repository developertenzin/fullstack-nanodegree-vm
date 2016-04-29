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
  player_id serial references players,
  Result int
);

INSERT INTO players (Name) VALUES
('Tenzin'),
('Qazi'),
('Illya'),
('Matthew');

SELECT * FROM players;

INSERT INTO matches (player_id, Result) VALUES
(1, 1),
(3, 1),
(2, 0),
(4, 0),
(1, 1);

SELECT * FROM matches;

CREATE VIEW player_standings as
  SELECT id ,
     name,
     count(CASE result WHEN 1 THEN 1 END) as wins,
     count(player_id) as matches
  FROM players
    LEFT OUTER JOIN matches
      ON players.id = matches.player_id
      GROUP BY id
      order by wins desc;

SELECT * FROM player_standings;


\c vagrant;
