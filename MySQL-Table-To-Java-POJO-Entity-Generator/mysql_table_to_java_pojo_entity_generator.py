#!/usr/bin/python
import sys; 
import getopt; 
import MySQLdb; 

def printHelp():
    print "\nThis script creates a Java POJO Entity class corresponding to a MySQL table."; 
    print "A Java file with member variables with appropriate hibernate (persistence) annotations" \
        +" as well as getters and setters is created when MySQL connection details" \
        +" and DB name and table is specified."; 
    print "\nThis assumes that table names and column names follow one of the following two naming conventions" \
        +" (or a combination of them):"; 
    print "1. Camel Case."
        #+'(Capitalization of the first letter of a new word\'s beginning,' \
        #+' all other letters being lower case.' \
        #+' Also, the first letter of the column name or table name is also lower case.)\n'; 
    print "2. Underscore.";  
    print "\nA sample run of this python file is \n"; 
    print "\"python mysql_table_to_java_pojo_entity_generator.py -d ~/Desktop/temp/ " \
        + "-o RulePermission -u root -p P@ssw0rd@123 -l 127.0.0.1 -n ez_pbac " \
        + "-t ez_profiling_rule_permission -k com.ezdi.pbac.service.ezcac.entities\"\n\n"; 
    print "The input options are explained below."; 
    print "-l : The DB Host to connect to."; 
    print "-u : The DB user to user."; 
    print "-p : The DB password to be used."; 
    print "-n : The name of the database to use."; 
    print "-t : The name of the table in the database whose Java Persistence POJO Entity has to be created."; 
    print "-o : The Java Class name to be used while creating the Java file."; 
    print "-d : The directory where the Java file has to be created. " \
        +"NOTE: Make sure there is a \"/\" suffixed at the end of the path specified."; 
    print "-k : The package name to be used in the Java file."; 
    print "-h : Prints out description and usage of this script."; 

def getJavaType(mysqlType):
    if mysqlType.startswith("int"):
        return "Integer"; 
    elif mysqlType.startswith("varchar"):
        return "String"; 
    elif mysqlType.startswith("datetime"):
        return "Date"; 
    elif mysqlType.startswith("mediumint"):
        return "Integer"; 
    elif mysqlType.startswith("tinyint"):
        return "Integer"; 
    elif mysqlType.startswith("smallint"):
        return "Integer"; 
    elif mysqlType.startswith("bigint"):
        return "Long"; 

def convertToCamelCase(str, isFirstLetterUpperCase=False):
    if(str.find("_") != -1):
        ret = ""; 
        words = str.split("_"); 
        for word in words:
            ret = ret+word.capitalize(); 
        if(isFirstLetterUpperCase != True):
            return ret[0].lower()+ret[1:]; 
        else:
            return ret; 
    else:
        return str; 

def convertToCamelCase1(str, isFirstLetterUpperCase=False):
    if(str.find("_") != -1):
        ret = string.capwords(str,"_"); 
        if(isFirstLetterUpperCase != True):
            return ret[0].lower()+ret[1:]; 
        else:
            return ret; 
    else:
        return str; 

def initialLines(fw, package):
    fw.write("package "+package+";\n\n"
        + "import java.util.Date;\n" \
        + "import javax.persistence.Column;\n" \
        + "import javax.persistence.Entity;\n" \
        + "import javax.persistence.Id;\n" \
        + "import javax.persistence.Table;\n" \
    ); 

def initialAnnotationsAndClassName(fw, dbTableName, javaClassName):
    fw.write("\n" \
        + "@Entity\n" \
        + "@Table(name=\""+dbTableName+"\")\n" \
        +"public class "+javaClassName+" {\n" \
    ); 

def addMemberVariables(fw, dbTableColumnDescList):
    for col in dbTableColumnDescList:
        if(col[3] == "PRI"):
            fw.write("\n\t@Id"); 
        fw.write("\n\t@Column(name=\""+col[0]+"\")\n"); 
        name = convertToCamelCase(col[0]); 
        varType = getJavaType(col[1]); 
        fw.write("\tprivate "+varType+" "+name+" ;\n"); 

def getMemberVariables(dbTableColumnDescList):
    elem = []; 
    ret = []; 
    count=0; 
    for col in dbTableColumnDescList:
        name = convertToCamelCase(col[0]); 
        varType = getJavaType(col[1]); 
        elem[0] = name; 
        elem[1] = varType; 
        elem[2] = ""; 
        if(col[3] == "PRI"):
            elem[2] = "PRI"; 
        ret[count] = elem; 
        count = count+1; 
    return ret; 

def addSetter(fw, varName, varType, setterName):
    fw.write("\n\tpublic void "+setterName+"("+varType+" "+varName+"){\n"); 
    fw.write("\t\tthis."+varName+" = "+varName+" ; \n"); 
    fw.write("\t}\n"); 

def addGetter(fw, varName, varType, getterName):
    fw.write("\n\tpublic "+varType+" "+getterName+"(){\n"); 
    fw.write("\t\treturn this."+varName+" ; \n"); 
    fw.write("\t}\n"); 

def addGettersAndSetters(fw, dbTableColumnDescList):
    for col in dbTableColumnDescList:
        varName = convertToCamelCase(col[0]); 
        partMethodName = convertToCamelCase(col[0]); 
        partMethodName = partMethodName[0].upper()+partMethodName[1:]; 
        setterName = "set"+partMethodName; 
        getterName = "get"+partMethodName; 
        varType = getJavaType(col[1]); 
        addSetter(fw, varName, varType, setterName); 
        addGetter(fw, varName, varType, getterName); 
        

def endLines(fw):
    fw.write("\n}\n"); 

################ MAIN #####################

dbUser = "default"; 
dbPwd = "default"; 
dbUrl = "localhost"; 
dbName = "default"; 
dbTable = "default"; 
outputJavaClass = "Default"; 
package = "default"
outputDir = "./"; 

try:
    opts, args = getopt.getopt(sys.argv[1:],"hu:d:p:l:n:t:o:d:k:"); 
except getopt.GetoptError:
	print 'SOMETHING WENT WRONG WITH THE WAY YOU RAN THIS PROGRAM!!'
	printHelp(); 
  	sys.exit(2); 

for opt, arg in opts:
	if opt == '-h': 
		printHelp(); 
		sys.exit(0); 
	if opt == '-u': 
		dbUser = str(arg); 
	if opt == '-p': 
		dbPwd = str(arg); 
	if opt == '-l': 
		dbUrl = str(arg);  
	if opt == '-n': 
		dbName = str(arg); 
	if opt == '-t': 
		dbTable = str(arg); 
	if opt == '-d': 
		outputDir = str(arg); 
	if opt == '-o': 
		outputJavaClass = str(arg); 
	if opt == '-k': 
		package = str(arg); 


db = MySQLdb.connect(host=dbUrl, user=dbUser, passwd=dbPwd, db=dbName); 
cursor = db.cursor(); 
numOfElements = cursor.execute("desc "+dbTable); 
columns = cursor.fetchall(); 
#print columns;
#for col in columns:
#    print col[1];


fileWriter = open(outputDir+outputJavaClass+".java", "w+"); 
initialLines(fileWriter, package); 
initialAnnotationsAndClassName(fileWriter, dbTable, outputJavaClass); 
addMemberVariables(fileWriter, columns); 
addGettersAndSetters(fileWriter, columns); 
endLines(fileWriter); 
fileWriter.close(); 