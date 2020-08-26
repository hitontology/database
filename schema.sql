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
	CHECK (label <> ''),
	comment text,
	CHECK (comment <> ''),
	codeRepository VARCHAR(200),
	CHECK (codeRepository <> ''),
	homepage VARCHAR(200),
	CHECK (homepage <> ''),
	clients Client [],
	databaseSystems DatabaseSystem [],
	languages Language [],
	licenses License [],
	operatingSystems OperatingSystem [],
	programmingLanguages ProgrammingLanguage [],
--	programmingLibraries ProgrammingLibrary [],
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://hitontology.eu/ontology/' || suffix) STORED
);
create table interoperabilityStandard(
	suffix VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL,
	CHECK (label <> ''),
	comment text,
	sourceuris VARCHAR(200)[],
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://dbpedia.org/resource/' || suffix) STORED
);
-- HITO catalogues as one table with type attribute
create table catalogue(
	suffix VARCHAR(200) PRIMARY KEY,
	label VARCHAR(200) NOT NULL,
	CHECK (label <> ''),
	type CatalogueType NOT NULL,
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
	classified_suffix VARCHAR(200) REFERENCES classified(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	label VARCHAR(200) NOT NULL,
	CHECK (label <> ''),
	comment TEXT,
	CHECK (comment <> ''),
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://hitontology.eu/ontology/' || suffix) STORED
);
-- relations from atomics to master
-- ToDo: check if parent is Feature and child is Feature or function
create table classified_has_child(
	parent_suffix character varying(200) NOT NULL REFERENCES classified(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	child_suffix character varying(200) NOT NULL REFERENCES classified(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (parent_suffix, child_suffix)
);
create table swp_has_interoperabilityStandard(
	swp_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	io_suffix character varying(200) NOT NULL	REFERENCES interoperabilityStandard(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_suffix, io_suffix)
);
-- ToDo: how to avoid circular reference? It would be complicated and of high cost to implement sth like a recursive query-monster, that points out the paths and checks if something is there twice. 
-- I think the data are structured enough so we don't need this feature. For the stability of the db it has also no effect.
create table swp_has_child(
	parent_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	child_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (parent_suffix, child_suffix)
);
