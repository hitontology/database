-- Caution!!
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
-- create types for client and databasesystems to use them in an enumerated way
create table client(suffix VARCHAR(8) PRIMARY KEY);
insert into client(suffix) values ('Mobile'), ('Native'), ('WebBased');

create table databasesystem(suffix VARCHAR(10) PRIMARY KEY);
insert into databasesystem(suffix ) values ('MySql'), ('PostgreSql');

--create table cataloguetype(suffix VARCHAR(19) PRIMARY KEY);
-- insert into table cataloguetype(suffix) values ('UserGroup'), ('ApplicationSystem'), ('Feature'), ('EnterpriseFunction'), ('OrganizationalUnit');  
create type cataloguetype as enum('UserGroup', 'ApplicationSystem', 'Feature', 'EnterpriseFunction', 'OrganizationalUnit');

-- the main table
-- client and databasesystem as arrays because they should be [0..n]
-- inserting new values needs to be like 'VALUES('{"bla","blubb"}')'
create table softwareproduct(
	suffix VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL,
	CHECK (label <> ''),
	comment text,
	CHECK (comment <> ''),
	coderepository VARCHAR(200),
	CHECK (coderepository <> ''),
	homepage VARCHAR(200),
	CHECK (homepage <> ''),
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://hitontology.eu/ontology/' || suffix) STORED
);

-- the atomic tables mostly filled with dbpedia data
create table programminglibrary(
	suffix VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL,
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://dbpedia.org/resource/' || suffix) STORED
);
create table language(
	suffix VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL,
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://dbpedia.org/resource/' || suffix) STORED
);
create table interoperabilitystandard(
	suffix VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL,
	CHECK (label <> ''),
	comment text,
	sourceuris VARCHAR(200)[],
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://dbpedia.org/resource/' || suffix) STORED
);
create table programminglanguage(
	suffix VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL,
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://dbpedia.org/resource/' || suffix) STORED
);
create table operatingsystem(
	suffix VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL,
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://dbpedia.org/resource/' || suffix) STORED
);
create table license(
	suffix VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL,
	uri VARCHAR(233) GENERATED ALWAYS AS ('http://www.ebi.ac.uk/swo/license/' || suffix) STORED
);
-- HITO catalogues as one table with type attribute
create table catalogue(
	suffix VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL,
	CHECK (label <> ''),
	type cataloguetype NOT NULL,
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://hitontology.eu/ontology/' || suffix) STORED
);
create table classified(
	suffix VARCHAR(200) PRIMARY KEY,
	catalogue_suffix VARCHAR(200) NOT NULL REFERENCES catalogue(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	n VARCHAR(10),
	label VARCHAR(200) NOT NULL,
	CHECK (label <> ''),
	comment TEXT,
	CHECK (comment <> ''),
	synonyms VARCHAR(200)[],
	dct_source VARCHAR(200),
	dce_sources VARCHAR(200)[],
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://hitontology.eu/ontology/' || suffix) STORED
);
create table citation(
	suffix VARCHAR(200) PRIMARY KEY,
	swp_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	label VARCHAR(200) NOT NULL,
	CHECK (label <> ''),
	comment TEXT,
	CHECK (comment <> ''),
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://hitontology.eu/ontology/' || suffix) STORED
);
-- relations from atomics to master
create table citation_has_classified(
	citation_suffix character varying(200) NOT NULL REFERENCES citation(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	classified_suffix character varying(200) NOT NULL REFERENCES classified(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (citation_suffix, classified_suffix)
);
-- ToDo: check if parent is Feature and child is Feature or function
create table classified_has_child(
	parent_suffix character varying(200) NOT NULL REFERENCES classified(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	child_suffix character varying(200) NOT NULL REFERENCES classified(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (parent_suffix, child_suffix)
);
create table swp_has_programminglibrary(
	swp_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	lib_suffix character varying(200) NOT NULL	REFERENCES programminglibrary(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_suffix, lib_suffix)
);
create table swp_has_language(
	swp_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	lang_suffix character varying(200) NOT NULL	REFERENCES language(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_suffix, lang_suffix)
);
create table swp_has_interoperabilitystandard(
	swp_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	io_suffix character varying(200) NOT NULL	REFERENCES interoperabilitystandard(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_suffix, io_suffix)
);
create table swp_has_programminglanguage(
	swp_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	plang_suffix character varying(200) NOT NULL	REFERENCES programminglanguage(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_suffix, plang_suffix)
);
create table swp_has_operatingsystem(
	swp_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	os_suffix character varying(200) NOT NULL	REFERENCES operatingsystem(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_suffix, os_suffix)
);
create table swp_has_license(
	swp_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	license_suffix character varying(200) NOT NULL	REFERENCES license(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_suffix, license_suffix)
);
create table swp_has_client(
	swp_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	client_suffix character varying(8) NOT NULL REFERENCES client(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_suffix, client_suffix)
);
create table swp_has_databasesystem(
	swp_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	db_suffix character varying(10) NOT NULL REFERENCES databasesystem(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_suffix, db_suffix)
);
-- ToDo: how to avoid circular reference? It would be complicated and of high cost to implement sth like a recursive query-monster, that points out the paths and checks if something is there twice. 
-- I think the data are structured enough so we don't need this feature. For the stability of the db it has also no effect.
create table swp_has_child(
	parent_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	child_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (parent_suffix, child_suffix)
);
