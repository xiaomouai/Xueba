-- 添加会员系统、闯关和听写模块的数据表
-- 使用方法: mysql -u root -p xuebadict < add_new_tables.sql

USE xuebadict;

-- 1. 会员套餐表
CREATE TABLE IF NOT EXISTS `membership_plans` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(50) NOT NULL COMMENT '套餐名称',
  `plan_type` VARCHAR(20) NOT NULL COMMENT '套餐类型:month/season/year/lifetime',
  `duration_days` INT DEFAULT 0 COMMENT '时长(天),0表示永久',
  `price` DECIMAL(10,2) NOT NULL COMMENT '价格',
  `original_price` DECIMAL(10,2) COMMENT '原价',
  `description` VARCHAR(500) COMMENT '描述',
  `features` TEXT COMMENT '特权列表,逗号分隔',
  `is_recommended` TINYINT(1) DEFAULT 0 COMMENT '是否推荐',
  `discount_label` VARCHAR(50) COMMENT '折扣标签',
  `sort_order` INT DEFAULT 0 COMMENT '排序',
  `is_active` TINYINT(1) DEFAULT 1 COMMENT '是否启用',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_plan_type` (`plan_type`),
  INDEX `idx_is_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会员套餐表';

-- 2. 用户会员表
CREATE TABLE IF NOT EXISTS `user_memberships` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL COMMENT '用户ID',
  `membership_type` VARCHAR(20) DEFAULT 'free' COMMENT '会员类型:free/month/season/year/lifetime',
  `expire_time` DATETIME COMMENT '过期时间,NULL表示永久',
  `status` VARCHAR(20) DEFAULT 'active' COMMENT '状态:active/expired/cancelled',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `uk_user_id` (`user_id`),
  INDEX `idx_user_status` (`user_id`, `status`),
  INDEX `idx_expire_time` (`expire_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户会员表';

-- 3. 会员订单表
CREATE TABLE IF NOT EXISTS `membership_orders` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_no` VARCHAR(64) NOT NULL COMMENT '订单号',
  `user_id` INT NOT NULL COMMENT '用户ID',
  `plan_id` INT NOT NULL COMMENT '套餐ID',
  `original_price` DECIMAL(10,2) NOT NULL COMMENT '原价',
  `actual_price` DECIMAL(10,2) NOT NULL COMMENT '实付金额',
  `payment_method` VARCHAR(20) DEFAULT 'alipay' COMMENT '支付方式:alipay/wechat',
  `payment_no` VARCHAR(64) COMMENT '第三方支付订单号',
  `status` VARCHAR(20) DEFAULT 'pending' COMMENT '状态:pending/paid/cancelled/refunded',
  `paid_time` DATETIME COMMENT '支付时间',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `uk_order_no` (`order_no`),
  INDEX `idx_user_id` (`user_id`),
  INDEX `idx_status` (`status`),
  INDEX `idx_payment_no` (`payment_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会员订单表';

-- 4. 会员权益表
CREATE TABLE IF NOT EXISTS `membership_benefits` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(50) NOT NULL COMMENT '权益名称',
  `description` VARCHAR(500) COMMENT '权益描述',
  `benefit_type` VARCHAR(50) NOT NULL COMMENT '权益类型',
  `benefit_value` VARCHAR(100) COMMENT '权益值',
  `membership_type` VARCHAR(20) NOT NULL COMMENT '适用会员类型',
  `icon` VARCHAR(50) COMMENT '图标',
  `is_active` TINYINT(1) DEFAULT 1 COMMENT '是否启用',
  `sort_order` INT DEFAULT 0 COMMENT '排序',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_membership_type` (`membership_type`),
  INDEX `idx_benefit_type` (`benefit_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会员权益表';

-- 5. 用户会员权益关联表
CREATE TABLE IF NOT EXISTS `user_membership_benefits` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL COMMENT '用户ID',
  `benefit_id` INT NOT NULL COMMENT '权益ID',
  `is_active` TINYINT(1) DEFAULT 1 COMMENT '是否启用',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_user_benefit` (`user_id`, `benefit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户会员权益关联表';

-- 6. 闯关表
CREATE TABLE IF NOT EXISTS `challenges` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL COMMENT '用户ID',
  `word_book_id` INT NOT NULL COMMENT '词书ID',
  `difficulty` VARCHAR(20) NOT NULL DEFAULT 'easy' COMMENT '难度:easy/medium/hard',
  `total_questions` INT DEFAULT 0 COMMENT '总题数',
  `answered_questions` INT DEFAULT 0 COMMENT '已答题数',
  `correct_answers` INT DEFAULT 0 COMMENT '正确答案数',
  `score` INT DEFAULT 0 COMMENT '得分',
  `status` VARCHAR(20) DEFAULT 'in_progress' COMMENT '状态:in_progress/completed',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `completed_at` DATETIME COMMENT '完成时间',
  INDEX `idx_user_id` (`user_id`),
  INDEX `idx_user_status` (`user_id`, `status`),
  INDEX `idx_word_book_id` (`word_book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='闯关表';

-- 7. 闯关记录表
CREATE TABLE IF NOT EXISTS `challenge_records` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL COMMENT '用户ID',
  `challenge_id` INT NOT NULL COMMENT '闯关ID',
  `word_book_id` INT NOT NULL COMMENT '词书ID',
  `difficulty` VARCHAR(20) NOT NULL COMMENT '难度',
  `score` INT DEFAULT 0 COMMENT '得分',
  `total_questions` INT DEFAULT 0 COMMENT '总题数',
  `correct_answers` INT DEFAULT 0 COMMENT '正确答案数',
  `time_spent` INT DEFAULT 0 COMMENT '耗时(秒)',
  `is_passed` TINYINT(1) DEFAULT 0 COMMENT '是否通过',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_user_id` (`user_id`),
  INDEX `idx_user_created` (`user_id`, `created_at`),
  INDEX `idx_word_book_id` (`word_book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='闯关记录表';

-- 8. 闯关答题表
CREATE TABLE IF NOT EXISTS `challenge_answers` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `challenge_id` INT NOT NULL COMMENT '闯关ID',
  `word_id` INT NOT NULL COMMENT '单词ID',
  `user_answer` VARCHAR(255) COMMENT '用户答案',
  `is_correct` TINYINT(1) DEFAULT 0 COMMENT '是否正确',
  `time_spent` INT DEFAULT 0 COMMENT '答题耗时(秒)',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_challenge_id` (`challenge_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='闯关答题表';

-- 9. 听写表
CREATE TABLE IF NOT EXISTS `dictations` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL COMMENT '用户ID',
  `word_book_id` INT NOT NULL COMMENT '词书ID',
  `mode` VARCHAR(20) NOT NULL DEFAULT 'sequential' COMMENT '模式:sequential/random/wrong_words',
  `total_words` INT DEFAULT 0 COMMENT '总单词数',
  `completed_words` INT DEFAULT 0 COMMENT '已完成数',
  `correct_words` INT DEFAULT 0 COMMENT '正确数',
  `accuracy` DECIMAL(5,2) DEFAULT 0 COMMENT '正确率',
  `status` VARCHAR(20) DEFAULT 'in_progress' COMMENT '状态:in_progress/completed',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `completed_at` DATETIME COMMENT '完成时间',
  INDEX `idx_user_id` (`user_id`),
  INDEX `idx_user_status` (`user_id`, `status`),
  INDEX `idx_word_book_id` (`word_book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='听写表';

-- 10. 听写记录表
CREATE TABLE IF NOT EXISTS `dictation_records` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL COMMENT '用户ID',
  `dictation_id` INT NOT NULL COMMENT '听写ID',
  `word_book_id` INT NOT NULL COMMENT '词书ID',
  `mode` VARCHAR(20) NOT NULL COMMENT '模式',
  `total_words` INT DEFAULT 0 COMMENT '总单词数',
  `correct_words` INT DEFAULT 0 COMMENT '正确数',
  `accuracy` DECIMAL(5,2) DEFAULT 0 COMMENT '正确率',
  `time_spent` INT DEFAULT 0 COMMENT '耗时(秒)',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_user_id` (`user_id`),
  INDEX `idx_user_created` (`user_id`, `created_at`),
  INDEX `idx_word_book_id` (`word_book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='听写记录表';

-- 11. 听写答题表
CREATE TABLE IF NOT EXISTS `dictation_answers` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `dictation_id` INT NOT NULL COMMENT '听写ID',
  `word_id` INT NOT NULL COMMENT '单词ID',
  `user_answer` VARCHAR(255) COMMENT '用户答案',
  `correct_answer` VARCHAR(255) COMMENT '正确答案',
  `is_correct` TINYINT(1) DEFAULT 0 COMMENT '是否正确',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_dictation_id` (`dictation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='听写答题表';

-- 显示创建结果
SELECT '✅ 数据表创建完成！' as '状态';
SELECT TABLE_NAME, TABLE_COMMENT 
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'xuebadict' 
  AND TABLE_NAME IN (
    'membership_plans', 'user_memberships', 'membership_orders', 
    'membership_benefits', 'user_membership_benefits',
    'challenges', 'challenge_records', 'challenge_answers',
    'dictations', 'dictation_records', 'dictation_answers'
  )
ORDER BY TABLE_NAME;
