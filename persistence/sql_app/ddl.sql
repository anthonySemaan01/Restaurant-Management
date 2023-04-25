CREATE TABLE `Manager`
(
    `manager_id`    INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `restaurant_id` INT             NOT NULL,
    `email`         VARCHAR(255)    NOT NULL,
    `password`      VARCHAR(255)    NOT NULL,
    `phone_nb`      VARCHAR(255)    NOT NULL,
    `first_name`    VARCHAR(255)    NOT NULL,
    `last_name`     VARCHAR(255)    NOT NULL,
    `date_of_birth` DATETIME        NOT NULL,
    `picture`       JSON
);

CREATE TABLE `Staff`
(
    `staff_id`      INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `manager_id`    INT             NOT NULL,
    `restaurant_id` INT             NOT NULL,
    `email`         VARCHAR(255)    NOT NULL,
    `password`      VARCHAR(255)    NOT NULL,
    `phone_nb`      VARCHAR(255)    NOT NULL,
    `first_name`    VARCHAR(255)    NOT NULL,
    `last_name`     VARCHAR(255)    NOT NULL,
    `date_of_birth` DATETIME        NOT NULL,
    `picture`       JSON
);

CREATE TABLE `Order`
(
    `order_id`   INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `table_id`   INT             NOT NULL,
    `id_init`    INT             NOT NULL,
    `id_fin`     INT             NOT NULL,
    `status`     ENUM ('In Progress', 'Completed', 'Canceled') NOT NULL,
    `time_init`  DATETIME        NOT NULL,
    `time_fin`   DATETIME,
    `edits_made` JSON,
    `proc_type`  VARCHAR(255),
    `fin_type`   VARCHAR(255)
);

CREATE TABLE `OrderDish`
(
    `order_id` INT NOT NULL,
    `dish_id`  INT NOT NULL,
    PRIMARY KEY (`order_id`, `dish_id`)
);

CREATE TABLE `Dish`
(
    `dish_id`       INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `restaurant_id` INT             NOT NULL,
    `name`          VARCHAR(255)    NOT NULL,
    `description`   VARCHAR(255)    NOT NULL,
    `price`         DECIMAL(10, 2)  NOT NULL
);

CREATE TABLE `Reservation`
(
    `reservation_id`   INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `table_id`         INT             NOT NULL,
    `customer_id`      INT             NOT NULL,
    `id_proc`          INT             NOT NULL,
    `reservation_time` DATETIME        NOT NULL,
    `status`           ENUM ('Pending', 'Confirmed', 'Canceled by Customer', 'Canceled by Restaurant') NOT NULL,
    `proc_type`        VARCHAR(255)
);

CREATE TABLE `Table`
(
    `table_id`      INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `restaurant_id` INT             NOT NULL,
    `capacity`      INT             NOT NULL,
    `location`      VARCHAR(255)    NOT NULL
);

CREATE TABLE `Restaurant`
(
    `restaurant_id`      INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `manager_id`         INT             NOT NULL,
    `name`               VARCHAR(255)    NOT NULL,
    `address`            VARCHAR(255)    NOT NULL,
    `phone_number`       VARCHAR(255)    NOT NULL,
    `cuisine`            ENUM ('American', 'Chinese', 'French', 'Indian', 'Italian', 'Japanese', 'Mexican', 'Middle Eastern') NOT NULL,
    `website`            VARCHAR(255),
    `social_media_pages` VARCHAR(255),
    `hours_of_operation` VARCHAR(255),
    `images`             JSON
);

CREATE TABLE `Review`
(
    `review_id`     INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `restaurant_id` INT             NOT NULL,
    `customer_id`   INT             NOT NULL,
    `rating`        ENUM ('0', '0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5') NOT NULL,
    `comment`       TEXT
);

CREATE TABLE `Customer`
(
    `customer_id`   INT(10) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `email`         VARCHAR(255) NOT NULL,
    `password`      VARCHAR(255) NOT NULL,
    `phone_nb`      VARCHAR(20)  NOT NULL,
    `first_name`    VARCHAR(255) NOT NULL,
    `last_name`     VARCHAR(255) NOT NULL,
    `picture`       VARCHAR(255),
    `date_of_birth` DATETIME     NOT NULL
);

ALTER TABLE `Manager`
    ADD FOREIGN KEY (`restaurant_id`) REFERENCES `Restaurant` (`restaurant_id`);

ALTER TABLE `Staff`
    ADD FOREIGN KEY (`manager_id`) REFERENCES `Manager` (`manager_id`);

ALTER TABLE `Staff`
    ADD FOREIGN KEY (`restaurant_id`) REFERENCES `Restaurant` (`restaurant_id`);

ALTER TABLE `Order`
    ADD FOREIGN KEY (`table_id`) REFERENCES `Table` (`table_id`);

ALTER TABLE `Order`
    ADD FOREIGN KEY (`id_init`) REFERENCES `Staff` (`staff_id`);

ALTER TABLE `Order`
    ADD FOREIGN KEY (`id_fin`) REFERENCES `Staff` (`staff_id`);

ALTER TABLE `Dish`
    ADD FOREIGN KEY (`restaurant_id`) REFERENCES `Restaurant` (`restaurant_id`);

ALTER TABLE `Reservation`
    ADD FOREIGN KEY (`table_id`) REFERENCES `Table` (`table_id`);

ALTER TABLE `Reservation`
    ADD FOREIGN KEY (`customer_id`) REFERENCES `Customer` (`customer_id`);

ALTER TABLE `Reservation`
    ADD FOREIGN KEY (`id_proc`) REFERENCES `Staff` (`staff_id`);

ALTER TABLE `Table`
    ADD FOREIGN KEY (`restaurant_id`) REFERENCES `Restaurant` (`restaurant_id`);

ALTER TABLE `Restaurant`
    ADD FOREIGN KEY (`manager_id`) REFERENCES `Manager` (`manager_id`);

ALTER TABLE `Review`
    ADD FOREIGN KEY (`restaurant_id`) REFERENCES `Restaurant` (`restaurant_id`);

ALTER TABLE `Review`
    ADD FOREIGN KEY (`customer_id`) REFERENCES `Customer` (`customer_id`);

ALTER TABLE `OrderDish`
    ADD FOREIGN KEY (`order_id`) REFERENCES `Order` (`order_id`);

ALTER TABLE `OrderDish`
    ADD FOREIGN KEY (`dish_id`) REFERENCES `Dish` (`dish_id`);
