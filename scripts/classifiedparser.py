import pandas
import os
import sys
import errno
import numpy 

filenames={
    "applicationsystem.csv":"ApplicationSystem",
    "function.csv":"Function",
    "feature.csv":"Feature",
    "subfeature.csv":"SubFeature",
}
folders=["Bb","WhoDhiClient","WhoDhiDataService","WhoDhiHealthcareProvider","WhoDhiHealthSystemManager","WhoDhiSystemCategory"]
outputBase = "catalogue"
try:
    os.makedirs(outputBase)
except OSError as e:
    if e.errno != errno.EEXIST:
            raise  # raises the error again

def has(row,column):
    return column in row and not (pandas.isna(row[column]))

def quote(row,column):
    if has(row,column):
        return  "E'"+str(row[column]).replace("'","\\'")+"'" # escape single quotes, add quotes for SQL
    else:
        return "NULL"

def quoteArray(row,column):
    if has(row,column):
        return "'{" + ",".join(map(lambda v: '"'+v.strip()+'"', row[column].split(";")))  + "}'"
    else:
        return "'{}'" 


inputBase = sys.argv[1]
for folder in folders:
    for filename in filenames:
        inputPath = inputBase +"/" + folder+"/"+filename
        if(os.path.isfile(inputPath)):
            #order: foldername + csv-Name with CamelCase is the catalogue_suffix
            catalogueType=filenames[filename]
            catalogue_suffix=folder+catalogueType.replace("Sub","")+"Catalogue" # sub catalogue is the same as the main one
            outPath = outputBase + "/"+ folder+catalogueType+".sql";
            output=open(outPath, "w")
            content = f"\echo Importing {catalogue_suffix} from {filename} \n"
            content += "INSERT INTO classified(suffix,catalogue_suffix,n,label,comment,synonyms,dct_source,dce_sources) VALUES \n";

            df = pandas.read_csv(inputPath)
            print("Transforming ",inputPath,df.shape)
            rows = list(map(lambda index_row: index_row[1], df.iterrows())) # persists the rows for multiple uses

            classifiedLines = map(lambda row:
                                f"('{row['uri']}','{catalogue_suffix}',{quote(row,'n')},{quote(row,'en')},{quote(row,'comment')},{quoteArray(row,'synonyms')},{quote(row,'dctsource')},{quoteArray(row,'dcesource')})",
                                rows) 
            content += ",\n".join(classifiedLines)
            content += ";\n"

            superRows = list(filter(lambda row: has(row,"super"), rows))
            if(len(superRows)>0):
                content += f"INSERT INTO classified_has_child(parent_suffix,child_suffix) VALUES \n";
                superLines = map(lambda row:
                                ",\n".join( # flatten
                                    map(lambda super:
                                        f"('{super}','{row['uri']}')",
                                        row['super'].split(";"))),
                                    rows)
            
                content += ",\n".join(superLines)
                content +=";"

            output.write(content)
            output.close()

