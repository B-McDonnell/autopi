CREATE SCHEMA autopi;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE autopi.user(
	last_login timestamptz NOT NULL DEFAULT NOW(),
	username text PRIMARY KEY
);

CREATE TABLE autopi.raspi(
	device_id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY, 
	hardware_id text,
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

CREATE TABLE autopi.admin(
	username text PRIMARY KEY
);
