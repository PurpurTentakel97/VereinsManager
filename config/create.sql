/* Raw Type */
CREATE TABLE IF NOT EXISTS "main"."raw_type"(
"ID" INTEGER NOT NULL UNIQUE,
"_created" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"_updated" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"type_name" Varchar(10) NOT NULL UNIQUE,
PRIMARY KEY ("ID")
);
INSERT OR IGNORE INTO raw_type (ID,type_name) VALUES (1,"Mitgliedsart");
INSERT OR IGNORE INTO raw_type (ID,type_name) VALUES (2,"E-Mail");
INSERT OR IGNORE INTO raw_type (ID,type_name) VALUES (3,"Telefon");
INSERT OR IGNORE INTO raw_type (ID,type_name) VALUES (4,"Position");
INSERT OR IGNORE INTO raw_type (ID,type_name) VALUES (5,"Land");
INSERT OR IGNORE INTO raw_type (ID,type_name) VALUES (6,"Plan Eintrag");

/* TYPE */
CREATE TABLE IF NOT EXISTS "main"."type" (
"ID" INTEGER NOT NULL UNIQUE,
"_created" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"_updated" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"name" Varchar(10) NOT NULL,
"type_id" INTEGER(1) NOT NULL,
"extra_value" VARCHAR(10) Default NULL,
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
SELECT type.ID, type.name, type.extra_value, type.type_id, raw_type.type_name
FROM type INNER JOIN raw_type ON type.type_id = raw_type.ID
WHERE type.active = 1;
/* Inactive Type */
CREATE VIEW IF NOT EXISTS "main"."v_inactive_type" AS
SELECT type.ID, type.name, type.extra_value, type.type_id, raw_type.type_name
FROM type INNER JOIN raw_type ON type.type_id = raw_type.ID
WHERE type.active = 0;
/* Active Member Type */
CREATE VIEW IF NOT EXISTS "main"."v_active_member_type" AS
SELECT type.ID,type.name,type.type_id,raw_type.type_name
FROM type INNER JOIN raw_type ON type.type_id = raw_type.ID
WHERE type.active = 1 AND type_id IN (1,2,3,4,5);
/* Inactive Member Type */
CREATE VIEW IF NOT EXISTS "main"."v_inactive_member_type" AS
SELECT type.ID,type.name,type.type_id,raw_type.type_name
FROM type INNER JOIN raw_type ON type.type_id = raw_type.ID
WHERE type.active = 0 AND type_id IN (1,2,3,4,5);


/* MEMBER PHONE */
CREATE TABLE IF NOT EXISTS "main"."member_phone" (
"ID" INTEGER NOT NULL UNIQUE,
"_created" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"_updated" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"member_id" INTEGER NOT NULL,
"type_id" INTEGER NOT NULL,
"number" VARCHAR(10),
"_active_member" INTEGER(1) DEFAULT 1,
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
"_active_member" INTEGER(1) DEFAULT 1,
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
"_active_member" INTEGER(1) DEFAULT 1,
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
"zip_code" VARCHAR(10),
"city" VARCHAR(10),
"country" INTEGER(1),
"maps" VARCHAR(50),
"b_day" INTEGER,
"entry_day" INTEGER,
"membership_type" INTEGER(1),
"special_member" INTEGER(1) DEFAULT 0,
"comment" VARCHAR,
"active" INTEGER(1) DEFAULT 1,
PRIMARY KEY ("ID" AUTOINCREMENT)
FOREIGN KEY ("membership_type") REFERENCES "type"
FOREIGN KEY ("country") REFERENCES "type"
);
/* Active Member */
CREATE VIEW IF NOT EXISTS "main"."v_active_member" AS
SELECT ID,first_name,last_name,street,number,zip_code,city,country,maps,b_day,entry_day,membership_type,special_member,comment
FROM member
WHERE active = 1;

/* Inactive Member */
CREATE VIEW IF NOT EXISTS "main"."v_inactive_member" AS
SELECT ID,first_name,last_name,street,number,zip_code,city,country,maps,b_day,entry_day,membership_type,special_member,comment
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
"_created" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"_updated" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"target_table" VARCHAR(10) NOT NULL,
"target_id" INTEGER NOT NULL,
"target_column" VARCHAR(10) NOT NULL,
"old_data" BLOB DEFAULT NULL,
"new_data" BLOB DEFAULT NULL,
"log_date" INTEGER NOT NULL,
PRIMARY KEY ("ID" AUTOINCREMENT)
);
/* date */
CREATE TRIGGER IF NOT EXISTS "trigger_update_log"
    AFTER UPDATE ON "log"
