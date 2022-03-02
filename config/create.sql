/* Raw Type */
CREATE TABLE IF NOT EXISTS "main"."raw_type"(
"ID" INTEGER NOT NULL UNIQUE,
"_created" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"_updated" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"type_name" Varchar(10) NOT NULL UNIQUE,
PRIMARY KEY (ID AUTOINCREMENT)
);
INSERT OR IGNORE INTO raw_type (type_name) VALUES ("Mitgliedsart");
INSERT OR IGNORE INTO raw_type (type_name) VALUES ("E-Mail");
INSERT OR IGNORE INTO raw_type (type_name) VALUES ("Telefon");
INSERT OR IGNORE INTO raw_type (type_name) VALUES ("Position");
INSERT OR IGNORE INTO raw_type (type_name) VALUES ("Job");
/* date */
CREATE TRIGGER IF NOT EXISTS "trigger_update_raw_type"
    AFTER UPDATE ON "raw_type"
BEGIN
    UPDATE "raw_type" SET _updated = CAST(strftime('%s', 'now') AS INTEGER) WHERE ID=OLD.id;
END;

/* TYPE */
CREATE TABLE IF NOT EXISTS "main"."type" (
"ID" INTEGER NOT NULL UNIQUE,
"_created" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"_updated" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"name" Varchar(10) NOT NULL,
"type_id" INTEGER(1) NOT NULL,
"_active" INTEGER(1) DEFAULT 1,
PRIMARY KEY ("ID" AUTOINCREMENT),
FOREIGN KEY ("type_id") REFERENCES "raw_type"
);
/* date */
CREATE TRIGGER IF NOT EXISTS "trigger_update_type"
    AFTER UPDATE ON "type"
BEGIN
    UPDATE "type" SET _updated = CAST(strftime('%s', 'now') AS INTEGER) WHERE ID=OLD.id;
END;
/* Log Type */
CREATE TRIGGER IF NOT EXISTS "trigger_log_type"
    AFTER UPDATE ON "type"
    WHEN NEW.name IS NOT OLD.name
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("type",OLD.ID,"type",OLD.name, NEW.name);
END;
CREATE TRIGGER IF NOT EXISTS "trigger_log_new_type"
    AFTER INSERT ON "type"
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("type",NEW.ID,"type",NULL, NEW.name);
END;
CREATE TRIGGER IF NOT EXISTS "trigger_log_delete_type"
    AFTER DELETE ON "type"
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("type",OLD.ID,"type",OLD.name, NULL);
END;
/* Active Type */
CREATE VIEW IF NOT EXISTS "main"."v_active_type" AS
SELECT type.ID, type.name, type.type_id, raw_type.type_name
FROM type INNER JOIN raw_type ON type.type_id = raw_type.ID
WHERE type._active = 1;
/* Active Member Type */
CREATE VIEW IF NOT EXISTS "main"."v_inactive_type" AS
SELECT type.ID,type.name,type.type_id,raw_type.type_name
FROM type INNER JOIN raw_type ON type.type_id = raw_type.ID
WHERE type._active = 0;
/* Active Member Type */
CREATE VIEW IF NOT EXISTS "main"."v_active_member_type" AS
SELECT type.ID,type.name,type.type_id,raw_type.type_name
FROM type INNER JOIN raw_type ON type.type_id = raw_type.ID
WHERE type._active = 1 AND type_id IN (1,2,3,4);
/* Inactive Member Type */
CREATE VIEW IF NOT EXISTS "main"."v_inactive_member_type" AS
SELECT type.ID,type.name,type.type_id,raw_type.type_name
FROM type INNER JOIN raw_type ON type.type_id = raw_type.ID
WHERE type._active = 0 AND type_id IN (1,2,3,4);


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
/* Log */
CREATE TRIGGER IF NOT EXISTS "trigger_log_member_phone"
    AFTER UPDATE ON "member_phone"
    WHEN NEW.number IS NOT OLD.number
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("member_phone",OLD.ID,"number",OLD.number, NEW.number);
END;
CREATE TRIGGER IF NOT EXISTS "trigger_log_member_phone_first"
    AFTER INSERT ON "member_phone"
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("member_phone",NEW.ID,"number",NULL, NEW.number);
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
/* Log */
CREATE TRIGGER IF NOT EXISTS "trigger_log_member_mail"
    AFTER UPDATE ON "member_mail"
    WHEN NEW.mail IS NOT OLD.mail
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("member_mail",OLD.ID,"mail",OLD.mail, NEW.mail);
END;
CREATE TRIGGER IF NOT EXISTS "trigger_log_member_mail_first"
    AFTER INSERT ON "member_mail"
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("member_mail",NEW.ID,"mail",NULL, NEW.mail);
END;

