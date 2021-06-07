CREATE SCHEMA autopi;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE autopi.user(
	last_login timestamptz NOT NULL DEFAULT NOW(),
	username text PRIMARY KEY,
	is_admin boolean NOT NULL DEFAULT FALSE
);

CREATE TABLE autopi.raspi(
	device_id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY, 
	hardware_id text,
	registered boolean NOT NULL GENERATED ALWAYS AS (hardware_id IS NOT NULL) STORED,
	ip_addr text,
	alias text,
	updated_at timestamptz NOT NULL DEFAULT NOW(),
	added_at timestamptz NOT NULL DEFAULT NOW(),
	vnc text,
	ssh text,
	power text,
	username text,
	FOREIGN KEY(username) REFERENCES autopi.user(username) ON DELETE CASCADE
);

CREATE TABLE autopi.raspi_warning(
	warning text,
	added_at timestamptz NOT NULL DEFAULT NOW(),
	device_id uuid,
	PRIMARY KEY(device_id, warning),
	FOREIGN KEY(device_id) REFERENCES autopi.raspi(device_id)
);


-- Add trigger to automatically update 'updated_at' in raspi column whenever the row is UPDATE'd.

CREATE OR REPLACE FUNCTION update_user_time() RETURNS TRIGGER
	AS
	$BODY$
	BEGIN
		new.updated_at := NOW();
		RETURN new;
	END;
	$BODY$
	LANGUAGE plpgsql;

CREATE TRIGGER onupdate BEFORE UPDATE ON autopi.raspi FOR EACH ROW EXECUTE PROCEDURE update_user_time();
