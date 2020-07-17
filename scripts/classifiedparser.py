import pandas
import os
import sys
import errno
import numpy 

filenames={
    "applicationsystem.csv":"ApplicationSystem",
    "function.csv":"Function",
    "feature.csv":"Feature",
    "subfeature.csv":"Feature",
}
folders=["Bb","WhoDhiClient","WhoDhiDataService","WhoDhiHealthcareProvider","WhoDhiHealthSystemManager","WhoDhiSystemCategory"]
outputBase = "catalogue"


def quote(row,column):
    if (not column in row) or (pandas.isna(row[column])):
        return "NULL" 
    return "E'"+str(row[column]).replace("'","\\'")+"'" # escape single quotes, add quotes for SQL

def quoteArray(row,column):
    if (not column in row) or (pandas.isna(row[column])):
        return "'{}'" 
    return "'{" + ",".join(map(lambda v: '"'+v.strip()+'"', row[column].split(";")))  + "}'"


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
            output.write("INSERT INTO classified(suffix,catalogue_suffix,n,label,comment,synonyms,dct_source,dce_sources) VALUES"+'\n')

            df = pandas.read_csv(inputPath)
            print("Transforming ",inputPath,df.shape)
            for index, row in df.iterrows():
                synonyms = []              
                if ("synonyms" in row) and (not pandas.isna(row["synonyms"])):
                    synonyms = row["synonyms"].split(";")
                synonymString = ",".join(map(lambda x: '"'+x+'"', synonyms))

                line = f"('{row['uri']}','{catalogue_suffix}',{quote(row,'n')},{quote(row,'en')},{quote(row,'comment')},{quoteArray(row,'synonyms')},{quoteArray(row,'dctsource')},{quoteArray(row,'dcesource')}),"
                output.write(line+"\n")
            output.close()
                #truncate last char of the file and replace it with ;
            with open(outPath, 'rb+') as filehandle:
                filehandle.seek(-2, os.SEEK_END)
                filehandle.truncate()
            with open (outPath, "a+") as append:
                append.write(';')
