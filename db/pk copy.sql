
-- -----------------------------------------------------
-- Table settings
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS settings (
    setting_id INTEGER,
    search_directory TEXT NOT NULL,
    output_directory TEXT NOT NULL,
    original_directory INTEGER NOT NULL DEFAULT 0,
    overwrite_packed_textures INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (setting_id)
);



-- -----------------------------------------------------
-- Table texture_types
-- -----------------------------------------------------
DROP TABLE IF EXISTS texture_types;
CREATE TABLE IF NOT EXISTS texture_types (
    texture_type_id INTEGER NOT NULL,
    setting_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    preferred_identifier TEXT NOT NULL,
    PRIMARY KEY (texture_type_id),
    FOREIGN KEY (setting_id)
        REFERENCES settings (setting_id)
            ON DELETE NO ACTION
            ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table packing_groups
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS packing_groups (
    packing_group_id INTEGER NOT NULL,
    setting_id INTEGER NOT NULL,
    extension TEXT NOT NULL,
    identifier TEXT NOT NULL,
    at_end INTEGER NOT NULL DEFAULT 0,
    channel_r_type TEXT,
    channel_g_type TEXT,
    channel_b_type TEXT,
    channel_a_type TEXT,
    PRIMARY KEY (packing_group_id),
    FOREIGN KEY (setting_id)
        REFERENCES settings (setting_id)
        ON DELETE NO ACTION
        ON UPDATE CASCADE
);


-- -----------------------------------------------------
-- Table identifiers
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS identifiers (
    identifier_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY (identifier_id)
);



-- -----------------------------------------------------
-- Table texture_type_identifiers
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS texture_type_identifiers (
    texture_type_id INTEGER NOT NULL,
    identifier_id INTEGER NOT NULL,
    PRIMARY KEY (texture_type_id, identifier_id),
    FOREIGN KEY (texture_type_id)
        REFERENCES texture_types (texture_type_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (identifier_id)
        REFERENCES identifiers (identifier_id)
        ON DELETE NO ACTION
        ON UPDATE CASCADE
);



-- -----------------------------------------------------
-- Table extensions
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS extensions (
    extension_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY (extension_id)
);



-- -----------------------------------------------------
-- Table texture_type_extensions
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS texture_type_extensions (
    texture_type_id INTEGER NOT NULL,
    extension_id INTEGER NOT NULL,
    PRIMARY KEY (texture_type_id, extension_id),
    FOREIGN KEY (texture_type_id)
        REFERENCES texture_types (texture_type_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (extension_id)
        REFERENCES extensions (extension_id)
        ON DELETE NO ACTION
        ON UPDATE CASCADE
);



-- -----------------------------------------------------
-- Table packed_textures
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS packed_textures (
    packed_textures_id INTEGER NOT NULL,
    packing_group_id INTEGER NOT NULL,
    path TEXT NOT NULL,
    channel_r_path TEXT NOT NULL,
    channel_g_path TEXT NOT NULL,
    channel_b_path TEXT NOT NULL,
    channel_a_path TEXT NOT NULL,
    state TEXT NOT NULL,
    date TEXT NOT NULL,
    PRIMARY KEY (packed_textures_id),
    FOREIGN KEY (packing_group_id)
        REFERENCES packing_groups (packing_group_id)
        ON DELETE NO ACTION
        ON UPDATE CASCADE
);



-- -----------------------------------------------------
-- Table imports
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS imports (
    import_id INTEGER NOT NULL,
    packed_textures_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    unreal_project TEXT NOT NULL,
    PRIMARY KEY (import_id),
    FOREIGN KEY (packed_textures_id)
        REFERENCES packed_textures (packed_textures_id)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);