BEGIN
    UPDATE "log" SET _updated = CAST(strftime('%s', 'now') AS INTEGER) WHERE ID=OLD.id;
END;

/*USER*/
CREATE TABLE IF NOT EXISTS "main"."user" (
"ID" INTEGER NOT NULL UNIQUE,
"_created" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"_updated" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"first_name" VARCHAR(10),
"last_name" VARCHAR(10),
"street" VARCHAR(20),
"number" VARCHAR(10),
"zip_code" VARCHAR(10),
"city" VARCHAR(10),
"country" VARCHAR(10),
"phone" VARCHAR(10),
"mail" VARCHAR(20),
"position" VARCHAR(20),
"password" VARCHAR NOT NULL,
"_active" INTEGER(1) DEFAULT 1,
PRIMARY KEY ("ID" AUTOINCREMENT)
);
INSERT OR IGNORE INTO user (ID,first_name, last_name, password) VALUES (1,"Default","Default","$2b$12$o1u7aISUrLVJmKKq3XcGDuA2rOhU25Bg5uFJR8Fpwld4z.gKCnQK2");
/* Active User */
CREATE VIEW IF NOT EXISTS "main"."v_active_user" AS
SELECT ID,first_name,last_name,street,number,zip_code,city,country,phone,mail,position
FROM "user"
WHERE _active = 1;

/* Active User Password */
CREATE VIEW IF NOT EXISTS "main"."v_active_user_password" AS
SELECT ID,password
FROM "user"
WHERE _active = 1;

/* Inactive User */
CREATE VIEW IF NOT EXISTS "main"."v_inactive_user" AS
SELECT ID,first_name,last_name,street,number,zip_code,city,country,phone,mail,position
FROM "user"
WHERE _active = 0;

/* date */
CREATE TRIGGER IF NOT EXISTS "trigger_update_user"
    AFTER UPDATE ON "user"
BEGIN
    UPDATE "user" SET _updated = CAST(strftime('%s', 'now') AS INTEGER) WHERE ID=OLD.id;
END;

/* Statistics */
CREATE TABLE IF NOT EXISTS "main"."statistics" (
"ID" INTEGER NOT NULL UNIQUE,
"_created" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"_updated" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"_log_date" INTEGER NOT NULL,
"raw_type_id" INTEGER NOT NULL,
"type_id" INTEGER NOT NULL,
"count" INTEGER NOT NULL,
PRIMARY KEY ("ID" AUTOINCREMENT),
FOREIGN KEY ("type_id") REFERENCES "type",
FOREIGN KEY ("raw_type_id") REFERENCES "raw_type"
);

/* date */
CREATE TRIGGER IF NOT EXISTS "trigger_update_statistics"
    AFTER UPDATE ON "statistics"
BEGIN
    UPDATE "statistics" SET _updated = CAST(strftime('%s', 'now') AS INTEGER) WHERE ID=OLD.id;
END;

/* Organisation */
CREATE TABLE IF NOT EXISTS "main"."organisation" (
"ID" INTEGER NOT NULL UNIQUE,
"_created" INTEGER Default (CAST(strftime('%s','now')AS INTEGER)),
"_updated" INTEGER Default (CAST(strftime('%s','now')AS INTEGER)),
"name" VARCHAR(30),
"street" VARCHAR(30),
"number" VARCHAR(10),
"zip_code" VARCHAR(10),
"city" VARCHAR(10),
"country" VARCHAR(15),
"bank_name" VARCHAR(30),
"bank_owner" VARCHAR(30),
"bank_IBAN" VARCHAR(15),
"bank_BIC" VARCHAR(10),
"contact_person" INTEGER(1),
"web_link" VARCHAR(50),
"extra_text" VARCHAR,
PRIMARY KEY ("ID" AUTOINCREMENT),
FOREIGN KEY ("contact_person") REFERENCES "user"
);

/* date */
CREATE TRIGGER IF NOT EXISTS "trigger_update_organisation"
    AFTER UPDATE ON "organisation"
BEGIN
    UPDATE "organisation" SET _updated = CAST(strftime('%s', 'now') AS INTEGER) WHERE ID=OLD.id;
END;