/* MEMBER POSITION */
CREATE TABLE IF NOT EXISTS "main"."member_position" (
"ID" INTEGER NOT NULL UNIQUE,
"_created" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"_updated" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
"member_id" INTEGER NOT NULL,
"type_id" INTEGER NOT NULL,
"_active" INTEGER DEFAULT 1,
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
/* Log */
CREATE TRIGGER IF NOT EXISTS "trigger_log_member_position"
    AFTER UPDATE ON "member_position"
    WHEN NEW._active IS NOT OLD._active
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("member_position",OLD.ID,"position",OLD._active, NEW._active);
END;
CREATE TRIGGER IF NOT EXISTS "trigger_log_member_position_first"
    AFTER INSERT ON "member_position"
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("member_position",NEW.ID,"position",NULL, NEW._active);
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
SELECT ID,first_name,last_name,street,number,zip_code,city,b_day,entry_day,membership_type,special_member,comment
FROM member
WHERE active = 1;

/* Inactive Member */
CREATE VIEW IF NOT EXISTS "main"."v_inactive_member" AS
SELECT ID,first_name,last_name,street,number,zip_code,city,b_day,entry_day,membership_type,special_member,comment
FROM member
WHERE active = 0;

/* date */
CREATE TRIGGER IF NOT EXISTS "trigger_update_member"
    AFTER UPDATE ON "member"
BEGIN
    UPDATE "member" SET _updated = CAST(strftime('%s', 'now') AS INTEGER) WHERE ID=OLD.id;
END;
/* Log (first_name) */
CREATE TRIGGER IF NOT EXISTS "trigger_log_member_first_name"
    AFTER UPDATE ON "member"
    WHEN NEW.first_name IS NOT OLD.first_name
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("member",OLD.ID,"first_name",OLD.first_name, NEW.first_name);
END;
/* Log (last_name) */
CREATE TRIGGER IF NOT EXISTS "trigger_log_member_last_name"
    AFTER UPDATE ON "member"
    WHEN NEW.last_name IS NOT OLD.last_name
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("member",OLD.ID,"last_name",OLD.last_name, NEW.last_name);
END;
/* Log (street) */
CREATE TRIGGER IF NOT EXISTS "trigger_log_member_street"
    AFTER UPDATE ON "member"
    WHEN NEW.street IS NOT OLD.street
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("member",OLD.ID,"street",OLD.street, NEW.street);
END;
/* Log (number) */
CREATE TRIGGER IF NOT EXISTS "trigger_log_member_number"
    AFTER UPDATE ON "member"
    WHEN NEW.number IS NOT OLD.number
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("member",OLD.ID,"number",OLD.number, NEW.number);
END;
/* Log (zip_code) */
CREATE TRIGGER IF NOT EXISTS "trigger_log_member_zip_code"
    AFTER UPDATE ON "member"
    WHEN NEW.zip_code IS NOT OLD.zip_code
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("member",OLD.ID,"zip_code",OLD.zip_code, NEW.zip_code);
END;
/* Log (city) */
CREATE TRIGGER IF NOT EXISTS "trigger_log_member_city"
    AFTER UPDATE ON "member"
    WHEN NEW.city IS NOT OLD.city
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("member",OLD.ID,"city",OLD.city, NEW.city);
END;
/* Log (b_day) */
CREATE TRIGGER IF NOT EXISTS "trigger_log_member_b_day"
    AFTER UPDATE ON "member"
    WHEN NEW.b_day IS NOT OLD.b_day
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("member",OLD.ID,"b_day",OLD.b_day, NEW.b_day);
END;
/* Log (entry_day) */
CREATE TRIGGER IF NOT EXISTS "trigger_log_member_entry_day"
    AFTER UPDATE ON "member"
    WHEN NEW.entry_day IS NOT OLD.entry_day
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("member",OLD.ID,"entry_day",OLD.entry_day, NEW.entry_day);
END;
/* Log (membership_type) */
CREATE TRIGGER IF NOT EXISTS "trigger_log_member_membership_type"
    AFTER UPDATE ON "member"
    WHEN NEW.membership_type IS NOT OLD.membership_type
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("member",OLD.ID,"membership_type",OLD.membership_type, NEW.membership_type);
END;
/* Log (special_member) */
CREATE TRIGGER IF NOT EXISTS "trigger_log_member_special_member"
    AFTER UPDATE ON "member"
    WHEN NEW.special_member IS NOT OLD.special_member
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("member",OLD.ID,"special_member",OLD.special_member, NEW.special_member);
END;
/* Log (comment) */
CREATE TRIGGER IF NOT EXISTS "trigger_log_member_comment"
    AFTER UPDATE ON "member"
    WHEN NEW.comment IS NOT OLD.comment
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("member",OLD.ID,"comment",OLD.comment, NEW.comment);
END;
/* Log (active) */
CREATE TRIGGER IF NOT EXISTS "trigger_log_member_active"
    AFTER UPDATE ON "member"
    WHEN NEW.active IS NOT OLD.active
BEGIN
    INSERT INTO "log" (_target_table,_target_id,_target_column,old_data,new_data) VALUES
    ("member",OLD.ID,"active",OLD.active, NEW.active);
END;



/* LOG */
CREATE TABLE IF NOT EXISTS "main"."log" (
"_ID" INTEGER NOT NULL UNIQUE,
"_target_table" VARCHAR(10) NOT NULL,
"_target_id" INTEGER NOT NULL,
"_target_column" VARCHAR(10) NOT NULL,
"old_data" BLOB DEFAULT NULL,
"new_data" BLOB DEFAULT NULL,
"created" INTEGER DEFAULT (CAST(strftime('%s', 'now') AS INTEGER)),
PRIMARY KEY ("_ID" AUTOINCREMENT)
);

/* QUERRY */
CREATE TABLE IF NOT EXISTS "query" (
"_ID" INTEGER NOT NULL UNIQUE,
"_target_table" VARCHAR(10) NOT NULL,
"_target_column" VARCHAR(10) NOT NULL,
"_target_data" BLOB NOT NULL,
"_target_id" INTEGER,
"_exec_time" INTEGER,
PRIMARY KEY("_ID" AUTOINCREMENT)
);