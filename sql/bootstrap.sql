CREATE EXTENSION IF NOT EXISTS plpgsql;
CREATE EXTENSION IF NOT EXISTS adminpack;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS plpythonu;
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Should be default behavior on postgres >= 8.1
SET default_with_oids = false;


-- System Tables
CREATE TABLE _tracked_table (
    date_created timestamp without time zone DEFAULT NOW() NOT NULL,
    date_modified timestamp without time zone DEFAULT NOW() NOT NULL
);

CREATE TABLE versions (
    from_version integer NOT NULL,
    to_version integer NOT NULL,
    date_migrated timestamp without time zone DEFAULT NOW() NOT NULL
);


-- Model Tables
CREATE TABLE images (
    image_id bigserial PRIMARY KEY,
    cdn_url text NOT NULL
) INHERITS(_tracked_table);


CREATE TABLE users (
    user_id bigserial PRIMARY KEY,
    name text NOT NULL,
    username text NOT NULL,
    password_hash text,
    password_salt text
) INHERITS(_tracked_table);


CREATE TABLE user_images (
    user_id bigint,
    image_id bigint,
    CONSTRAINT user_images_image_id_fkey
        FOREIGN KEY (image_id)
        REFERENCES images(image_id),
    CONSTRAINT user_images_user_id_fkey
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);