/* Location */
CREATE TABLE IF NOT EXISTS "main"."location" (
"ID" INTEGER NOT NULL UNIQUE,
"_created" INTEGER Default (CAST(strftime('%s','now')AS INTEGER)),
"_updated" INTEGER Default (CAST(strftime('%s','now')AS INTEGER)),
"owner" VARCHAR(30),
"name" VARCHAR(30),
"street" VARCHAR(30),
"number" VARCHAR(10),
"zip_code" VARCHAR(10),
"city" VARCHAR(10),
"country" INTEGER(1),
"maps_link" VARCHAR(30),
"comment" VARCHAR,
"_active" INTEGER(1) Default 1,
PRIMARY KEY ("ID" AUTOINCREMENT),
FOREIGN KEY ("country") REFERENCES "type"
);
/* Active Location */
CREATE VIEW IF NOT EXISTS "main"."v_active_location" AS
SELECT ID,owner,name,street,number,zip_code,city,country,maps_link,comment
FROM location
WHERE _active = 1;

/* Inactive Location */
CREATE VIEW IF NOT EXISTS "main"."v_inactive_location" AS
SELECT ID,owner,name,street,number,zip_code,city,country,maps_link,comment
FROM location
WHERE _active = 0;

/* date */
CREATE TRIGGER IF NOT EXISTS "trigger_update_location"
    AFTER UPDATE ON "location"
BEGIN
    UPDATE "location" SET _updated = CAST(strftime('%s', 'now') AS INTEGER) WHERE ID=OLD.id;
END;

/* Schedule Day */
CREATE TABLE IF NOT EXISTS "main"."schedule_day" (
"ID" INTEGER NOT NULL UNIQUE,
"_created" INTEGER Default (CAST(strftime('%s','now')AS INTEGER)),
"_updated" INTEGER Default (CAST(strftime('%s','now')AS INTEGER)),
"date" INTEGER NOT NULL,
"hour" INTEGER(2),
"minute" INTEGER(2),
"location" INTEGER(1) NOT NULL,
"uniform" VARCHAR(10),
"comment" VARCHAR,
"_active" INTEGER(1) Default 1,
PRIMARY KEY ("ID" AUTOINCREMENT),
FOREIGN KEY ("location") REFERENCES "location"
);
/* Active Schedule Day */
CREATE VIEW IF NOT EXISTS "main"."v_active_schedule_day" AS
SELECT ID,date,hour,minute,location,uniform,comment
FROM schedule_day
WHERE _active = 1;

/* Inactive Schedule Day */
CREATE VIEW IF NOT EXISTS "main"."v_inactive_schedule_day" AS
SELECT ID,date,hour,minute,location,uniform,comment
FROM schedule_day
WHERE _active = 0;

/* date */
CREATE TRIGGER IF NOT EXISTS "trigger_update_schedule_day"
    AFTER UPDATE ON "schedule_day"
BEGIN
    UPDATE "schedule_day" SET _updated = CAST(strftime('%s', 'now') AS INTEGER) WHERE ID=OLD.id;
END;

/*Schedule Entry*/
CREATE TABLE IF NOT EXISTS "main"."schedule_entry" (
"ID" INTEGER NOT NULL UNIQUE,
"_created" INTEGER Default (CAST(strftime('%s','now')AS INTEGER)),
"_updated" INTEGER Default (CAST(strftime('%s','now')AS INTEGER)),
"day" INTEGER(1) NOT NULL,
"title" VARCHAR(10) NOT NULL,
"hour" INTEGER(2),
"minute" INTEGER(2),
"entry_type" INTEGER(1) NOT NULL,
"location" INTEGER(1) NOT NULL,
"comment" VARCHAR,
"_active" INTEGER(1) Default 1,
PRIMARY KEY ("ID" AUTOINCREMENT),
FOREIGN KEY ("entry_type") REFERENCES "type",
FOREIGN KEY ("day") REFERENCES "schedule_day",
FOREIGN KEY ("location") REFERENCES "location"
);
/* Active Schedule Entry */
CREATE VIEW IF NOT EXISTS "main"."v_active_schedule_entry" AS
SELECT ID,day,title,hour,minute,entry_type,location,comment
FROM schedule_entry
WHERE _active = 1;

/* Inactive Schedule Entry */
CREATE VIEW IF NOT EXISTS "main"."v_inactive_schedule_entry" AS
SELECT ID,day,title,hour,minute,entry_type,location,comment
FROM schedule_entry
WHERE _active = 0;

/* date */
CREATE TRIGGER IF NOT EXISTS "trigger_update_schedule_entry"
    AFTER UPDATE ON "schedule_entry"
BEGIN
    UPDATE "schedule_entry" SET _updated = CAST(strftime('%s', 'now') AS INTEGER) WHERE ID=OLD.id;
END;