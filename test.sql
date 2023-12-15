SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `test` DEFAULT CHARACTER SET utf8 ;
USE `test` ;


-- -----------------------------------------------------
-- Table `DB`.`suppliers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `test`.`suppliers` (
  `supplierId` INT(11) NOT NULL AUTO_INCREMENT,
  `supplierName` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`supplierId`))
ENGINE = InnoDB
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `DB`.`products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `test`.`products` (
  `productId` INT(11) NOT NULL AUTO_INCREMENT,
  `nameProduct` VARCHAR(45) NOT NULL,
  `suppliers_supplierId` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`productId`),  
  CONSTRAINT `fkProductssuppliers1`
    FOREIGN KEY (`suppliers_supplierId`)
    REFERENCES `test`.`suppliers` (`supplierId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 28
DEFAULT CHARACTER SET = utf8;

INSERT INTO test.suppliers (supplierId, supplierName) VALUES ( 1, "jorge");

INSERT INTO test.suppliers (supplierId, supplierName) VALUES ( 2, "betiana");



