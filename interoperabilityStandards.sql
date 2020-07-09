-- select ?x, STR(?y), STR(?z), group_concat(?b;separator="','") as ?sources
-- {
-- ?x a hito:Interoperability;
--    rdfs:label ?y;
--    rdfs:comment ?z;
--    <http://purl.org/dc/terms/source> ?b.
-- }

INSERT INTO interoperabilityStandard(suffix,label,comment,sourceuris) VALUES
(),
();
