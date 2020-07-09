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
('BbApplicationComponentApplicationSystemCatalogue','Blue Book Application Components','ApplicationSystem'),
('BbArchitectureApplicationSystemCatalogue','Blue Book Architecture Application System Catalogue','ApplicationSystem'),
('BbArchitectureFeatureCatalogue','Blue Book Architecture Feature Catalogue','Feature'),
('WhoDhiHealthSystemManagerFunctionCatalogue','Health System Managers Function Catalogue','EnterpriseFunction'),
('WhoDhiHealthcareProviderFunctionCatalogue','Healthcare Provider Function Catalogue','EnterpriseFunction'),
-- ('UnknownOrganizationalUnitCatalogue','Unknown Organizational Unit Catalogue','OrganizationalUnit'),
-- ('UnknownUserGroupCatalogue','Unknown User Group Catalogue','UserGroup'),
('SnomedEnvironmentOrganizationalUnitCatalogue','SNOMED CT Environment Client Feature Catalogue','OrganizationalUnit'),
('SnomedUserGroupCatalogue','SNOMED CT User Group Catalogue','UserGroup'),
('BbReferenceModelFunctionCatalogue','Blue Book Reference Model Function Catalogue','EnterpriseFunction'),
-- ('UnknownFunctionCatalogue','Unknown Enterprise Function Catalogue','EnterpriseFunction'),
('BbArchitectureFunctionCatalogue','Blue Book Architecture Function Catalogue','EnterpriseFunction');
