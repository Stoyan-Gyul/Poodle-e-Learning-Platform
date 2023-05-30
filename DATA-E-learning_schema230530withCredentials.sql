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
AUTO_INCREMENT = 6
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
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `e-learning`.`objectives`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`objectives` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
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
AUTO_INCREMENT = 2
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
AUTO_INCREMENT = 6
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


-- -----------------------------------------------------
-- Table `e-learning`.`credentials`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `e-learning`.`credentials` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(100) NOT NULL,
  `password` VARCHAR(500) NOT NULL,
  `users_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_credentials_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_credentials_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `e-learning`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- Insert data into the courses table
INSERT INTO courses (id, title, description, home_page_pic, owner_id, is_active, is_premium, course_rating)
VALUES
    (1, 'Core Python', 'This is core module', '1', 1, 0, 8.0),
    (2, 'OOP', 'This is OOP module', '1', 1, 1, 6.5),
    (4, 'General Python', 'This is general', '1', 1, 0, 7.0);


-- Insert data into the courses_have_objectives table
INSERT INTO courses_have_objectives (objectives_id, courses_id)
VALUES
    (1, 1),
    (1, 2),
    (2, 4);


-- Insert data into the courses_have_tags table
INSERT INTO courses_have_tags (courses_id, tags_id)
VALUES
    (1, 1),
    (2, 1),
    (4, 1);


-- Insert data into the objectives table
INSERT INTO objectives (id, description)
VALUES
    (1, 'Learn software'),
    (2, 'General view');

-- Insert data into the sections table
INSERT INTO sections (id, title, content, description, external_link, courses_id)
VALUES
    (1, 'Basics', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse lobortis velit id orci vestibulum mollis eget in lectus. Vestibulum massa lorem, volutpat a augue id, egestas tristique mi. Suspendisse potenti. Suspendisse iaculis tincidunt lacus. Ves...', 'Explain the basics', 'any', 1),
    (2, 'Tuples', 'Integer gravida, lectus non interdum rutrum, metus ex tempor orci, id venenatis lectus odio imperdiet nibh. Integer pellentesque neque in ultrices consectetur. Etiam luctus magna vitae nisl maximus sodales. Maecenas eget justo efficitur quam effi...', 'Explain tuples', 'any', 1),
    (3, 'Dicts', 'Vivamus lorem elit, luctus quis neque ut, congue venenatis purus. In rutrum ullamcorper nisl, at euismod urna aliquam sed. Curabitur ut velit magna. Donec quis sem vel felis pretium accumsan. Donec tempus ullamcorper risus, sed tristique orci. Class ap...', 'Explain dictionaries', 'any', 1),
    (4, 'Basic OOP', 'Aenean commodo bibendum mi id efficitur. Nam auctor, mauris eget blandit lacinia, turpis erat mattis felis, nec feugiat est justo eget leo. Suspendisse potenti. Cras sodales sapien lacus, vel pretium nunc tempus at. Maecenas sed ex quis sapien ornare g...', 'Explain basic OOP', 'any', 2),
    (5, 'Abstractions', 'Morbi ut arcu risus. Phasellus porta commodo lorem, vitae faucibus ipsum commodo in. Aliquam ornare, nunc vel luctus vulputate, ipsum dui gravida leo, dapibus euismod ligula nisi non dolor. Sed sodales ante est, ac scelerisque elit dignissim sed. Sed in...', 'Explain Abstraction', 'any', 2);

-- Insert data into the tags table
INSERT INTO tags (id, expertise_area)
VALUES
    (1, 'software development');

-- Insert data into the teachers table
INSERT INTO teachers (users_id, phone_number, linked_in_account)
VALUES
    (1, '888345600', 'www.linkedin.com/aliceparker100');

-- Insert data into the users table
INSERT INTO users (id, email, password, first_name, last_name, role, verification_token, is_verified, is_approved)
VALUES
    (1, 'alice@abv.bg', '$2b$12$Xag4rXZGOJrNkwRb32N6s.nscNQFlIfJSYhJXgHrFebVGgjj8Ve9K', 'Alice', 'Parker100', 'teacher', NULL, 0, 1),
    (2, 'steven@abv.bg', '$2b$12$ooercgclJ9NziweYJC8nSunM8LJ43PE0EvxTv8cul/7kdNTolGqMm', 'Steven', 'Parker100', 'student', NULL, 0, 1),
    (3, 'steven1@abv.bg', '$2b$12$yUT0WH0qklpI15Y7jXqyVe3.j6DCJVo4HsjrYBdIoLTB684/YLBTu', 'Steven1', 'Parker1', 'student', 'e399f595-5312-4ba1-bb74-64c46dc5bcd2', 1, 1),
    (4, 'steven2@abv.bg', '$2b$12$3cUVOilSyrfMNZ5LjPUKT.68P/OY7qVYL/VrVM6mpWUTx192xza8K', 'Steven2', 'Parker2', 'student', '77dc7699-4e3f-448a-9133-fb676d8b373b', 1, 0),
    (5, 'admin@abv.bg', '$2b$12$at3uULHSgb2zV6nrIJLP7uuSITMvZbMw68gA54Lfpy9OvV7saevaO', 'Admin', 'Adminov', 'admin', '77dc7699-4e3f-448a-9133-fb676d8b373b', 0, 1);

-- Insert data into the users_have_courses table
INSERT INTO users_have_courses (users_id, courses_id, status, rating, progress)
VALUES
    (2, 1, 1, 8, NULL),
    (2, 2, 1, 6, NULL),
    (3, 2, 1, 7, NULL),
    (3, 4, 1, 7, NULL);

