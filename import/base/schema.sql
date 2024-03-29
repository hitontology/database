-- Caution!!
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
-- create types for client and databasesystems to use them in an enumerated way
create table client(suffix VARCHAR(8) PRIMARY KEY, label VARCHAR(20) NOT NULL);
insert into client(suffix,label) values ('Mobile','Mobile'), ('Native','Native'), ('WebBased','Web Based');

create table databasesystem(suffix VARCHAR(20) PRIMARY KEY, label VARCHAR(20) NOT NULL);
insert into databasesystem(suffix,label) values ('MySql','MySQL'), ('PostgreSql','PostgreSQL'), ('IbmDb2','IBM DB2'), ('MariaDb','MariaDB'), ('MicrosoftSqlServer','Microsoft SQL Server'), ('MongoDb','MongoDB'), ('OracleDatabase','Oracle Database'), ('SapHana','SAP HANA'), ('TinyDb', 'TinyDB'), ('SQLite','SQLite');

create type cataloguetype as enum('UserGroup', 'ApplicationSystemType', 'Feature', 'EnterpriseFunction', 'OrganizationalUnit','OutcomeCriteria');

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
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://hitontology.eu/ontology/' || suffix) STORED
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
	n VARCHAR(20),
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
	type cataloguetype NOT NULL,
	uri VARCHAR(229) GENERATED ALWAYS AS ('http://hitontology.eu/ontology/' || suffix) STORED
);
-- relations from atomics to master
create table citation_has_classified(
	citation_suffix character varying(200) NOT NULL REFERENCES citation(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	classified_suffix character varying(200) NOT NULL REFERENCES classified(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (citation_suffix, classified_suffix)
);

CREATE FUNCTION typeCheck() RETURNS trigger AS $typeCheck$
DECLARE citation_type cataloguetype;
DECLARE classified_type cataloguetype;
DECLARE catalogue_suffix catalogue.suffix%type;
BEGIN
  SELECT type INTO citation_type FROM citation WHERE suffix = NEW.citation_suffix;

  SELECT catalogue.suffix, catalogue.type INTO catalogue_suffix, classified_type
  FROM classified INNER JOIN catalogue
  ON classified.catalogue_suffix = catalogue.suffix
  WHERE classified.suffix = NEW.classified_suffix;

  IF citation_type != classified_type THEN
    RAISE EXCEPTION 'Citation % has type % but it`s classified % is in catalogue % with type %.', NEW.citation_suffix, citation_type, NEW.classified_suffix, catalogue_suffix, classified_type;
  END IF;

   RETURN NEW; -- result is used, since it is a row-level BEFORE trigger
END;
$typeCheck$ LANGUAGE plpgsql;

CREATE TRIGGER typeCheck BEFORE INSERT OR UPDATE ON citation_has_classified FOR EACH ROW EXECUTE PROCEDURE typeCheck();

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
	db_suffix character varying(20) NOT NULL REFERENCES databasesystem(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_suffix, db_suffix)
);
-- direct connection between software product and classified
create table swp_has_classified(
	swp_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	classified_suffix character varying(200) NOT NULL REFERENCES classified(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (swp_suffix, classified_suffix)
);
create table feature_supports_function(
	feature_suffix character varying(200) NOT NULL REFERENCES citation(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	function_suffix character varying(200) NOT NULL REFERENCES citation(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	source VARCHAR(200),
	PRIMARY KEY (feature_suffix, function_suffix)
);

DROP FUNCTION IF EXISTS featureFunctionCheck CASCADE;
CREATE FUNCTION featureFunctionCheck() RETURNS trigger AS $featureFunctionCheck$
DECLARE feature_type cataloguetype;
DECLARE function_type cataloguetype;
BEGIN

  SELECT
  feature.type, function.type INTO feature_type, function_type
  FROM feature_supports_function
  JOIN citation feature ON feature.suffix=feature_supports_function.feature_suffix
  JOIN citation function ON function.suffix=feature_supports_function.function_suffix;

  IF feature_type != 'Feature' THEN
    RAISE EXCEPTION 'Citation % has type % but it should be a feature in entry (%,%) of table feature_supports_function .', NEW.feature_suffix, feature_type, NEW.feature_suffix, NEW.function_suffix;
  END IF;

  IF function_type != 'EnterpriseFunction' THEN
    RAISE EXCEPTION 'Citation % has type % but it should be a function in entry (%,%) of table feature_supports_function .', NEW.function_suffix, function_type, NEW.feature_suffix, NEW.function_suffix;
  END IF;

   RETURN NEW; -- result is used, since it is a row-level BEFORE trigger
END;
$featureFunctionCheck$ LANGUAGE plpgsql;
CREATE TRIGGER featureFunctionCheck BEFORE INSERT OR UPDATE ON feature_supports_function FOR EACH ROW EXECUTE PROCEDURE featureFunctionCheck();


-- ToDo: how to avoid circular reference? It would be complicated and of high cost to implement sth like a recursive query-monster, that points out the paths and checks if something is there twice.
-- I think the data are structured enough so we don't need this feature. For the stability of the db it has also no effect.
create table swp_has_child(
	parent_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	child_suffix character varying(200) NOT NULL REFERENCES softwareproduct(suffix) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (parent_suffix, child_suffix)
);

CREATE TABLE rdf_property(
	type cataloguetype NOT NULL,
	swp_citation VARCHAR(20) NOT NULL,
	swp_classified VARCHAR(20) NOT NULL,
	citation_classified VARCHAR(20) NOT NULL,
	PRIMARY KEY (type)
);

INSERT INTO rdf_property(type,swp_citation,swp_classified,citation_classified) values
('UserGroup',				'spUsedByUserCit',	'spUsedByUserCla',	'userCitClassifiedAs'),
('ApplicationSystemType',	'spIsOfAstCit',		'astIsOfAstCla',	'astCitClassifiedAs'),
('Feature',					'spOffersFCit',		'spOffersFCla',		'fCitClassifiedAs'),
('EnterpriseFunction',		'spSupportsEfCit',	'spSupportsEfCla',	'efCitClassifiedAs'),
('OrganizationalUnit',		'spUsedInOuCit',	'spUsedInOuCla',	'ouCitClassifiedAs');

CREATE VIEW classified_type AS
SELECT classified.suffix, catalogue.type
FROM classified RIGHT JOIN catalogue
ON classified.catalogue_suffix = catalogue.suffix;

-- seems to be unused by export
CREATE VIEW citation_has_classified_type AS
SELECT citation_has_classified.citation_suffix,
       citation_has_classified.classified_suffix,
       citation.type,
       'http://hitontology.eu/ontology/' || rdf_property.citation_classified AS property
FROM		citation
INNER JOIN	citation_has_classified
ON			citation.suffix = citation_has_classified.citation_suffix
INNER JOIN	rdf_property
ON			citation.type = rdf_property.type;

CREATE VIEW swp_citation_rdf AS
SELECT 'http://hitontology.eu/ontology/' || citation.swp_suffix AS subject,
       'http://hitontology.eu/ontology/' || rdf_property.swp_citation AS predicate,
       citation.uri AS object
FROM		citation
INNER JOIN	rdf_property
ON			citation.type = rdf_property.type;

-- Assumes that all classifieds in that table are features
CREATE VIEW swp_classified_rdf AS
SELECT 'http://hitontology.eu/ontology/' || swp_has_classified.swp_suffix AS subject,
       'http://hitontology.eu/ontology/' || rdf_property.swp_classified  AS predicate,
       'http://hitontology.eu/ontology/' || swp_has_classified.classified_suffix AS object
FROM		swp_has_classified
INNER JOIN	classified_type
ON			swp_has_classified.classified_suffix = classified_type.suffix
INNER JOIN	rdf_property
ON			classified_type.type = rdf_property.type;

CREATE VIEW citation_classified_rdf AS
SELECT citation.uri AS subject,
       'http://hitontology.eu/ontology/' || rdf_property.citation_classified AS predicate,
       'http://hitontology.eu/ontology/' || citation_has_classified.classified_suffix AS object                                       
FROM		citation
INNER JOIN	citation_has_classified 
ON			citation.suffix = citation_has_classified.citation_suffix
INNER JOIN	rdf_property
ON			citation.type = rdf_property.type;

CREATE VIEW classified_has_child_type AS
SELECT
child.suffix as child_suffix,
child.type AS child_type,
parent.suffix as parent_suffix,
parent.type AS parent_type
FROM classified_has_child
JOIN classified_type child ON classified_has_child.child_suffix=child.suffix
JOIN classified_type parent ON classified_has_child.parent_suffix=parent.suffix;

