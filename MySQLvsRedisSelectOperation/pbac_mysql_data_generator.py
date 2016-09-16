import sys
import random
import getopt
from shutil import move
import os


def printHelp():
	print 'This script creates a mysql script file (default name "dummy.sql") - similar to the file "mysqldump" command creates.'
	print 'The mysql script file can be run by the command "mysql -u Username -pPassword DatabaseName < dummy.sql"'
	print ''
	print 'Usage:: python '+sys.argv[0]+' -n <number of integer valued columns> -s <number of string valued columns> '+ \
			'-v <number of distinct values for each column> -r <number of rows to be generated> -o <outputMysqlScriptFile>' + \
			'-p <startOfPrimaryId>'
	print ''
	print 'If, for example you give '+ \
			'"python '+sys.argv[0]+' -n 4 -s 7 -v 3 -r 1000 -o dummy.sql -p 1007 -j \"/path/to/application.properties\" -x \"True\"'+ \
			', the table "dummy" will have its columns as described below:'
	print '+-------+-------------+------+-----+---------+----------------+'
	print '| Field | Type        | Null | Key | Default | Extra          |'
	print '+-------+-------------+------+-----+---------+----------------+'
	print '| id    | int(11)     | NO   | PRI | NULL    | auto_increment |'
	print '| num1  | int(11)     | NO   |     | 0       |                |'
	print '| num2  | int(11)     | NO   |     | 0       |                |'
	print '| num3  | int(11)     | NO   |     | 0       |                |'
	print '| num4  | int(11)     | NO   |     | 0       |                |'
	print '| str1  | varchar(50) | YES  |     | NULL    |                |'
	print '| str2  | varchar(50) | YES  |     | NULL    |                |'
	print '| str3  | varchar(50) | YES  |     | NULL    |                |'
	print '| str4  | varchar(50) | YES  |     | NULL    |                |'
	print '| str5  | varchar(50) | YES  |     | NULL    |                |'
	print '| str6  | varchar(50) | YES  |     | NULL    |                |'
	print '| str7  | varchar(50) | YES  |     | NULL    |                |'
	print '+-------+-------------+------+-----+---------+----------------+'
	print ''
	print 'There are 4 integer columns (not considering "id") because of the option "-n 4".'
	print 'Default value is 4.'
	print ''
	print 'There are 7 string (varchar(50)) columns because of the option "-s 7".'
	print 'Default value is 7.'
	print ''
	print 'Because of the option "-v 3", it would be assumed that each column (except id) has 3 probable values. That is,'
	print '	Value of column "num1" in any row will be one of [1, 2, 3].'
	print '	Value of column "num2" in any row will be one of [1, 2, 3].'
	print '	Value of column "num3" in any row will be one of [1, 2, 3].'
	print '	Value of column "num4" in any row will be one of [1, 2, 3].'
	print '	Value of column "str1" in any row will be one of ["str1_1", "str1_2", "str1_3"]'
	print '	Value of column "str2" in any row will be one of ["str2_1", "str2_2", "str2_3"]'
	print '	Value of column "str3" in any row will be one of ["str3_1", "str3_2", "str3_3"]'
	print '	Value of column "str4" in any row will be one of ["str4_1", "str4_2", "str4_3"]'
	print '	Value of column "str5" in any row will be one of ["str5_1", "str5_2", "str5_3"]'
	print '	Value of column "str6" in any row will be one of ["str6_1", "str6_2", "str6_3"]'
	print '	Value of column "str6" in any row will be one of ["str7_1", "str7_2", "str7_3"]'
	print 'Default value is 3.'
	print ''
	print 'Because of the option "-r 1000", there would be 1000 rows inserted into the table "dummy". ' \
			+'Each column in each row will have a randomly generated value among its "probable values"' \
			+'("probable values" as explained in "-v 3" explanation).'
	print 'Default value is 1000.'
	print ''
	print 'Because of the option "-o dummy.sql", the mysql script file generated would be "dummy.sql".' 
	print 'Default output file is "dummy.sql".'
	print ''
	print 'Because of the option "-p 1007", the rows that shall be generated will have their id (PRIMARY KEY) starting from 1007' \
			+' and shall auto-increment from 1007 onwards till the total number of rows. In our example, the id (PRIMARY KEY) ' \
			+'range of the rows generated shall be 1007 to 2006 (1000 rows - because of the option "-r 1000").'
	print 'Default value is 1.'
	print ''
	print 'Because of the option \'-j \"/path/to/application.properties\"\', this script shall add/replace the following lines in the file ' \
			+'/path/to/application.properties -- '
	print 'hql.permission.query=SELECT distinct D.str7 where D.num1=:num1 and D.num2=:num2 and D.num3=:num3 and D.num3=:num3' \
			+' and D.str1=:str1 and D.str2=:str2 and D.str3=:str3 and D.str4=:str4 and D.str5=:str5 and D.str6=:str6'
	print 'Please look at the java project in the repo for more details as to why this application.properties is used.'
	print 'There is NO default value. The operation explained above will simple not be executed if "-j" option is not given.'
	print ''
	print 'Because of the option \'-x \"True\"\', the mysql script produced will drop the table dummy. If the option is "False", ' \
			'the table shall not be dropped'
	print 'Default value is "True".'



