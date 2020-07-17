-- Caution!!
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
-- create types for client and databasesystems to use them in an enumerated way
create type Client as enum('Mobile', 'Native', 'WebBased');
create type DatabaseSystem as enum('MySql', 'PostgreSql');
create type CatalogueType as enum('UserGroup', 'ApplicationSystem', 'Feature', 'EnterpriseFunction', 'OrganizationalUnit');

-- the main table
-- client and databasesystem as arrays because they should be [0..n]
-- inserting new values needs to be like 'VALUES('{"bla","blubb"}')'
create table softwareProduct(
	suffix VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL,
	comment text,
	codeRepository VARCHAR(200),
	homepage VARCHAR(200),
	clients Client [],
	databaseSystems DatabaseSystem [],
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://hitontology.eu/ontology/' || suffix) STORED
);

-- the atomic tables mostly filled with dbpedia data
create table programmingLibrary(
	suffix VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL,
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://dbpedia.org/resource/' || suffix) STORED
);
create table language(
	suffix VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL,
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://dbpedia.org/resource/' || suffix) STORED
);
create table interoperabilityStandard(
	suffix VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL,
	comment text,
	sourceuris VARCHAR(200)[],
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://dbpedia.org/resource/' || suffix) STORED
);
create table programmingLanguage(
	suffix VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL,
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://dbpedia.org/resource/' || suffix) STORED
);
create table operatingSystem(
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
	type CatalogueType NOT NULL,
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://hitontology.eu/ontology/' || suffix) STORED
);
create table classified(
	suffix VARCHAR(200) PRIMARY KEY,
	catalogue_suffix VARCHAR(200) NOT NULL REFERENCES catalogue(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	n VARCHAR(10),
	label VARCHAR(200) NOT NULL,
	comment TEXT,
	synonyms VARCHAR(200)[],
	dct_source VARCHAR(200),
	dce_sources VARCHAR(200)[],
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://hitontology.eu/ontology/' || suffix) STORED
);
create table citation(
	suffix VARCHAR(200) PRIMARY KEY,
	swp_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	classified_suffix VARCHAR(200) NOT NULL REFERENCES classified(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	label VARCHAR(200) NOT NULL,
	comment TEXT,
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://hitontology.eu/ontology/' || suffix) STORED
);
-- relations from atomics to master
-- ToDo: check if parent is Feature and child is Feature or function
create table classified_has_child(
	parent_suffix character varying(200) NOT NULL REFERENCES classified(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	child_suffix character varying(200) NOT NULL REFERENCES classified(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (parent_suffix, child_suffix)
);
create table swp_has_programmingLibrary(
	swp_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	lib_suffix character varying(200) NOT NULL	REFERENCES programmingLibrary(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_suffix, lib_suffix)
);
create table swp_has_language(
	swp_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	lang_suffix character varying(200) NOT NULL	REFERENCES language(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_suffix, lang_suffix)
);
create table swp_has_interoperabilityStandard(
	swp_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	io_suffix character varying(200) NOT NULL	REFERENCES interoperabilityStandard(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_suffix, io_suffix)
);
create table swp_has_programmingLanguage(
	swp_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	plang_suffix character varying(200) NOT NULL	REFERENCES programmingLanguage(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_suffix, plang_suffix)
);
create table swp_has_operatingSystem(
	swp_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	os_suffix character varying(200) NOT NULL	REFERENCES operatingSystem(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_suffix, os_suffix)
);
create table swp_has_license(
	swp_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	license_suffix character varying(200) NOT NULL	REFERENCES license(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_suffix, license_suffix)
);
-- ToDo: how to avoid circular reference? It would be complicated and of high cost to implement sth like a recursive query-monster, that points out the paths and checks if something is there twice. 
-- I think the data are structured enough so we don't need this feature. For the stability of the db it has also no effect.
create table swp_has_child(
	parent_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	child_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (parent_suffix, child_suffix)
);
