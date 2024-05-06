-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: admin
-- ------------------------------------------------------
-- Server version	8.0.36-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `CONTAINER_DETAILS`
--

DROP TABLE IF EXISTS `CONTAINER_DETAILS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CONTAINER_DETAILS` (
  `IP_ADDRESS` varchar(15) DEFAULT NULL,
  `URL` varchar(255) DEFAULT NULL,
  `DOCKER_IMAGE_NAME` varchar(255) DEFAULT NULL,
  `PACKAGE` varchar(255) DEFAULT NULL,
  `PASSWORD` varchar(255) DEFAULT NULL,
  `COURSE` varchar(255) DEFAULT NULL,
  `SUBJECT` varchar(255) DEFAULT NULL,
  `FACULTY_REQUEST_ID` int DEFAULT NULL,
  `SOURCE_VOLUME_LOCATION` varchar(255) DEFAULT NULL,
  `CONTAINER_ID` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CONTAINER_DETAILS`
--

LOCK TABLES `CONTAINER_DETAILS` WRITE;
/*!40000 ALTER TABLE `CONTAINER_DETAILS` DISABLE KEYS */;
INSERT INTO `CONTAINER_DETAILS` VALUES ('172.16.51.26','http://172.16.51.26:3331','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 1A','Machine learning Lab Morning',1,'MLB7457','eef78ad5858c8183be2c680333b9a95ac93edf17a4e910dc50991782042a6769\n'),('172.16.51.34','http://172.16.51.34:3346','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 1A','Machine learning Lab Morning',1,'MLB4090','7229531ce7820839d9561ac65d2519f08c161d825057b829aa2be57608c88f61\n'),('172.16.51.21','http://172.16.51.21:3365','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 1A','Machine learning Lab Morning',1,'MLB8978','ddc61f09ae64924cb0dabff0dd26535953924c13e4c55cb83118fafda11787c8\n'),('172.16.51.121','http://172.16.51.121:3381','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 1A','Machine learning Lab Morning',1,'MLB2026','3fd761f5364d1607ee469fc910750c376406fc542f842a8ebdee65e3e74581c7\n'),('172.16.51.38','http://172.16.51.38:3405','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 1A','Machine learning Lab Morning',1,'MLB4214','bfc00a6c27697bbc125163c4911b0a40700c2a98cb7b803b72490da801f413dc\n'),('172.16.51.50','http://172.16.51.50:3422','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 1A','Machine learning Lab Morning',1,'MLB4270','bb64df4de3831a703eb64455d25ad6d699b951ede05220ab7ef1a734f3b607b0\n'),('172.16.51.26','http://172.16.51.26:3440','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 1A','Machine learning Lab Morning',1,'MLB8869','cbff3fd380b402b58c3c68b0bed409b3d2148c7133d7a4147933baec0a17da34\n'),('172.16.51.34','http://172.16.51.34:3458','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 1A','Machine learning Lab Morning',1,'MLB6932','20867dbacf2d859cc929d13499764771886b6d86e4237ac12371ec85ec7bf497\n'),('172.16.51.21','http://172.16.51.21:3473','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 1A','Machine learning Lab Morning',1,'MLB3784','9585a1538df06efbc93be8f3c3ac37588bc6b0f527b6f39696652f05a79ff572\n'),('172.16.51.121','http://172.16.51.121:3483','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 1A','Machine learning Lab Morning',1,'MLB7105','34106be5ee3bc9251297a270cf3baca0ccfadd7de760842e03a37f97e82dfdd0\n'),('172.16.51.38','http://172.16.51.38:3507','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 1A','Machine learning Lab Morning',1,'MLB8249','ac22d13cd5c1c22bb70f021a57ec4781af12c8a1bbafeda76ba85be325802768\n'),('172.16.51.50','http://172.16.51.50:3519','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 1A','Machine learning Lab Morning',1,'MLB5102','e07240fb004016d471f0a72723564a01da41ad1f2f0089c539f85875e845f631\n'),('172.16.51.26','http://172.16.51.26:3534','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 1A','Machine learning Lab Morning',1,'MLB3866','61cb43424f524c1a9735f1f621ff767ba7e04fb7a11d2251155b608225a83111\n'),('172.16.51.34','http://172.16.51.34:3555','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 1A','Machine learning Lab Morning',1,'MLB5853','a65b95c168b74b7792b75cb5da671ed6f9a67849b857344a153ee15ebe205048\n'),('172.16.51.21','http://172.16.51.21:3569','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 1A','Machine learning Lab Morning',1,'MLB5153','08b8754549be17eebc722f5150721ad7d1e14acef23bb5ea551512109a621230\n'),('172.16.51.26','http://172.16.51.26:5178','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 2A','Machine learning Lab Afternoon',2,'MLB8777','ff4ae332f6873b7e73338bf6f674fd1eb723a22d3d6966e7b37849212512b7dc\n'),('172.16.51.34','http://172.16.51.34:5193','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 2A','Machine learning Lab Afternoon',2,'MLB8152','3b74ae17fd31670142dfb3e3b67dddb32edc74d72d18fb4aaef6f82b45501c93\n'),('172.16.51.21','http://172.16.51.21:5211','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 2A','Machine learning Lab Afternoon',2,'MLB9564','199808fb27011806a5915580d01e6e242b1c37800cbb2b4321977e12b500c1c9\n'),('172.16.51.121','http://172.16.51.121:5228','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 2A','Machine learning Lab Afternoon',2,'MLB2218','a01707469a5a959cb04ff18d8c37c0501794c805b740115f5ec4c7443f1ef6e7\n'),('172.16.51.38','http://172.16.51.38:5248','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 2A','Machine learning Lab Afternoon',2,'MLB1088','004dd236acd479a563d6cd624618ee1621c80a3f797209a37f92fc0eba709ee7\n'),('172.16.51.50','http://172.16.51.50:5258','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 2A','Machine learning Lab Afternoon',2,'MLB8663','d21448f3d46455c8241e0a0c04ffc199750eef7e946bcb2fab2361c0cbbd1d4e\n'),('172.16.51.26','http://172.16.51.26:5271','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 2A','Machine learning Lab Afternoon',2,'MLB6887','1b82b8945b414069e3d509157424e385fad7d4c2c3af59ed5516201780689a59\n'),('172.16.51.34','http://172.16.51.34:5281','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 2A','Machine learning Lab Afternoon',2,'MLB9714','87319c851e32699d59f19e6404cadf939fe6b30719c76cb5efd2deb86cd6e3c7\n'),('172.16.51.21','http://172.16.51.21:5295','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 2A','Machine learning Lab Afternoon',2,'MLB9410','19287c1e32a7244a4df4ad9d883d25254a3f2eff73a6ccfd53b489284855909e\n'),('172.16.51.121','http://172.16.51.121:5305','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 2A','Machine learning Lab Afternoon',2,'MLB9929','01182823f46df57992602a8c7fe2a1b33b9fc2122ff981d068d818d550eae7a5\n'),('172.16.51.38','http://172.16.51.38:5323','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 2A','Machine learning Lab Afternoon',2,'MLB9563','4474993f502a7f106dc5c0558b731712b66c9b7f121456fd8de8f9e9f6dbe8e2\n'),('172.16.51.50','http://172.16.51.50:5335','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 2A','Machine learning Lab Afternoon',2,'MLB2872','f5561f877db7f5b1a957d91c01dee062a0d4b4e49c2729c1412f7db3b04cf0c9\n'),('172.16.51.26','http://172.16.51.26:5346','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 2A','Machine learning Lab Afternoon',2,'MLB8060','5ed1b6c6fe24c3529c26852c163c63821531df5f9a991cf65a62afe75d7290ad\n'),('172.16.51.34','http://172.16.51.34:5358','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 2A','Machine learning Lab Afternoon',2,'MLB5622','98eb8ee50361d87fcd10ada3cde9d9d7a7584689f0fa0db2b48d19924f3e3bd6\n'),('172.16.51.21','http://172.16.51.21:5373','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 2A','Machine learning Lab Afternoon',2,'MLB4844','83a370b4032cfb21cd6d6458a3c8cc7f6430c565c89bbd11595014747398197a\n'),('172.16.51.121','http://172.16.51.121:5386','sreedocker123/mllabjupyter:updated','jupyter:updated','msois@123 ','Big Data Analytics Batch 2A','Machine learning Lab Afternoon',2,'MLB8907','b657685f8f0a73841d721fe061c21bcd456a3f62ee7f07c0d2e7fcc5c1468b82\n');
/*!40000 ALTER TABLE `CONTAINER_DETAILS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_details`
--

DROP TABLE IF EXISTS `course_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course_details` (
  `course_id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_details`
--

LOCK TABLES `course_details` WRITE;
/*!40000 ALTER TABLE `course_details` DISABLE KEYS */;
INSERT INTO `course_details` VALUES (1,'Cloud Computing'),(2,'Big Data'),(3,'VLSI'),(4,'Cyber security'),(11,'Big Data Analytics Batch 1A'),(13,'Big Data Analytics Batch 2A');
/*!40000 ALTER TABLE `course_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty_details`
--

DROP TABLE IF EXISTS `faculty_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty_details` (
  `FACULTY_ID` varchar(255) NOT NULL,
  `FACULTY_NAME` varchar(255) DEFAULT NULL,
  `COURSE` varchar(255) DEFAULT NULL,
  `INSTITUTE` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`FACULTY_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty_details`
--

LOCK TABLES `faculty_details` WRITE;
/*!40000 ALTER TABLE `faculty_details` DISABLE KEYS */;
INSERT INTO `faculty_details` VALUES ('101','Vashishta','Cloud Computing','SOIS'),('102','Vasudeva','Big Data','SOIS'),('103','Dronacharya','VLSI','SOIS'),('MAHE0007066','AROCKIARAJ S','Big Data Analytics','MSIS');
/*!40000 ALTER TABLE `faculty_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty_requests`
--

DROP TABLE IF EXISTS `faculty_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty_requests` (
  `REQUEST_ID` int NOT NULL AUTO_INCREMENT,
  `Course_name` varchar(255) DEFAULT NULL,
  `Subject` varchar(255) DEFAULT NULL,
  `Faculty_ID` varchar(255) DEFAULT NULL,
  `NUM_SYS_REQ` int DEFAULT NULL,
  `OS_TYPE` varchar(255) DEFAULT NULL,
  `REQUIRED_TOOLS` varchar(255) DEFAULT NULL,
  `REQUEST_DATETIME` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `START_DATE` date DEFAULT NULL,
  `START_TIME` time DEFAULT NULL,
  `END_DATE` date DEFAULT NULL,
  `END_TIME` time DEFAULT NULL,
  PRIMARY KEY (`REQUEST_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty_requests`
--

LOCK TABLES `faculty_requests` WRITE;
/*!40000 ALTER TABLE `faculty_requests` DISABLE KEYS */;
INSERT INTO `faculty_requests` VALUES (1,'Big Data Analytics Batch 1A','Machine learning Lab Morning','101',15,'Exam','jupyter:updated','2024-05-02 12:15:42','2024-05-03','08:45:00','2024-05-03','12:30:00'),(2,'Big Data Analytics Batch 2A','Machine learning Lab Afternoon','101',16,'Exam','jupyter:updated','2024-05-03 06:52:15','2024-05-03','12:45:00','2024-05-03','17:00:00');
/*!40000 ALTER TABLE `faculty_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_details`
--

DROP TABLE IF EXISTS `server_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `server_details` (
  `Hostid` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `hostname` varchar(255) DEFAULT NULL,
  `ip_address` varchar(15) DEFAULT NULL,
  `root_username` varchar(255) DEFAULT NULL,
  `Host_OS` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Hostid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_details`
--

LOCK TABLES `server_details` WRITE;
/*!40000 ALTER TABLE `server_details` DISABLE KEYS */;
INSERT INTO `server_details` VALUES ('11','cloud@321','cdc-msis5','172.16.51.26','msis','Linux'),('12','cloud@321','PROJECTADMIN','172.16.51.34','msis','Linux'),('13','cloud@321','cdc-msis4','172.16.51.21','msis','Linux'),('14','sois@123','jenkins','172.16.51.121','jenkins','ubuntu'),('15','raghu@123','raghu','172.16.51.38','raghu','ubuntu'),('16','sois@123','kubemaster','172.16.51.50','ansible','ubuntu');
/*!40000 ALTER TABLE `server_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_details`
--

DROP TABLE IF EXISTS `student_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_details` (
  `REGID` varchar(255) NOT NULL,
  `STUDENTNAME` varchar(255) DEFAULT NULL,
  `COURSE` varchar(255) DEFAULT NULL,
  `INSTITUTE` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`REGID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_details`
--

LOCK TABLES `student_details` WRITE;
/*!40000 ALTER TABLE `student_details` DISABLE KEYS */;
INSERT INTO `student_details` VALUES ('02','Sita','Cloud Computing','SOIS'),('03','Luxman','Cloud Computing','SOIS'),('04','Krishna','Big Data','SOIS'),('05','Balaram','Big Data','SOIS'),('06','Radha','Big Data','SOIS'),('07','Arjun','VLSI','SOIS'),('08','Draupadi','VLSI','SOIS'),('09','Bhima','VLSI','SOIS'),('1','Ram','Cloud Computing','SOIS'),('10','Rex','Cyber security','SOIS'),('104','Roy','cloud computing','msis'),('11','Prem','Cyber security','SOIS'),('231058001','NIDHI.S','Big Data Analytics Batch 1A','MSIS'),('231058002','SUDHANVA H G','Big Data Analytics Batch 1A','MSIS'),('231058003','NITHIN B M','Big Data Analytics Batch 1A','MSIS'),('231058004','SUSHRUTH E S','Big Data Analytics Batch 1A','MSIS'),('231058005','CHAITANYA SACHIDANAND','Big Data Analytics Batch 1A','MSIS'),('231058006','AKASH G S KUMAR','Big Data Analytics Batch 1A','MSIS'),('231058007','GOWTHAMI G BHAT','Big Data Analytics Batch 1A','MSIS'),('231058008','ABHISHEK ASUNDI','Big Data Analytics Batch 1A','MSIS'),('231058009','B T ANVIT','Big Data Analytics Batch 1A','MSIS'),('231058010','TEJAS M','Big Data Analytics Batch 1A','MSIS'),('231058011','S SHREE LAKSHMI','Big Data Analytics Batch 2A','MSIS'),('231058012','MANTHANA H K','Big Data Analytics Batch 1A','MSIS'),('231058013','B A SOHANKUMAR','Big Data Analytics Batch 1A','MSIS'),('231058014','PREETHAM GOUDA S PATIL','Big Data Analytics Batch 1A','MSIS'),('231058015','PUNEETH G L','Big Data Analytics Batch 1A','MSIS'),('231058016','DHRUVA D NAYAK','Big Data Analytics Batch 2A','MSIS'),('231058017','J TRESHIKA','Big Data Analytics Batch 2A','MSIS'),('231058019','CHETHAN N','Big Data Analytics Batch 2A','MSIS'),('231058020','SUJANA','Big Data Analytics Batch 2A','MSIS'),('231058021','IMAAD SALIM SHAIKH','Big Data Analytics Batch 2A','MSIS'),('231058022','ARUNA B','Big Data Analytics Batch 2A','MSIS'),('231058023','SUHAS S A','Big Data Analytics Batch 2A','MSIS'),('231058024','AARON DAVID KARKADA','Big Data Analytics Batch 2A','MSIS'),('231058025','RAKSHIT V M','Big Data Analytics Batch 2A','MSIS'),('231058027','N PRAMEETH SHENOY','Big Data Analytics Batch 2A','MSIS'),('231058028','VINAY H M','Big Data Analytics Batch 2A','MSIS'),('231058029','ANANYA V BHAT','Big Data Analytics Batch 2A','MSIS'),('231058030','NANDAN N','Big Data Analytics Batch 2A','MSIS'),('231058031','SAHANA C','Big Data Analytics Batch 2A','MSIS'),('231058032','SHRUNGA K P','Big Data Analytics Batch 2A','MSIS');
/*!40000 ALTER TABLE `student_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subject_details`
--

DROP TABLE IF EXISTS `subject_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subject_details` (
  `subject_id` int NOT NULL AUTO_INCREMENT,
  `course_id` int DEFAULT NULL,
  `subject_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`subject_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `subject_details_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course_details` (`course_id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subject_details`
--

LOCK TABLES `subject_details` WRITE;
/*!40000 ALTER TABLE `subject_details` DISABLE KEYS */;
INSERT INTO `subject_details` VALUES (1,1,'DEVOPS FOR CLOUD'),(2,1,'LINUX AND DATA STRUCUTURE'),(3,1,'CLOUD ARCHITECTURE AND MANAGEMENT'),(4,2,'APPLIED PROBABILITY AND STATISTICS'),(5,2,'ARCHITECTURE OF BIG DATA SYSTEMS'),(6,2,'PRINCIPAL OF DATA VISUALIZATION'),(7,3,'DIGITAL SYSTEM'),(8,3,'CAD FOR VLSI'),(9,3,'VERIFICATION'),(10,2,'VERIFICATION'),(11,1,'PRINCIPAL OF DATA VISUALIZATION'),(12,3,'LINUX AND DATA STRUCUTURE'),(13,1,'DATA STRUCTURES'),(14,2,'DATA STRUCTURES'),(15,3,'DATA STRUCTURES'),(16,4,'COMPUTER NETWORKS AND SECURITY'),(17,4,'LINUX OS AND SCRIPTING'),(18,4,'CRYPTOLOGY'),(19,4,'ETHICAL HACKING'),(20,4,'DEVOPS FOR CLOUD'),(52,11,'Machine learning Lab Morning'),(54,13,'Machine learning Lab Afternoon');
/*!40000 ALTER TABLE `subject_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tools`
--

DROP TABLE IF EXISTS `tools`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tools` (
  `TOOLID` int NOT NULL AUTO_INCREMENT,
  `OS` varchar(255) DEFAULT NULL,
  `PACKAGES` varchar(255) DEFAULT NULL,
  `HOST_PORT` varchar(255) DEFAULT NULL,
  `CONTAINER_PORT` varchar(255) DEFAULT NULL,
  `USERNAME` varchar(255) DEFAULT NULL,
  `PASSWORD_KEY` varchar(255) DEFAULT NULL,
  `PASSWORD_VALUE` varchar(255) DEFAULT NULL,
  `DOCKER_IMAGE_NAME` varchar(255) DEFAULT NULL,
  `SOURCE_VOLUME` varchar(255) DEFAULT NULL,
  `CONTAINER_VOLUME` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`TOOLID`)
) ENGINE=InnoDB AUTO_INCREMENT=1322 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tools`
--

LOCK TABLES `tools` WRITE;
/*!40000 ALTER TABLE `tools` DISABLE KEYS */;
INSERT INTO `tools` VALUES (1,'Ubuntu','Sublime Text, GCC, JAVA Netbeans','6901','6901','SOIS','VNC_PW','soisvnc@123','jiteshsojitra/docker-ubuntu-xfce-container','LDS','/root'),(2,'Ubuntu','Eclips, VS code','6080','6080','SOIS','VNCPASS','soisvnc@123','sreedocker123/docker-eclipse-novnc','JWT','/home/ubuntu'),(3,'CentOS','GCC, Gedit','6901','6901','SOIS','VNC','soisvnc@123','consol/centos-xfce-vnc','VLSI','/root'),(4,'Ubuntu','JupyterHub','8888','8888','MSIS','JUPYTER_TOKEN','msois@123','jupyter/scipy-notebook:83ed2c63671f','FML','/home/jovyan'),(5,'CentOS','rstudio,test','8899','8787','rstudio','PASSWORD','soisrstudio@123','rocker/verse','APS','/home/rstudio'),(7,'Exam','jupyter:updated','8888','8888','EXAM','JUPYTER_TOKEN','msois@123 ','sreedocker123/mllabjupyter:updated','MLB','/home/jovyan'),(8,' Ubuntu 22.04','VS Code and Dot Net SDK 8.0','6901','6901  --user root','msis','VNC_PW','soisvnc@123','sreedocker123/ubuntuvscodedotnet:latest','DOTNET','/home/headless'),(12,'Ubuntu','Jupyter-opencv-librosa','8888','8888','sois','JUPYTER_TOKEN','msois@123 ','sreedocker123/mllabjupyter:opencv','MMA','/home/jovyan');
/*!40000 ALTER TABLE `tools` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-03 16:49:47
