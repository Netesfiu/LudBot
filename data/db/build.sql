CREATE TABLE IF NOT EXISTS guilds (
	ServerID integer PRIMARY KEY,
	ServerName text DEFAULT NONE,
	Prefix text DEFAULT "//"
);

CREATE TABLE IF NOT EXISTS mutes (
	UserID integer PRIMARY KEY,
	RoleIDs text,
	EndTime text
);

CREATE TABLE IF NOT EXISTS hallgato (
	UserID integer PRIMARY KEY,
    NEPTUN text DEFAULT "Nem Regisztrált",
	Kollegium integer DEFAULT 0,
	Kozossegi integer DEFAULT 1
);