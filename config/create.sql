/* Raw Type */
CREATE TABLE IF NOT EXISTS "main"."raw_type"(
"ID" INTEGER NOT NULL UNIQUE,
"_created" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"_updated" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"type_name" Varchar(10) NOT NULL UNIQUE,
PRIMARY KEY ("ID" AUTOINCREMENT)
);
INSERT OR IGNORE INTO raw_type (type_name) VALUES ("Mitgliedsart");
INSERT OR IGNORE INTO raw_type (type_name) VALUES ("E-Mail");
INSERT OR IGNORE INTO raw_type (type_name) VALUES ("Telefon");
INSERT OR IGNORE INTO raw_type (type_name) VALUES ("Position");
INSERT OR IGNORE INTO raw_type (type_name) VALUES ("Job");

/* TYPE */
CREATE TABLE IF NOT EXISTS "main"."type" (
"ID" INTEGER NOT NULL UNIQUE,
"_created" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"_updated" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"name" Varchar(10) NOT NULL,
"type_id" INTEGER(1) NOT NULL,
"active" INTEGER(1) DEFAULT 1,
PRIMARY KEY ("ID" AUTOINCREMENT),
FOREIGN KEY ("type_id") REFERENCES "raw_type"
);
/* date */
CREATE TRIGGER IF NOT EXISTS "trigger_update_type"
    AFTER UPDATE ON "type"
BEGIN
    UPDATE "type" SET _updated = CAST(strftime('%s', 'now') AS INTEGER) WHERE ID=OLD.id;
END;

/* Active Type */
CREATE VIEW IF NOT EXISTS "main"."v_active_type" AS
SELECT type.ID, type.name, type.type_id, raw_type.type_name
FROM type INNER JOIN raw_type ON type.type_id = raw_type.ID
WHERE type.active = 1;
/* Active Member Type */
CREATE VIEW IF NOT EXISTS "main"."v_inactive_type" AS
SELECT type.ID,type.name,type.type_id,raw_type.type_name
FROM type INNER JOIN raw_type ON type.type_id = raw_type.ID
WHERE type.active = 0;
/* Active Member Type */
CREATE VIEW IF NOT EXISTS "main"."v_active_member_type" AS
SELECT type.ID,type.name,type.type_id,raw_type.type_name
FROM type INNER JOIN raw_type ON type.type_id = raw_type.ID
WHERE type.active = 1 AND type_id IN (1,2,3,4);
/* Inactive Member Type */
CREATE VIEW IF NOT EXISTS "main"."v_inactive_member_type" AS
SELECT type.ID,type.name,type.type_id,raw_type.type_name
FROM type INNER JOIN raw_type ON type.type_id = raw_type.ID
WHERE type.active = 0 AND type_id IN (1,2,3,4);


/* MEMBER PHONE */
CREATE TABLE IF NOT EXISTS "main"."member_phone" (
"ID" INTEGER NOT NULL UNIQUE,
"_created" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"_updated" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"member_id" INTEGER NOT NULL,
"type_id" INTEGER NOT NULL,
"number" VARCHAR(10),
PRIMARY KEY ("ID" AUTOINCREMENT),
FOREIGN KEY ("member_id") REFERENCES "member",
FOREIGN KEY ("type_id") REFERENCES "type"
);
/* date */
CREATE TRIGGER IF NOT EXISTS "trigger_update_member_phone"
    AFTER UPDATE ON "member_phone"
BEGIN
    UPDATE "member_phone" SET _updated = CAST(strftime('%s', 'now') AS INTEGER) WHERE ID=OLD.id;
END;

/* MEMBER MAIL */
CREATE TABLE IF NOT EXISTS "main"."member_mail" (
"ID" INTEGER NOT NULL UNIQUE,
"_created" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"_updated" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"member_id" INTEGER NOT NULL,
"type_id" INTEGER NOT NULL,
"mail" VARCHAR(20),
PRIMARY KEY ("ID" AUTOINCREMENT),
FOREIGN KEY ("member_id") REFERENCES "member",
FOREIGN KEY ("type_id") REFERENCES "type"
);
/* date */
CREATE TRIGGER IF NOT EXISTS "trigger_update_member_mail"
    AFTER UPDATE ON "member_mail"
BEGIN
    UPDATE "member_mail" SET _updated = CAST(strftime('%s', 'now') AS INTEGER) WHERE ID=OLD.id;
END;

/* MEMBER POSITION */
CREATE TABLE IF NOT EXISTS "main"."member_position" (
"ID" INTEGER NOT NULL UNIQUE,
"_created" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"_updated" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"member_id" INTEGER NOT NULL,
"type_id" INTEGER NOT NULL,
"active" INTEGER DEFAULT 1,
PRIMARY KEY ("ID" AUTOINCREMENT),
FOREIGN KEY ("member_id") REFERENCES "member",
FOREIGN KEY ("type_id") REFERENCES "type"
);
/* date */
CREATE TRIGGER IF NOT EXISTS "trigger_update_member_position"
    AFTER UPDATE ON "member_position"
BEGIN
    UPDATE "member_position" SET _updated = CAST(strftime('%s', 'now') AS INTEGER) WHERE ID=OLD.id;
END;

/* MEMBER */
CREATE TABLE IF NOT EXISTS "main"."member" (
"ID" INTEGER NOT NULL UNIQUE,
"_created" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"_updated" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"first_name" VARCHAR(10),
"last_name" VARCHAR(10),
"street" VARCHAR(20),
"number" VARCHAR(10),
"zip_code" INTEGER(10),
"city" VARCHAR(10),
"maps" VARCHAR(50),
"b_day" INTEGER,
"entry_day" INTEGER,
"membership_type" INTEGER(1),
"special_member" INTEGER(1) DEFAULT 0,
"comment" VARCHAR,
"active" INTEGER(1) DEFAULT 1,
PRIMARY KEY ("ID" AUTOINCREMENT)
FOREIGN KEY ("membership_type") REFERENCES "type"
);
/* Active Member */
CREATE VIEW IF NOT EXISTS "main"."v_active_member" AS
SELECT ID,first_name,last_name,street,number,zip_code,city,maps,b_day,entry_day,membership_type,special_member,comment
FROM member
WHERE active = 1;

/* Inactive Member */
CREATE VIEW IF NOT EXISTS "main"."v_inactive_member" AS
SELECT ID,first_name,last_name,street,number,zip_code,city,maps,b_day,entry_day,membership_type,special_member,comment
FROM member
WHERE active = 0;

/* date */
CREATE TRIGGER IF NOT EXISTS "trigger_update_member"
    AFTER UPDATE ON "member"
BEGIN
    UPDATE "member" SET _updated = CAST(strftime('%s', 'now') AS INTEGER) WHERE ID=OLD.id;
END;

/* LOG */
CREATE TABLE IF NOT EXISTS "main"."log" (
"ID" INTEGER NOT NULL UNIQUE,
"target_table" VARCHAR(10) NOT NULL,
"target_id" INTEGER NOT NULL,
"target_column" VARCHAR(10) NOT NULL,
"old_data" BLOB DEFAULT NULL,
"new_data" BLOB DEFAULT NULL,
"log_date" INTEGER NOT NULL,
"_created" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
PRIMARY KEY ("ID" AUTOINCREMENT)
);
