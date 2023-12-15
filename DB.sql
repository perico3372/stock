SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `DB` DEFAULT CHARACTER SET utf8 ;
USE `DB` ;

-- -----------------------------------------------------
-- Table `DB`.`addresses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB`.`addresses` (
  `addressId` INT(11) NOT NULL AUTO_INCREMENT,
  `streetAddress` VARCHAR(100) NOT NULL,
  `numberAddress` INT(11) NULL DEFAULT NULL,
  `floorAddress` INT(11) NULL DEFAULT NULL,
  `dptoAddress` VARCHAR(10) NULL DEFAULT NULL,
  PRIMARY KEY (`addressId`))
ENGINE = InnoDB
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `DB`.`persons`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB`.`persons` (
  `personId` INT(11) NOT NULL AUTO_INCREMENT,
  `personName` VARCHAR(45) NOT NULL,
  `personEmail` VARCHAR(45) NULL DEFAULT NULL,
  `addresses_addressId` INT(11) NOT NULL,
  PRIMARY KEY (`personId`),
  INDEX `fk_persons_addresses_addressId_idx` (`addresses_addressId` ASC),
  CONSTRAINT `fk_persons_addresses_addressId`
    FOREIGN KEY (`addresses_addressId`)
    REFERENCES `DB`.`addresses` (`addressId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `DB`.`customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB`.`customers` (
  `customerId` INT(11) NOT NULL AUTO_INCREMENT,
  `persons_personId` INT(11) NOT NULL,
  `customerStatus` INT(11) NOT NULL,
  PRIMARY KEY (`customerId`),
  INDEX `fk_clientes_persons_personId_idx` (`persons_personId` ASC),
  CONSTRAINT `fk_clientes_persons_personId`
    FOREIGN KEY (`persons_personId`)
    REFERENCES `DB`.`persons` (`personId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `DB`.`suppliers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB`.`suppliers` (
  `supplierId` INT(11) NOT NULL AUTO_INCREMENT,
  `supplierDescription` VARCHAR(255) NULL DEFAULT NULL,
  `persons_personId` INT(11) NOT NULL,
  `supplierWeb` VARCHAR(200) NULL DEFAULT NULL,
  `supplierStatus` INT(11) NOT NULL,
  PRIMARY KEY (`supplierId`),
  INDEX `fk_suppliers_persons_personId_idx` (`persons_personId` ASC),
  CONSTRAINT `fk_suppliers_persons_personId`
    FOREIGN KEY (`persons_personId`)
    REFERENCES `DB`.`persons` (`personId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `DB`.`transactionType`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB`.`transactionType` (
  `transactionTypeId` INT(11) NOT NULL AUTO_INCREMENT,
  `transactionType` VARCHAR(45) NOT NULL,
  `suppliers_supplierId` INT(11) NULL DEFAULT NULL,
  `customers_customerId` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`transactionTypeId`),
  INDEX `fk_transactionType_customers_customerId_idx` (`customers_customerId` ASC),
  CONSTRAINT `fk_transactionType_customers_customerId`
    FOREIGN KEY (`customers_customerId`)
    REFERENCES `DB`.`customers` (`customerId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  INDEX `fk_transactionType_suppliers_supplierId_idx` (`suppliers_supplierId` ASC),
  CONSTRAINT `fk_transactionType_suppliers_supplierId`
    FOREIGN KEY (`suppliers_supplierId`)
    REFERENCES `DB`.`suppliers` (`supplierId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `DB`.`transactions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB`.`transactions` (
  `transactionId` INT(11) NOT NULL AUTO_INCREMENT,
  `transactionDate` DATE NOT NULL,
  `transactionType_transactionTypeId` INT(11) NOT NULL,
  `transactionStatus` INT(11) NOT NULL,
  PRIMARY KEY (`transactionId`),
  INDEX `fk_transactions_transactionType_transactionTypeId_idx` (`transactionType_transactionTypeId` ASC),
  CONSTRAINT `fk_transactions_transactionType_transactionTypeId`
    FOREIGN KEY (`transactionType_transactionTypeId`)
    REFERENCES `DB`.`transactionType` (`transactionTypeId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `DB`.`brands`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB`.`brands` (
  `brandId` INT(11) NOT NULL AUTO_INCREMENT,
  `brandName` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`brandId`))
ENGINE = InnoDB
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `DB`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB`.`categories` (
  `categoryId` INT(11) NOT NULL AUTO_INCREMENT,
  `categoryName` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`categoryId`))
ENGINE = InnoDB
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;




-- -----------------------------------------------------
-- Table `DB`.`transactionDetail`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB`.`transactionDetail` (
  `transactionDetailId` INT(11) NOT NULL AUTO_INCREMENT,
  `quantity` INT(11) NULL DEFAULT NULL,
  `unitPrice` DOUBLE NULL DEFAULT NULL,
  `products_productId` INT(11) NOT NULL,
  `transactions_transactionId` INT(11) NOT NULL,
  PRIMARY KEY (`transactionDetailId`),
  INDEX `fk_transactionDetail_transactions_transactionId_idx` (`transactions_transactionId` ASC),
  CONSTRAINT `fk_transactionDetail_transactions_transactionId`
    FOREIGN KEY (`transactions_transactionId`)
    REFERENCES `DB`.`transactions` (`transactionId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  INDEX `fk_transactionDetail_products_productId_idx` (`products_productId` ASC),
  CONSTRAINT `fk_transactionDetail_products_productId`
    FOREIGN KEY (`products_productId`)
    REFERENCES `DB`.`products` (`productId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `DB`.`genres`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB`.`generos` (
  `genreId` INT(11) NOT NULL AUTO_INCREMENT,
  `genreDescripcion` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`genreId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `DB`.`modelos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB`.`modelos` (
  `idmodelos` INT(11) NOT NULL AUTO_INCREMENT,
  `descripcion` VARCHAR(50) NOT NULL,
  `marcas_idmarcas` INT(11) NOT NULL,
  PRIMARY KEY (`idmodelos`),
  INDEX `fk_modelos_marcas1_idx` (`marcas_idmarcas` ASC),
  CONSTRAINT `fk_modelos_marcas1`
    FOREIGN KEY (`marcas_idmarcas`)
    REFERENCES `DB`.`marcas` (`idmarcas`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `DB`.`payments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB`.`payments` (
  `paymentId` INT(11) NOT NULL AUTO_INCREMENT,
  `paymentDate` DATE NOT NULL,
  `paymentAmount` DOUBLE NOT NULL,
  `transactionType_transactionTypeId` INT(11) NOT NULL,
  PRIMARY KEY (`paymentId`),
  INDEX `fk_payments_transactionType_transactionTypeId_idx` (`transactionType_transactionTypeId` ASC),
  CONSTRAINT `fk_payments_transactionType_transactionTypeId`
    FOREIGN KEY (`transactionType_transactionTypeId`)
    REFERENCES `DB`.`transactionType` (`transactionTypeId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `DB`.`phones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB`.`phones` (
  `phoneId` INT(11) NOT NULL AUTO_INCREMENT,
  `phoneNumber` BIGINT(20) NOT NULL,
  `phoneType` VARCHAR(45) NOT NULL,
  `persons_personId` INT(11) NOT NULL,
  PRIMARY KEY (`phoneId`),
  INDEX `fk_phones_persons_personId_idx` (`persons_personId` ASC),
  CONSTRAINT `fk_phones_persons_personId`
    FOREIGN KEY (`persons_personId`)
    REFERENCES `DB`.`persons` (`personId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `DB`.`types`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB`.`types` (
  `typesId` INT(11) NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(45) NOT NULL,
  `categories_categoryId` INT(11) NOT NULL,
  PRIMARY KEY (`typesId`),
  INDEX `fk_types_categories1_idx` (`categories_categoryId` ASC),
  CONSTRAINT `fk_types_categories1`
    FOREIGN KEY (`categories_categoryId`)
    REFERENCES `DB`.`categories` (`categoryId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `DB`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB`.`users` (
  `userId` INT(11) NOT NULL AUTO_INCREMENT,
  `userType` VARCHAR(45) NOT NULL,
  `persons_personId` INT(11) NOT NULL,
  `userPassword` VARCHAR(45) NOT NULL,
  `userName` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`userId`),
  INDEX `fk_users_persons_personId_idx` (`persons_personId` ASC),
  CONSTRAINT `fk_users_persons_personId`
    FOREIGN KEY (`persons_personId`)
    REFERENCES `DB`.`persons` (`personId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 0
DEFAULT CHARACTER SET = utf8;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

INSERT INTO DB.addresses (addressId, streetAddress, numberAddress, floorAddress, dptoAddress)  VALUES ( 1, 'crerrito', '3372', '0', '2');
INSERT INTO DB.persons (personName, personEmail, addresses_addressId) VALUES ( 'Perez, Pablo', 'perico3372@gmail.com', 1);
INSERT INTO DB.users (userId, userType, persons_personId, userPassword, userName) VALUES (1, 'ADMINISTRADOR', 1, 'admin', 'admin');

INSERT INTO DB.brands (brandId, brandName)  VALUES ( 1, "moño azul");


INSERT INTO DB.brands (brandId, brandName)  VALUES ( 2, "gaucho");

INSERT INTO DB.categories (categoryId, categoryName)  VALUES ( 1, "frutas");


INSERT INTO DB.categories (categoryId, categoryName)  VALUES ( 2, "verduras");



