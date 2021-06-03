CREATE SCHEMA autopi;

CREATE TABLE autopi.user(
	last_login timestamptz NOT NULL,
	username text PRIMARY KEY
);

CREATE TABLE autopi.raspi(
	device_id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY, 
	hardware_id text,
	ip_addr text,
	updated_at timestamptz,
	added_at timestamptz NOT NULL,
	vnc text,
	ssh text,
	power text,
	username text,
	FOREIGN KEY(username) REFERENCES autopi.user(username)
);

CREATE TABLE autopi.raspi_warning(
	warning text,
	added_at timestamptz NOT NULL,
	device_id text,
	PRIMARY KEY(device_id, warning),
	FOREIGN KEY(device_id) REFERENCES autopi.raspi(device_id)
);

CREATE TABLE autopi.admin(
	username text PRIMARY KEY
);
	
	
	
	
	
