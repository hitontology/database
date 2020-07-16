import pandas
import os
import sys
import errno
import numpy 

filenames={
    "applicationsystem.csv":"ApplicationSystem",
    "function.csv":"Function",
    "feature.csv":"Feature",
}
folders=["BbApplicationComponent","BbArchitecture","BbReferenceModel","WhoDhiClient","WhoDhiDataService","WhoDhiHealthcareProvider","WhoDhiHealthSystemManager","WhoDhiSystemCategory"]
outputBase = "catalogue"
#folders=["BbArchitecture","BbApplicationComponent","BbReferenceModel","WhoDhiClient"]
#filenames=["applicationsystem.csv","function.csv"]
#filenames=["function.csv"]

def quote(s):
    return "E'"+s.replace("'","\\'")+"'" # escape single quotes, add quotes for SQL

inputBase = sys.argv[1]
for folder in folders:
    for filename in filenames:
        inputPath = inputBase +"/" + folder+"/"+filename
        if(os.path.isfile(inputPath)):
            #order: foldername + csv-Name with CamelCase is the catalogue_suffix
            catalogueType=filenames[filename]
            catalogue_suffix=folder+catalogueType+"Catalogue"
            try:
                os.makedirs(outputBase)
            except OSError as e:
                if e.errno != errno.EEXIST:
                        raise  # raises the error again
            outPath = outputBase + "/"+ folder+catalogueType+".sql";
            output=open(outPath, "w")
            output.write("INSERT INTO classified(suffix,n,label,comment,synonyms,catalogue_suffix) VALUES"+'\n')

            df = pandas.read_csv(inputPath)
            print("Transforming ",inputPath,df.shape)
            for index, row in df.iterrows():

                quotedN = "NULL"
                if "n" in row:
                    quotedN = quote(str(row["n"]))

                quotedComment = "NULL"
                if ("comment" in row) and (not pandas.isna(row["comment"])):
                    quotedComment = quote(row["comment"])
                synonyms = []
                if ("synonyms" in row) and (not pandas.isna(row["synonyms"])):
                    synonyms = row["synonyms"].split(";")

                synonymString = ",".join(map(lambda x: '"'+x+'"', synonyms))

                line = f"('{row['uri']}',{quotedN},{quote(row['en'])},{quotedComment},'{{{synonymString}}}','{catalogue_suffix}'),"
                output.write(line+"\n")
            output.close()
                #truncate last char of the file and replace it with ;
            with open(outPath, 'rb+') as filehandle:
                filehandle.seek(-2, os.SEEK_END)
                filehandle.truncate()
            with open (outPath, "a+") as append:
                append.write(';')
