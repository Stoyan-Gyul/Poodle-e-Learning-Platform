-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema e-learning
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema e-learning
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `e-learning` DEFAULT CHARACTER SET utf8mb4 ;
USE `e-learning` ;

-- -----------------------------------------------------
-- Table `e-learning`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(100) NOT NULL,
  `password` VARCHAR(500) NOT NULL,
  `first_name` VARCHAR(45) NULL DEFAULT NULL,
  `last_name` VARCHAR(45) NULL DEFAULT NULL,
  `role` VARCHAR(45) NULL DEFAULT NULL,
  `verification_token` VARCHAR(100) NULL DEFAULT NULL,
  `is_verified` TINYINT(4) NULL DEFAULT NULL,
  `is_approved` TINYINT(4) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `e-learning`.`teachers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`teachers` (
  `users_id` INT(11) NOT NULL,
  `phone_number` VARCHAR(45) NULL DEFAULT NULL,
  `linked_in_account` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`users_id`),
  INDEX `fk_Teachers_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_Teachers_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `e-learning`.`users` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `e-learning`.`courses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`courses` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NULL DEFAULT NULL,
  `description` VARCHAR(500) NULL DEFAULT NULL,
  `home_page_pic` BLOB NULL DEFAULT NULL,
  `owner_id` INT(11) NOT NULL,
  `is_active` TINYINT(1) NULL DEFAULT NULL,
  `is_premium` TINYINT(1) NOT NULL,
  `course_rating` DECIMAL(10,1) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) VISIBLE,
  INDEX `fk_courses_Teachers1_idx` (`owner_id` ASC) VISIBLE,
  CONSTRAINT `fk_courses_Teachers1`
    FOREIGN KEY (`owner_id`)
    REFERENCES `e-learning`.`teachers` (`users_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `e-learning`.`objectives`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`objectives` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `e-learning`.`courses_have_objectives`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`courses_have_objectives` (
  `objectives_id` INT(11) NOT NULL,
  `courses_id` INT(11) NOT NULL,
  PRIMARY KEY (`objectives_id`, `courses_id`),
  INDEX `fk_objectives_has_courses_courses1_idx` (`courses_id` ASC) VISIBLE,
  INDEX `fk_objectives_has_courses_objectives1_idx` (`objectives_id` ASC) VISIBLE,
  CONSTRAINT `fk_objectives_has_courses_courses1`
    FOREIGN KEY (`courses_id`)
    REFERENCES `e-learning`.`courses` (`id`),
  CONSTRAINT `fk_objectives_has_courses_objectives1`
    FOREIGN KEY (`objectives_id`)
    REFERENCES `e-learning`.`objectives` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `e-learning`.`tags`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`tags` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `expertise_area` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `e-learning`.`courses_have_tags`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`courses_have_tags` (
  `courses_id` INT(11) NOT NULL,
  `tags_id` INT(11) NOT NULL,
  PRIMARY KEY (`courses_id`, `tags_id`),
  INDEX `fk_Courses_has_Tags_Tags1_idx` (`tags_id` ASC) VISIBLE,
  INDEX `fk_Courses_has_Tags_Courses_idx` (`courses_id` ASC) VISIBLE,
  CONSTRAINT `fk_Courses_has_Tags_Courses`
    FOREIGN KEY (`courses_id`)
    REFERENCES `e-learning`.`courses` (`id`),
  CONSTRAINT `fk_Courses_has_Tags_Tags1`
    FOREIGN KEY (`tags_id`)
    REFERENCES `e-learning`.`tags` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `e-learning`.`sections`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`sections` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NULL DEFAULT NULL,
  `content` LONGTEXT NULL DEFAULT NULL,
  `description` VARCHAR(45) NULL DEFAULT NULL,
  `external_link` VARCHAR(45) NULL DEFAULT NULL,
  `courses_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`, `courses_id`),
  INDEX `fk_sections_courses1_idx` (`courses_id` ASC) VISIBLE,
  CONSTRAINT `fk_sections_courses1`
    FOREIGN KEY (`courses_id`)
    REFERENCES `e-learning`.`courses` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `e-learning`.`users_have_courses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`users_have_courses` (
  `users_id` INT(11) NOT NULL,
  `courses_id` INT(11) NOT NULL,
  `status` TINYINT(3) NULL DEFAULT NULL,
  `rating` INT(11) NULL DEFAULT NULL,
  `progress` TINYINT(100) NULL DEFAULT NULL,
  PRIMARY KEY (`users_id`, `courses_id`),
  INDEX `fk_users_has_Courses_Courses1_idx` (`courses_id` ASC) VISIBLE,
  INDEX `fk_users_has_Courses_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_Courses_Courses1`
    FOREIGN KEY (`courses_id`)
    REFERENCES `e-learning`.`courses` (`id`),
  CONSTRAINT `fk_users_has_Courses_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `e-learning`.`users` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `e-learning`.`users_has_sections`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`users_has_sections` (
  `users_id` INT(11) NOT NULL,
  `sections_id` INT(11) NOT NULL,
  PRIMARY KEY (`users_id`, `sections_id`),
  INDEX `fk_users_has_sections_sections1_idx` (`sections_id` ASC) VISIBLE,
  INDEX `fk_users_has_sections_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_sections_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `e-learning`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_sections_sections1`
    FOREIGN KEY (`sections_id`)
    REFERENCES `e-learning`.`sections` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
