-- -----------------------------------------------------
-- Table packed_textures
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS packing_groups (
    packed_textures_id INTEGER NOT NULL,
    path TEXT,
    state TEXT NOT NULL,
    date TEXT NOT NULL,
    size INTEGER,
    channel_r_path TEXT NOT NULL,
    channel_g_path TEXT NOT NULL,
    channel_b_path TEXT NOT NULL,
    channel_a_path TEXT NOT NULL,
    PRIMARY KEY (packed_textures_id),
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
