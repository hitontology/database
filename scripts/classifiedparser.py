import pandas
import os
filenames={
#    "applicationsystem.csv":"ApplicationSystem",
    "function.csv":"Function",
#    "subfeature.csv":"SubFeature",
}
#folders=["BbApplicationComponent","BbArchitecture","BbReferenceModel","WhoDhiClient","WhoDhiDataService","WhoDhiHealthcareProvider","WhoDhiHealthSystemManager","WhoDhiSystemCategory"]
folders=["BbArchitecture"]
#filenames=["applicationsystem.csv","function.csv"]
#filenames=["function.csv"]
for folder in folders:
    for filename in filenames:
        inPath = folder+"/"+filename;
        if(os.path.isfile(inPath)):
            #order: foldername + csv-Name with CamelCase is the catalogue_suffix
            catalogueType=filenames[filename]
            catalogue_suffix=folder+catalogueType+"Catalogue"
            outputfile=catalogueType
            output=open(folder+"/"+catalogueType+".sql", "a+")
            output.write("INSERT INTO classified(suffix,n,label,comment,synonyms,catalogue_suffix) VALUES"+'\n')

            df = pandas.read_csv(inPath)
            print(df)
            for index, row in df.iterrows():
               
                quotedN = "NULL"
                if "n" in row:
                    quotedN = "'"+str(row["n"])+"'"
                
                quotedComment = "NULL"
                if "comment" in row:
                    quotedComment = "'"+row["comment"]+"'"
                synonyms = []
                if "synonyms" in row:
                    synonyms = row["synonyms"].split(";")
                
                synonymString = ",".join(map(lambda x: '"'+x+'"', synonyms)) 

                print(f"('{row['uri']}',{quotedN},'{row['en']}',{quotedComment},'{{{synonymString}}}','{catalogue_suffix}'),\n")
#                output.write( '(\''+line[1]+'\',\''+line[0]+'\',\''+catalogue_suffix+'\'),\n')
            #     #print(line)
            # output.close()
            # #truncate last char of the file and replace it with ;
            # with open(folder+"/"+catalogueType+".sql", 'rb+') as filehandle:
            #     filehandle.seek(-2, os.SEEK_END)
            #     filehandle.truncate()
            # with open (folder+"/"+catalogueType+".sql", "a+") as append:
            #     append.write(';')
