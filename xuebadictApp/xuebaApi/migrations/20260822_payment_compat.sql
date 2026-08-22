-- 支付兼容模块增量迁移。
-- 仅创建 legacy /api/v1/payment 所需表，不修改现有 membership_* 商业表。
-- 执行前请确认当前数据库已存在 users(id varchar(32))。

CREATE TABLE IF NOT EXISTS `payment_orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_no` varchar(64) NOT NULL,
  `trade_no` varchar(128) DEFAULT NULL,
  `user_id` varchar(32) NOT NULL,
  `payment_method` varchar(20) NOT NULL,
  `payment_scene` varchar(50) NOT NULL,
  `product_name` varchar(200) NOT NULL,
  `product_desc` varchar(500) DEFAULT NULL,
  `total_amount` int NOT NULL,
  `paid_amount` int DEFAULT 0,
  `status` int DEFAULT 0,
  `created_at` datetime DEFAULT NULL,
  `paid_at` datetime DEFAULT NULL,
  `expired_at` datetime DEFAULT NULL,
  `cancelled_at` datetime DEFAULT NULL,
  `client_ip` varchar(50) DEFAULT NULL,
  `extra_data` text,
  `callback_data` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_payment_orders_order_no` (`order_no`),
  UNIQUE KEY `uk_payment_orders_trade_no` (`trade_no`),
  KEY `idx_payment_orders_user_id` (`user_id`),
  CONSTRAINT `fk_payment_orders_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `payment_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_no` varchar(64) NOT NULL,
  `action` varchar(50) NOT NULL,
  `message` text,
  `request_data` text,
  `response_data` text,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_payment_logs_order_no` (`order_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `vip_memberships` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(32) NOT NULL,
  `vip_type` varchar(20) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 0,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_vip_memberships_user_id` (`user_id`),
  CONSTRAINT `fk_vip_memberships_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `user_coins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(32) NOT NULL,
  `total_coins` int DEFAULT 0,
  `used_coins` int DEFAULT 0,
  `available_coins` int DEFAULT 0,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_coins_user_id` (`user_id`),
  CONSTRAINT `fk_user_coins_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
