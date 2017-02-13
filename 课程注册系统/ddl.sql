CREATE DATABASE `homework` /*!40100 DEFAULT CHARACTER SET latin1 */;

CREATE TABLE `student` (
  `student_id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(20) NOT NULL DEFAULT '000',
  `name` varchar(30) NOT NULL,
  `ssn` varchar(15) NOT NULL,
  `birthday` date NOT NULL,
  `graduate_date` date NOT NULL,
  `position` varchar(30) NOT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `student_id_UNIQUE` (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

CREATE TABLE `professor` (
  `professor_id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(20) NOT NULL DEFAULT '000',
  `name` varchar(30) NOT NULL,
  `birthday` date NOT NULL,
  `position` varchar(30) NOT NULL,
  `department` varchar(30) NOT NULL,
  `ssn` varchar(15) NOT NULL,
  PRIMARY KEY (`professor_id`),
  UNIQUE KEY `professor_id_UNIQUE` (`professor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

CREATE TABLE `registrar` (
  `registrar_id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(20) NOT NULL DEFAULT '000',
  `name` varchar(30) NOT NULL,
  PRIMARY KEY (`registrar_id`),
  UNIQUE KEY `registrar_id_UNIQUE` (`registrar_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

CREATE TABLE `course` (
  `course_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `day` varchar(10) NOT NULL,
  `time` varchar(10) NOT NULL,
  `term` varchar(10) NOT NULL,
  `type` varchar(15) NOT NULL,
  PRIMARY KEY (`course_id`),
  UNIQUE KEY `course_id_UNIQUE` (`course_id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;

CREATE TABLE `professor_course` (
  `professor_course_id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` int(11) NOT NULL,
  `professor_id` int(11) NOT NULL,
  `count` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`professor_course_id`),
  UNIQUE KEY `professor_course_id_UNIQUE` (`professor_course_id`),
  KEY `fk_professor_course_course_idx` (`course_id`),
  KEY `fk_professor_course_professor_idx` (`professor_id`),
  CONSTRAINT `fk_professor_course_course` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_professor_course_professor` FOREIGN KEY (`professor_id`) REFERENCES `professor` (`professor_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `s_c_save` (
  `s_c_save_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `professor_course_id` int(11) NOT NULL,
  PRIMARY KEY (`s_c_save_id`),
  UNIQUE KEY `s_c_save_id_UNIQUE` (`s_c_save_id`),
  KEY `fk_s_c_save_stu_idx` (`student_id`),
  KEY `fk_s_c_save_cou_idx` (`professor_course_id`),
  CONSTRAINT `fk_s_c_save_cou` FOREIGN KEY (`professor_course_id`) REFERENCES `professor_course` (`professor_course_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_s_c_save_stu` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `s_c_register` (
  `s_c_register_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `professor_course_id` int(11) NOT NULL,
  `score` varchar(3) NOT NULL DEFAULT 'I',
  PRIMARY KEY (`c_s_register_id`),
  UNIQUE KEY `c_s_register_id_UNIQUE` (`c_s_register_id`),
  KEY `fk_c_s_register_stu_idx` (`student_id`),
  KEY `fk_c_s_register_pro_c_idx` (`professor_course_id`),
  CONSTRAINT `fk_c_s_register_pro_c` FOREIGN KEY (`professor_course_id`) REFERENCES `professor_course` (`professor_course_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_c_s_register_stu` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `registering` (
  `registering_id` int(11) NOT NULL AUTO_INCREMENT,
  `account` int(11) NOT NULL,
  PRIMARY KEY (`registering_id`),
  UNIQUE KEY `registering_id_UNIQUE` (`registering_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE `close_or_not` (
  `close` varchar(3) NOT NULL,
  PRIMARY KEY (`close`),
  UNIQUE KEY `close_UNIQUE` (`close`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;