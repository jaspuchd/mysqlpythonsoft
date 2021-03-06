-- MySQL dump 10.13  Distrib 5.7.20, for Linux (x86_64)
--
-- Host: localhost    Database: jgh
-- ------------------------------------------------------
-- Server version	5.7.20-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `commit`
--

DROP TABLE IF EXISTS `commit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `commit` (
  `sha` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `repo_id` int(11) unsigned NOT NULL,
  `comment_count` int(11) NOT NULL,
  `author_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `author_email` varchar(80) COLLATE utf8_unicode_ci DEFAULT NULL,
  `author_date` datetime DEFAULT NULL,
  `committer_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `committer_email` varchar(80) COLLATE utf8_unicode_ci DEFAULT NULL,
  `committer_date` datetime DEFAULT NULL,
  PRIMARY KEY (`sha`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commit`
--

LOCK TABLES `commit` WRITE;
/*!40000 ALTER TABLE `commit` DISABLE KEYS */;
/*!40000 ALTER TABLE `commit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contents`
--

DROP TABLE IF EXISTS `contents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contents` (
  `sha` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `repo_id` int(11) unsigned NOT NULL,
  `name` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `path` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `size` int(11) NOT NULL,
  `type` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`sha`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contents`
--

LOCK TABLES `contents` WRITE;
/*!40000 ALTER TABLE `contents` DISABLE KEYS */;
/*!40000 ALTER TABLE `contents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `issue`
--

DROP TABLE IF EXISTS `issue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `issue` (
  `id` int(11) unsigned NOT NULL,
  `number` int(10) unsigned NOT NULL,
  `repo_id` int(11) unsigned NOT NULL,
  `title` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_by` int(11) unsigned NOT NULL,
  `state` varchar(6) COLLATE utf8_unicode_ci NOT NULL,
  `is_locked` tinyint(1) NOT NULL,
  `milestone_id` int(11) unsigned DEFAULT NULL,
  `is_pull_request` tinyint(1) NOT NULL,
  `comments_count` int(10) unsigned NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `closed_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `issue`
--

LOCK TABLES `issue` WRITE;
/*!40000 ALTER TABLE `issue` DISABLE KEYS */;
/*!40000 ALTER TABLE `issue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repo`
--

DROP TABLE IF EXISTS `repo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `repo` (
  `id` int(11) unsigned NOT NULL,
  `name` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `is_fork` tinyint(1) unsigned NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `pushed_at` datetime DEFAULT NULL,
  `homepage` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `size` int(10) unsigned NOT NULL,
  `stargazers_count` int(10) unsigned NOT NULL,
  `watchers_count` int(10) unsigned NOT NULL,
  `forks` int(10) unsigned NOT NULL,
  `primary_language` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `has_issues` tinyint(1) unsigned NOT NULL,
  `has_pages` tinyint(1) unsigned NOT NULL,
  `has_wiki` tinyint(1) unsigned NOT NULL,
  `is_archived` tinyint(1) unsigned NOT NULL,
  `open_issues` int(10) unsigned DEFAULT NULL,
  `license` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `network_count` int(10) unsigned DEFAULT NULL,
  `user_id` int(11) unsigned NOT NULL,
  `parent_repo_id` int(11) unsigned DEFAULT NULL,
  `parent_repo_owner_id` int(11) unsigned DEFAULT NULL,
  `source_repo_id` int(11) unsigned DEFAULT NULL,
  `source_repo_full_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_repo_owner_id` int(11) unsigned DEFAULT NULL,
  `parent_repo_full_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `full_name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repo`
--

LOCK TABLES `repo` WRITE;
/*!40000 ALTER TABLE `repo` DISABLE KEYS */;
/*!40000 ALTER TABLE `repo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) unsigned NOT NULL,
  `login` varchar(25) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `company` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `blog` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `location` varchar(40) COLLATE utf8_unicode_ci DEFAULT NULL,
  `email` varchar(90) COLLATE utf8_unicode_ci DEFAULT NULL,
  `hireable` tinyint(1) unsigned DEFAULT NULL,
  `public_repos` int(11) NOT NULL,
  `public_gists` int(11) NOT NULL,
  `followers` int(11) NOT NULL,
  `following` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-01-16 17:11:19
