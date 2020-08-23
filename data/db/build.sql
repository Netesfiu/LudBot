CREATE TABLE IF NOT EXISTS guilds (
	GuildID integer PRIMARY KEY,
	GuildName text DEFAULT NONE,
	Prefix text DEFAULT "//"
);

CREATE TABLE IF NOT EXISTS mutes (
	UserID integer PRIMARY KEY,
	RoleIDs text,
	EndTime text
);

CREATE TABLE IF NOT EXISTS HALLGATO (
	UserID integer PRIMARY KEY,
	Kozossegi integer DEFAULT 0,
	HashID text DEFAULT "0"
);