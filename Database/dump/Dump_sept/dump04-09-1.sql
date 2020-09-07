-- MySQL Script generated by MySQL Workbench
-- Fri Sep  4 17:59:27 2020
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema all_gid_2
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema all_gid_2
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `all_gid_2` DEFAULT CHARACTER SET utf8 ;
USE `all_gid_2` ;

-- -----------------------------------------------------
-- Table `all_gid_2`.`auth_group`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `all_gid_2`.`auth_group` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name` (`name` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `all_gid_2`.`django_content_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `all_gid_2`.`django_content_type` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `app_label` VARCHAR(100) NOT NULL,
  `model` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label` ASC, `model` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 25
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `all_gid_2`.`auth_permission`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `all_gid_2`.`auth_permission` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `content_type_id` INT(11) NOT NULL,
  `codename` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id` ASC, `codename` ASC) VISIBLE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co`
    FOREIGN KEY (`content_type_id`)
    REFERENCES `all_gid_2`.`django_content_type` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 97
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `all_gid_2`.`auth_group_permissions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `all_gid_2`.`auth_group_permissions` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `group_id` INT(11) NOT NULL,
  `permission_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id` ASC, `permission_id` ASC) VISIBLE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id` ASC) VISIBLE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`
    FOREIGN KEY (`permission_id`)
    REFERENCES `all_gid_2`.`auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id`
    FOREIGN KEY (`group_id`)
    REFERENCES `all_gid_2`.`auth_group` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `all_gid_2`.`auth_user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `all_gid_2`.`auth_user` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `password` VARCHAR(128) NOT NULL,
  `last_login` DATETIME(6) NULL DEFAULT NULL,
  `is_superuser` TINYINT(1) NOT NULL,
  `username` VARCHAR(150) NOT NULL,
  `first_name` VARCHAR(30) NOT NULL,
  `last_name` VARCHAR(150) NOT NULL,
  `email` VARCHAR(254) NOT NULL,
  `is_staff` TINYINT(1) NOT NULL,
  `is_active` TINYINT(1) NOT NULL,
  `date_joined` DATETIME(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username` (`username` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `all_gid_2`.`auth_user_groups`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `all_gid_2`.`auth_user_groups` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `group_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id` ASC, `group_id` ASC) VISIBLE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id` ASC) VISIBLE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id`
    FOREIGN KEY (`group_id`)
    REFERENCES `all_gid_2`.`auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `all_gid_2`.`auth_user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `all_gid_2`.`auth_user_user_permissions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `all_gid_2`.`auth_user_user_permissions` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `permission_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id` ASC, `permission_id` ASC) VISIBLE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id` ASC) VISIBLE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`
    FOREIGN KEY (`permission_id`)
    REFERENCES `all_gid_2`.`auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `all_gid_2`.`auth_user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `all_gid_2`.`django_admin_log`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `all_gid_2`.`django_admin_log` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `action_time` DATETIME(6) NOT NULL,
  `object_id` LONGTEXT NULL DEFAULT NULL,
  `object_repr` VARCHAR(200) NOT NULL,
  `action_flag` SMALLINT(5) UNSIGNED NOT NULL,
  `change_message` LONGTEXT NOT NULL,
  `content_type_id` INT(11) NULL DEFAULT NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id` ASC) VISIBLE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id` ASC) VISIBLE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co`
    FOREIGN KEY (`content_type_id`)
    REFERENCES `all_gid_2`.`django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `all_gid_2`.`auth_user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `all_gid_2`.`django_migrations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `all_gid_2`.`django_migrations` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `app` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `applied` DATETIME(6) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 17
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `all_gid_2`.`django_session`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `all_gid_2`.`django_session` (
  `session_key` VARCHAR(40) NOT NULL,
  `session_data` LONGTEXT NOT NULL,
  `expire_date` DATETIME(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  INDEX `django_session_expire_date_a5c62663` (`expire_date` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `all_gid_2`.`mnt_classes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `all_gid_2`.`mnt_classes` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `type` ENUM('CL', 'GO') NULL DEFAULT NULL,
  `class_subtype` VARCHAR(45) NULL DEFAULT NULL,
  `text` VARCHAR(45) NULL DEFAULT NULL,
  `explanation` VARCHAR(45) NULL DEFAULT NULL,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `all_gid_2`.`mnt_products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `all_gid_2`.`mnt_products` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `brand` VARCHAR(45) NULL DEFAULT NULL,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `screen_size` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `all_gid_2`.`mnt_products_has_mnt_classes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `all_gid_2`.`mnt_products_has_mnt_classes` (
  `fk_products` INT(11) NOT NULL,
  `fk_classes` INT(11) NOT NULL,
  `id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`fk_products`, `fk_classes`),
  INDEX `fk_Mnt_products_has_Mnt_classes_Mnt_products1_idx` (`fk_products` ASC) VISIBLE,
  INDEX `fk_classes_idx` (`fk_classes` ASC) VISIBLE,
  CONSTRAINT `fk_mnt_classes`
    FOREIGN KEY (`fk_classes`)
    REFERENCES `all_gid_2`.`mnt_classes` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_mnt_products`
    FOREIGN KEY (`fk_products`)
    REFERENCES `all_gid_2`.`mnt_products` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `all_gid_2`.`mnt_vardata`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `all_gid_2`.`mnt_vardata` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `month` DATE NULL DEFAULT NULL,
  `sales_units` INT(11) NULL DEFAULT NULL,
  `price_rur` FLOAT NULL DEFAULT NULL,
  `fk_products` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_mnt_products_name_idx` (`fk_products` ASC) VISIBLE,
  CONSTRAINT `fk_mnt_products_name`
    FOREIGN KEY (`fk_products`)
    REFERENCES `all_gid_2`.`mnt_products` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `all_gid_2`.`nb_classes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `all_gid_2`.`nb_classes` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `type` ENUM('CL', 'GO') NULL DEFAULT NULL,
  `class_subtype` VARCHAR(45) NULL DEFAULT NULL,
  `text` VARCHAR(100) NULL DEFAULT NULL,
  `explanation` VARCHAR(256) NULL DEFAULT NULL,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 37
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `all_gid_2`.`nb_products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `all_gid_2`.`nb_products` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `brand` VARCHAR(45) NULL DEFAULT NULL,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `cluster` VARCHAR(45) NULL DEFAULT NULL,
  `target_market` ENUM('Commercial', 'Consumer') NULL DEFAULT NULL,
  `cpu_vendor` VARCHAR(45) NULL DEFAULT NULL,
  `base_platform` VARCHAR(45) NULL DEFAULT NULL,
  `gpu_list` VARCHAR(45) NULL DEFAULT NULL,
  `screen_size` VARCHAR(45) NULL DEFAULT NULL,
  `screen_resulution_list` VARCHAR(45) NULL DEFAULT NULL,
  `touchscreen` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 4385
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `all_gid_2`.`nb_products_has_nb_classes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `all_gid_2`.`nb_products_has_nb_classes` (
  `fk_products` INT(11) NOT NULL AUTO_INCREMENT,
  `fk_classes` INT(11) NOT NULL,
  `id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`fk_products`, `fk_classes`),
  INDEX `fk_Nb_products_has_Nb_classes_Nb_products1_idx` (`fk_products` ASC) VISIBLE,
  INDEX `fk_classes_idx` (`fk_classes` ASC) VISIBLE,
  CONSTRAINT `fk_nb_classes`
    FOREIGN KEY (`fk_classes`)
    REFERENCES `all_gid_2`.`nb_classes` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_nb_products`
    FOREIGN KEY (`fk_products`)
    REFERENCES `all_gid_2`.`nb_products` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 4385
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `all_gid_2`.`nb_vardata`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `all_gid_2`.`nb_vardata` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `month` DATE NULL DEFAULT NULL,
  `sales_units` INT(11) NULL DEFAULT NULL,
  `price_rur` FLOAT NULL DEFAULT NULL,
  `fk_products` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Nb_products_vardata_idx` (`fk_products` ASC) VISIBLE,
  CONSTRAINT `fk_Nb_products_vardata`
    FOREIGN KEY (`fk_products`)
    REFERENCES `all_gid_2`.`nb_products` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 6335
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
