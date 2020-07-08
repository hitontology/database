import csv
import os
filenames={
    "applicationsystem.csv":"ApplicationSystem",
    "function.csv":"Function",
    "subfeature.csv":"SubFeature",
}
folders=["BbApplicationComponent","BbArchitecture","BbReferenceModel","WhoDhiClient","WhoDhiDataService","WhoDhiHealthcareProvider","WhoDhiHealthSystemManager","WhoDhiSystemCategory"]
#filenames=["applicationsystem.csv","function.csv"]
for folder in folders:
    for filename in filenames:
        if(os.path.isfile(folder+"/"+filename)):
            #order: foldername + csv-Name with CamelCase is the catalogue_suffix
            shortFile=filenames[filename]
            catalogue_suffix=folder+shortFile+"Catalogue"
            outputfile=shortFile
            output=open(folder+"/"+shortFile+".sql", "a+")
            output.write("INSERT INTO classified(suffix,label,catalogue_suffix) VALUES"+'\n')
            with open (folder+"/"+filename) as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                next(readCSV, None)
                for line in readCSV:
                    output.write('(\''+line[1]+'\',\''+line[2]+'\',\''+catalogue_suffix+'\'),\n')

            output.close()
            #truncate last char of the file and replace it with ;
            with open(folder+"/"+shortFile+".sql", 'rb+') as filehandle:
                filehandle.seek(-2, os.SEEK_END)
                filehandle.truncate()
            with open (folder+"/"+shortFile+".sql", "a+") as append:
                append.write(';')
