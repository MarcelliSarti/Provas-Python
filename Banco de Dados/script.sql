create database grexaminations;

use grexaminations;

CREATE TABLE `courses` (
  `id` char(20) NOT NULL,
  `numberOfSeries` int NOT NULL DEFAULT '1',
  `caption` char(100) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `examconstraints` (
  `id` int NOT NULL AUTO_INCREMENT,
  `login` char(50) NOT NULL,
  `done` int NOT NULL DEFAULT '0',
  `courseId` char(20) NOT NULL,
  `specialityId` char(20) NOT NULL,
  `subjectId` char(20) NOT NULL,
  `serie` int NOT NULL,
  `examType` char(20) NOT NULL,
  `size1` int NOT NULL,
  `bFacility1` int NOT NULL,
  `eFacility1` int NOT NULL,
  `size2` int NOT NULL,
  `bFacility2` int NOT NULL,
  `eFacility2` int NOT NULL,
  `size3` int NOT NULL,
  `bFacility3` int NOT NULL,
  `eFacility3` int NOT NULL,
  `creation` date NOT NULL,
  `readDate` date NOT NULL,
  `counterX0` int NOT NULL DEFAULT '0',
  `counterX9` int NOT NULL DEFAULT '0',
  `counterWarning` int NOT NULL DEFAULT '0',
  `numberOfQuestions` int NOT NULL DEFAULT '0',
  `applyDate` date NOT NULL,
  `monthsFromLastUse` int NOT NULL DEFAULT '24',
  PRIMARY KEY (`id`)
);

CREATE TABLE `exams` (
  `id` int NOT NULL,
  `class` char(3) NOT NULL,
  `questionNumber` int NOT NULL,
  `questionId` int NOT NULL,
  `globalFacility` int NOT NULL,
  `localFacility` int NOT NULL DEFAULT '0',
  `A` int NOT NULL DEFAULT '0',
  `B` int NOT NULL DEFAULT '0',
  `C` int NOT NULL DEFAULT '0',
  `D` int NOT NULL DEFAULT '0',
  `counterA` int NOT NULL DEFAULT '0',
  `counterB` int NOT NULL DEFAULT '0',
  `counterC` int NOT NULL DEFAULT '0',
  `counterD` int NOT NULL DEFAULT '0'
);

CREATE TABLE `examstructure` (
  `examConstraintsId` int NOT NULL,
  `login` char(50) NOT NULL,
  `unit` int NOT NULL,
  `subUnit` int NOT NULL,
  `CH` int NOT NULL,
  `numberOfQuestions` int NOT NULL,
  `questionsAvailable` int NOT NULL
);

CREATE TABLE `examtype` (
  `id` char(20) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `examuniverse` (
  `examConstraintsId` int NOT NULL,
  `login` char(50) NOT NULL,
  `questionId` int NOT NULL,
  `rightAnswer` char(1) DEFAULT NULL,
  `facility` int NOT NULL,
  `lastUsed` date DEFAULT NULL,
  `status` int NOT NULL DEFAULT '0',
  `unit` int NOT NULL,
  `subUnit` int NOT NULL
);

CREATE TABLE `hyerarchies` (
  `hyerarchy` char(3) NOT NULL,
  `levelNo` int NOT NULL,
  `caption` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`hyerarchy`)
);

CREATE TABLE `questions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `subjectId` char(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `author` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `initialFacility` int NOT NULL,
  `facility` int NOT NULL,
  `unit` int NOT NULL,
  `subUnit` int NOT NULL,
  `rightAnswer` char(1) COLLATE utf8mb4_unicode_ci NOT NULL,
  `body` mediumtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `bodyImage` char(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `answer1` mediumtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `answer1Image` char(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `answer2` mediumtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `answer2Image` char(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `answer3` mediumtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `answer3Image` char(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `answer4` mediumtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `answer4Image` char(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `reference` char(250) COLLATE utf8mb4_unicode_ci NOT NULL,
  `lastUsed` date DEFAULT NULL,
  `creation` date DEFAULT NULL,
  `questionType` int NOT NULL,
  `revision` int NOT NULL DEFAULT '0',
  `counter` int NOT NULL DEFAULT '0',
  `counterA` int NOT NULL DEFAULT '0',
  `counterB` int NOT NULL DEFAULT '0',
  `counterC` int NOT NULL DEFAULT '0',
  `counterD` int NOT NULL DEFAULT '0',
  `status` int NOT NULL DEFAULT '0',
  `numberAtSU` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=733604 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `series` (
  `id` int NOT NULL AUTO_INCREMENT,
  `serie` int NOT NULL,
  `courseId` char(20) NOT NULL,
  `specialityId` char(20) NOT NULL,
  `subjectId` int NOT NULL,
  `exposureClasses` int NOT NULL,
  `practiceClasses` int NOT NULL,
  `examClasses` int NOT NULL,
  `partialExams` int NOT NULL,
  `finalExams` int NOT NULL,
  `practiceExams` int NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `specialities` (
  `id` char(20) NOT NULL,
  `caption` char(100) DEFAULT NULL,
  `courseId` char(20) NOT NULL,
  `name` char(20) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `specialitiesmap` (
  `courseId` char(20) NOT NULL,
  `specialityId` char(20) NOT NULL
);

CREATE TABLE `subjects` (
  `id` char(20) NOT NULL,
  `eearNo` int(3) unsigned zerofill NOT NULL,
  `caption` char(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `subjectsmap` (
  `specialityId` char(20) NOT NULL,
  `subjectId` char(20) NOT NULL,
  `serie` int NOT NULL DEFAULT '1'
);

CREATE TABLE `subjecttoc` (
  `subjectId` char(20) NOT NULL,
  `unit` int NOT NULL,
  `subUnit` int NOT NULL,
  `caption` char(255) DEFAULT NULL,
  `CH` int NOT NULL DEFAULT '2',
  `multiplicador` int DEFAULT '1'
);

CREATE TABLE `users` (
  `login` char(50) NOT NULL,
  `realName` char(255) NOT NULL,
  `password` char(50) NOT NULL,
  `accessLevel` int NOT NULL,
  `lastAccess` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `lastAccessAddress` char(100) NOT NULL,
  `showCourses` int NOT NULL DEFAULT '0',
  `editCourse` int NOT NULL DEFAULT '0',
  `mapCourse` int NOT NULL DEFAULT '0',
  `removeCourse` int NOT NULL DEFAULT '0',
  `showSpecialities` int NOT NULL DEFAULT '0',
  `editSpeciality` int NOT NULL DEFAULT '0',
  `mapSpeciality` int NOT NULL DEFAULT '0',
  `removeSpeciality` int NOT NULL DEFAULT '0',
  `showSubjects` int NOT NULL DEFAULT '0',
  `editSubject` int NOT NULL DEFAULT '0',
  `removeSubject` int NOT NULL DEFAULT '0',
  `showQuestions` int NOT NULL DEFAULT '0',
  `editQuestion` int NOT NULL DEFAULT '0',
  `previewQuestion` int NOT NULL DEFAULT '0',
  `showExams` int NOT NULL DEFAULT '0',
  `showExamDetails` int NOT NULL DEFAULT '0',
  `createExam` int NOT NULL DEFAULT '0',
  `correctExam` int NOT NULL DEFAULT '0',
  `removeExam` int NOT NULL DEFAULT '0',
  `adminUsers` int NOT NULL DEFAULT '0',
  `showLogs` int NOT NULL DEFAULT '0',
  `editSubjectCH` int NOT NULL DEFAULT '0',
  `hyerarchy` char(3) NOT NULL DEFAULT 'CV',
  `revisionOkQuestion` int NOT NULL DEFAULT '0',
  `backupFull` int NOT NULL DEFAULT '0',
  `backupPartial` int NOT NULL DEFAULT '0',
  `is_active` tinyint(1) DEFAULT NULL,
  `is_anonymous` tinyint(1) DEFAULT NULL,
  `is_authenticated` tinyint(1) DEFAULT NULL,
  `deleteQuestion` int DEFAULT NULL,
  PRIMARY KEY (`login`)
);