-- select ?x STR(?y) REPLACE(STR(?b),' ','')
-- {
-- ?x a [rdfs:subClassOf hito:Catalogue].
-- ?x rdfs:label ?y.
-- ?x a ?z.
-- ?z rdfs:label ?b.
-- }

INSERT INTO catalogue(suffix,label,type)VALUES
('WhoDhiClientFeatureCatalogue','Client Feature Catalogue','Feature'),
('WhoDhiDataServiceFeatureCatalogue','Data Service Feature Catalogue','Feature'),
('WhoDhiHealthSystemManagerFeatureCatalogue','Health System Managers Feature Catalogue','Feature'),
('WhoDhiHealthcareProviderFeatureCatalogue','Healthcare Provider Feature Catalogue','Feature'),
('WhoDhiSystemCategoryApplicationSystemCatalogue','System Categories','ApplicationSystem'),
-- ('UnknownFeatureCatalogue','Unknown Feature Catalogue','Feature'),
-- ('UnknownApplicationSystemCatalogue','Unknown Application System Catalogue','ApplicationSystem'),
('Dickinson','Dickinson G, Ritter J, Stevens-Love H, Dyke P Van. ISO/HL7 10781 - Electronic Health Record System Functional Model, Release 2. 2014.','Feature'),
('BbApplicationSystemCatalogue','Blue Book Application Components','ApplicationSystem'),
('BbFeatureCatalogue','Blue Book Feature Catalogue','Feature'),
('BbFunctionCatalogue','Blue Book Function Catalogue','EnterpriseFunction'),
('WhoDhiHealthSystemManagerFunctionCatalogue','Health System Managers Function Catalogue','EnterpriseFunction'),
('WhoDhiHealthcareProviderFunctionCatalogue','Healthcare Provider Function Catalogue','EnterpriseFunction'),
-- ('UnknownOrganizationalUnitCatalogue','Unknown Organizational Unit Catalogue','OrganizationalUnit'),
-- ('UnknownUserGroupCatalogue','Unknown User Group Catalogue','UserGroup'),
('SnomedEnvironmentOrganizationalUnitCatalogue','SNOMED CT Environment Client Feature Catalogue','OrganizationalUnit'),
-- ('UnknownFunctionCatalogue','Unknown Enterprise Function Catalogue','EnterpriseFunction'),
('SnomedUserGroupCatalogue','SNOMED CT User Group Catalogue','UserGroup');
