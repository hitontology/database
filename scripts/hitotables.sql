-- create types for client and databasesystems to use them in an enumerated way
create type client as enum('mobile', 'native', 'web-based');

create type databasesystem as enum('MySQL', 'PostgreSQL');

-- the master table
-- client and databasesystem as arrays because they should be [0..n]
-- inserting new values needs to be like 'VALUES('{"bla","blubb"}')'
create table softwareproduct(
	uri VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL,
	comment text,
	codeRepository VARCHAR(200),
	homepage VARCHAR(200),
	client client [],
	databaseSystem databasesystem []
);
-- the atomic tables mostly filled with dbpedia data
create table programmingLibrary(
	uri VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL
);
create table language(
	uri VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL
);
create table interoperabilityStandard(
	uri VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL
);
create table programmingLanguage(
	uri VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL
);
create table operatingSystem(
	uri VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL
);
create table license(
	uri VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL
);
-- relations from atomics to master
create table swp_has_programmingLibrary(
	swp_uri character varying(200) NOT NULL REFERENCES softwareproduct(uri) ON DELETE CASCADE ON UPDATE CASCADE,
	lib_uri character varying(200) NOT NULL	REFERENCES programmingLibrary(uri) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_uri, lib_uri)
);
create table swp_has_language(
	swp_uri character varying(200) NOT NULL REFERENCES softwareproduct(uri) ON DELETE CASCADE ON UPDATE CASCADE,
	lang_uri character varying(200) NOT NULL	REFERENCES language(uri) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_uri, lang_uri)
);
create table swp_has_interoperabilityStandard(
	swp_uri character varying(200) NOT NULL REFERENCES softwareproduct(uri) ON DELETE CASCADE ON UPDATE CASCADE,
	io_uri character varying(200) NOT NULL	REFERENCES interoperabilityStandard(uri) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_uri, io_uri)
);
create table swp_has_programmingLanguage(
	swp_uri character varying(200) NOT NULL REFERENCES softwareproduct(uri) ON DELETE CASCADE ON UPDATE CASCADE,
	plang_uri character varying(200) NOT NULL	REFERENCES programmingLanguage(uri) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_uri, plang_uri)
);
create table swp_has_operatingSystem(
	swp_uri character varying(200) NOT NULL REFERENCES softwareproduct(uri) ON DELETE CASCADE ON UPDATE CASCADE,
	os_uri character varying(200) NOT NULL	REFERENCES operatingSystem(uri) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_uri, os_uri)
);
create table swp_has_license(
	swp_uri character varying(200) NOT NULL REFERENCES softwareproduct(uri) ON DELETE CASCADE ON UPDATE CASCADE,
	license_uri character varying(200) NOT NULL	REFERENCES license(uri) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_uri, license_uri)
);