def sqlTextAtTheBeginning(fw):
	fw.write("-- MySQL dump 10.13  Distrib 5.7.13, for Linux (x86_64)\n" \
		+"--\n" \
		#+"-- Host: localhost    Database: yaji_pbac_loadtest\n" \
		+"-- ------------------------------------------------------\n" \
		+"-- Server version       5.6.30\n" \
		+"\n" \
		+"/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;\n" \
		+"/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;\n" \
		+"/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;\n" \
		+"/*!40101 SET NAMES utf8 */;\n" \
		+"/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;\n" \
		+"/*!40103 SET TIME_ZONE='+00:00' */;\n" \
		+"/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;\n" \
		+"/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;\n" \
		+"/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;\n" \
		+"/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;\n" \
		+"\n" \
		+"--\n" \
		+"-- Table structure for table `dummy`\n" \
		+"--\n");

def sqlTextAtTheEnd(fw):
	fw.write("/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;\n" \
		+"\n" \
		+"/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;\n" \
		+"/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;\n" \
		+"/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;\n" \
		+"/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;\n" \
		+"/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;\n" \
		+"/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;\n" \
		+"/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;\n")


def dropTableDummy(fw):
	fw.write("DROP TABLE IF EXISTS `dummy`;\n");

def addCompositeIndex(fw, numLists, strLists):
	fw.write(",\n"+"  INDEX dummy_index (");
	isCommaNeeded=False;
	for i in range(1,len(numLists)+1):
		if isCommaNeeded:
			fw.write(", ");
		fw.write("`num"+str(i)+"`");
		if not isCommaNeeded:
			isCommaNeeded=True;
	for j in range(1,len(strLists)):
		if isCommaNeeded:
			fw.write(", ");
		fw.write("`str"+str(j)+"`");
		if not isCommaNeeded:
			isCommaNeeded=True;
	fw.write(")");


def createTableDummy(fw, numLists, strLists, isCompositeIndex=True):
	fw.write("/*!40101 SET @saved_cs_client     = @@character_set_client */;\n" \
		+"/*!40101 SET character_set_client = utf8 */;\n");
	fw.write("CREATE TABLE `dummy` (\n" \
		+"  `id` int(11) NOT NULL AUTO_INCREMENT");
	if numLists:
		fw.write(",\n")
		for i in range(1, len(numLists)):
			fw.write("  `num"+str(i)+"` int(11) NOT NULL DEFAULT '0',\n");
		fw.write("  `num"+str(len(numLists))+"` int(11) NOT NULL DEFAULT '0'");
	if 	strLists:
		fw.write(",\n");
		for j in range(1, len(strLists)):
			fw.write("  `str"+str(j)+"` varchar(50) DEFAULT NULL,\n");
		fw.write("  `str"+str(len(strLists))+"` varchar(50) DEFAULT NULL")
	fw.write(",\n"+"  PRIMARY KEY (`id`)")
	if isCompositeIndex:
		addCompositeIndex(fw, numLists, strLists);
	fw.write("\n) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;\n" \
		+"/*!40101 SET character_set_client = @saved_cs_client */;\n");

def putDataIntoTableDummy(fw, numLists, strLists, rows, primaryId):
	fw.write("LOCK TABLES `dummy` WRITE;\n");
	fw.write("/*!40000 ALTER TABLE `dummy` DISABLE KEYS */;\n");
	# print ''
	# print 'Inside putDataIntoTableDummy'
	# print ''
	# print numLists
	# print ''
	# print strLists

	for k in range(1,rows+1):
		fw.write("INSERT INTO `dummy` VALUES ("+str(primaryId));
		for nList in numLists:
			# print "nList: "
			# print nList;
			if nList:
				fw.write(","+str(random.choice(nList)));
		for sList in strLists:
			# print "sList: "
			# print sList;
			if sList:
				fw.write(",'"+random.choice(sList)+"'");
		fw.write(");\n");
		primaryId+=1;

	# for num1 in range(1,5):
	# 	for num2 in range(1,5):
	# 		for num3 in range(1,5):
	# 			for num4 in range(1,5):
	# 				fx.write("INSERT INTO `dummy` VALUES ("+str(myId)+"," \
	# 					+str(num1)+","+str(num2)+","+str(num3)+","+str(num4)+"," \
	# 					+"'"+random.choice(str1Vals)+"'"+","+"'"+random.choice(str2Vals)+"'"+"," \
	# 					+"'"+random.choice(str3Vals)+"'"+","+"'"+random.choice(str4Vals)+"'"+"," \
	# 					+"'"+random.choice(str5Vals)+"'"+","+"'"+random.choice(str6Vals)+"'"+"," \
	# 					+"'"+random.choice(str7Vals)+"'"+");\n");
	# 				myId+=1;

	fw.write("/*!40000 ALTER TABLE `dummy` ENABLE KEYS */;\n");
	fw.write("UNLOCK TABLES;\n");


