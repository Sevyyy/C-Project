CREATE DATABASE `Classroom_Manage` /*!40100 DEFAULT CHARACTER SET latin1 */;

CREATE TABLE `Application` (
  `application_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_type` enum('s','p','e') NOT NULL,
  `user_id` int(11) NOT NULL,
  `size` enum('big','medium big','medium small','small') NOT NULL,
  `week` int(11) NOT NULL,
  `day` enum('mon','tue','wed','thu','fri','sat','sun') NOT NULL,
  `course_begin` int(11) NOT NULL,
  `course_end` int(11) NOT NULL,
  `reason` varchar(100) NOT NULL,
  `vertify` tinyint(4) NOT NULL DEFAULT '0',
  `classroom_id` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`application_id`),
  UNIQUE KEY `application_id_UNIQUE` (`application_id`),
  KEY `fk_applocation_classroom_idx` (`classroom_id`),
  CONSTRAINT `fk_applocation_classroom` FOREIGN KEY (`classroom_id`) REFERENCES `Classroom` (`classroom_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=latin1;

CREATE TABLE `Classroom` (
  `classroom_id` varchar(5) NOT NULL,
  `size` enum('big','medium big','medium small','small') NOT NULL,
  `facility` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`classroom_id`),
  UNIQUE KEY `classroom_id_UNIQUE` (`classroom_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Course` (
  `course_id` int(11) NOT NULL AUTO_INCREMENT,
  `course_name` varchar(30) NOT NULL,
  `professor_id` int(11) NOT NULL,
  `classroom_id` varchar(5) NOT NULL,
  `week_begin` int(11) NOT NULL,
  `week_end` int(11) NOT NULL,
  `day` int(11) NOT NULL,
  `course_begin` int(11) NOT NULL,
  `course_end` int(11) NOT NULL,
  PRIMARY KEY (`course_id`),
  UNIQUE KEY `course_id_UNIQUE` (`course_id`),
  KEY `fk_course_professor_idx` (`professor_id`),
  KEY `fk_course_classroom_idx` (`classroom_id`),
  CONSTRAINT `fk_course_classroom` FOREIGN KEY (`classroom_id`) REFERENCES `Classroom` (`classroom_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_course_professor` FOREIGN KEY (`professor_id`) REFERENCES `Professor` (`professor_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

CREATE TABLE `External` (
  `external_id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(20) NOT NULL DEFAULT '000',
  `name` varchar(30) NOT NULL,
  `email` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`external_id`),
  UNIQUE KEY `external_id_UNIQUE` (`external_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

CREATE TABLE `Manager` (
  `manager_id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(20) NOT NULL DEFAULT '000',
  `name` varchar(30) NOT NULL,
  PRIMARY KEY (`manager_id`),
  UNIQUE KEY `manager_id_UNIQUE` (`manager_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

CREATE TABLE `Professor` (
  `professor_id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(20) NOT NULL DEFAULT '000',
  `name` varchar(30) NOT NULL,
  `email` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`professor_id`),
  UNIQUE KEY `professor_id_UNIQUE` (`professor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

CREATE TABLE `Report` (
  `report_id` int(11) NOT NULL AUTO_INCREMENT,
  `statement` varchar(100) NOT NULL,
  `vertify` tinyint(4) NOT NULL DEFAULT '0',
  `classroom_id` varchar(5) NOT NULL,
  PRIMARY KEY (`report_id`),
  KEY `fk_report_classroom_idx` (`classroom_id`),
  CONSTRAINT `fk_report_classroom` FOREIGN KEY (`classroom_id`) REFERENCES `Classroom` (`classroom_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

CREATE TABLE `Sparetime` (
  `classroom_id` varchar(5) NOT NULL,
  `week` int(11) NOT NULL,
  `mon` int(11) NOT NULL DEFAULT '0',
  `tue` int(11) NOT NULL DEFAULT '0',
  `wed` int(11) NOT NULL DEFAULT '0',
  `thu` int(11) NOT NULL DEFAULT '0',
  `fri` int(11) NOT NULL DEFAULT '0',
  `sat` int(11) NOT NULL DEFAULT '0',
  `sun` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`classroom_id`,`week`),
  CONSTRAINT `fk_sparetime_classroom` FOREIGN KEY (`classroom_id`) REFERENCES `Classroom` (`classroom_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Student` (
  `student_id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(20) NOT NULL DEFAULT '000',
  `name` varchar(30) NOT NULL,
  `grade` enum('1','2','3','4') NOT NULL,
  `major` varchar(100) NOT NULL,
  `email` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `student_id_UNIQUE` (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

CREATE TABLE `Student_course` (
  `s_c_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  PRIMARY KEY (`s_c_id`),
  UNIQUE KEY `s_c_id_UNIQUE` (`s_c_id`),
  KEY `fk_s_c_student_idx` (`student_id`),
  KEY `fk_s_c_course_idx` (`course_id`),
  CONSTRAINT `fk_s_c_course` FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_s_c_student` FOREIGN KEY (`student_id`) REFERENCES `Student` (`student_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