def makeIntValList(numb):
	return range(1,numb+1);

def makeStrValList(stri, numb):
	ret = [];
	for i in range(1,numb+1):
		ret.append(stri+str(i));
	return ret;


def recursiveList(myList):
	if not myList:
		return [];
	ret=[]
	retListOrig = recursiveList(myList[1:]);
	for i in myList[0]:
		retList = list(retListOrig);
		if not retList:
			ret.append([i]);
		else:
			for x in range(0,len(retList)):
				iList = list(retList[x]);
				iList.append(i);
				ret.append(iList);
	return ret;


def constructHQLPermissionQuery(intColumns, strColumns):
	hqlQuery="hql.permission.query=SELECT distinct D.str"+str(strColumns)+" FROM Dummy D where" 
	isAndReqd = False;
	# hql.permission.query=SELECT distinct D.str7 FROM Dummy D where
	# D.num1=:num1 and D.num2=:num2 and D.num3=:num3 and D.num4=:num4 
	# and D.str1=:str1 and D.str2=:str2 and D.str3=:str3 and D.str4=:str4 and D.str5=:str5 and D.str6=:str6
	for i in range(1,intColumns+1):
		temp="num"+str(i);
		if not i==1:
			hqlQuery = hqlQuery + " and";
		hqlQuery = hqlQuery + " D."+temp+"=:"+temp;
		isAndReqd=True;
	for j in range(1,strColumns):
		temp="str"+str(j);
		if isAndReqd:
			hqlQuery = hqlQuery + " and";
		hqlQuery = hqlQuery + " D."+temp+"=:"+temp;
	return hqlQuery+"\n";



def writeApplicationProperties(path, intColumns, strColumns):
	if path:
		fa = open(path,'r');
		fn = open(path+".new",'w');
		for line in fa:
			if not line.find("hql.permission.query") == -1:
				fn.write(constructHQLPermissionQuery(intColumns,strColumns));
			else:
				fn.write(line);
		fa.close();
		fn.close();
		os.remove(path);
		move(path+".new",path);



#########################  MAIN()  #######################################

intColumns=4;
strColumns=7;
distinctVals=3;
rows=1000;
sqlFileName="dummy.sql";
primaryId=1;
isDropTableDummy=True;
application_properties_file_path=""

try:
    opts, args = getopt.getopt(sys.argv[1:],"hn:s:v:r:o:p:x:j:");
except getopt.GetoptError:
	print ''
	print 'SOMETHING WENT WRONG WITH THE WAY YOU RAN THIS PROGRAM!!'
	print 'To see how to run this program run "python '+sys.argv[0]+' -h'
  	sys.exit(2);

for opt, arg in opts:
	if opt == '-h':
		printHelp();
		sys.exit(0);
	if opt == '-n':
		intColumns = int(arg);
	if opt == '-s':
		strColumns = int(arg);
	if opt == '-v':
		distinctVals = int(arg);
	if opt == '-r':
		rows = int(arg);
	if opt == '-o':
		sqlFileName = str(arg);
	if opt == '-p':
		primaryId = int(arg);
	if opt == '-x':
		isDropTableDummy = bool(arg);
	if opt == '-j':
		print 'arg -- '+arg
		application_properties_file_path = str(arg)

print 'nValue = '+str(intColumns);
print 'sValue = '+str(strColumns);
print 'vValue = '+str(distinctVals);
print 'rValue = '+str(rows);
print 'oValue = '+sqlFileName;
print 'jValue = '+application_properties_file_path
print 'xValue = '+str(isDropTableDummy)
print ''

numLists=[]
strLists=[]

for i in range(1,intColumns+1):
	myList = makeIntValList(distinctVals);
	numLists.append(myList);

for i in range(1,strColumns+1):
	myList = makeStrValList("str"+str(i)+"_",distinctVals);
	strLists.append(myList);

# print 'numLists:'
# print numLists
# print ''
# print 'strLists:'
# print strLists
# print ''

fx = open(sqlFileName,'w');
sqlTextAtTheBeginning(fx);
if isDropTableDummy:
	dropTableDummy(fx);
	createTableDummy(fx, numLists, strLists);
putDataIntoTableDummy(fx, numLists, strLists, rows, primaryId);
sqlTextAtTheEnd(fx);

fx.close();

if application_properties_file_path:
	writeApplicationProperties(application_properties_file_path, intColumns, strColumns);
#echo "LOCK TABLES `dummy` WRITE;" >> new_sql.sql
#echo "/*!40000 ALTER TABLE `dummy` DISABLE KEYS */;" >> new_sql.sql
#echo "INSERT INTO `dummy` VALUES (1,1,1,1,1,'one','one','one','one','one','one','one');" >> new_sql.sql
#echo "/*!40000 ALTER TABLE `dummy` ENABLE KEYS */;" >> new_sql.sql
#echo "UNLOCK TABLES;" >> new_sql.sql
