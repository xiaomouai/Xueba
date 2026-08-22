-- 会员系统初始化数据
-- 插入会员套餐数据和默认权益

USE xuebadict;

-- 清空现有数据（可选）
-- TRUNCATE TABLE membership_plans;
-- TRUNCATE TABLE membership_benefits;

-- 插入会员套餐
INSERT INTO membership_plans (name, plan_type, duration_days, price, original_price, description, features, is_recommended, discount_label, sort_order, is_active) VALUES
('月度会员', 'month', 30, 19.90, 29.90, '一个月畅享所有功能', '无限次听写,无限次闯关,AI智能辅导,专属学习报告,去除广告', 0, '限时优惠', 1, 1),
('季度会员', 'season', 90, 49.90, 89.90, '三个月超值套餐', '无限次听写,无限次闯关,AI智能辅导,专属学习报告,去除广告,优先客服', 1, '推荐', 2, 1),
('年度会员', 'year', 365, 159.90, 359.90, '一年无忧学习', '无限次听写,无限次闯关,AI智能辅导,专属学习报告,去除广告,优先客服,学习资料包', 0, '超值', 3, 1),
('终身会员', 'lifetime', 36500, 499.90, 999.90, '一次购买终身使用', '无限次听写,无限次闯关,AI智能辅导,专属学习报告,去除广告,优先客服,学习资料包,终身免费更新', 0, '最划算', 4, 1);

-- 插入会员权益
INSERT INTO membership_benefits (name, description, benefit_type, benefit_value, membership_type, icon, is_active, sort_order) VALUES
-- 免费用户权益
('每日听写', '每天最多听写20个单词', 'daily_limit', '20', 'free', '📝', 1, 1),
('基础闯关', '只能挑战简单难度', 'difficulty_limit', 'easy', 'free', '🎯', 1, 2),

-- 月度会员权益
('无限听写', '无限次数听写练习', 'unlimited_dictation', 'unlimited', 'month', '✍️', 1, 3),
('全难度闯关', '解锁所有难度闯关', 'all_difficulties', 'all', 'month', '🎮', 1, 4),
('AI智能辅导', '个性化学习建议', 'ai_tutor', 'enabled', 'month', '🤖', 1, 5),
('去除广告', '无广告纯净体验', 'no_ads', 'enabled', 'month', '🚫', 1, 6),

-- 季度会员额外权益
('优先客服', '专属客服通道', 'priority_support', 'enabled', 'season', '👨‍💼', 1, 7),
('学习报告', '每周学习数据报告', 'weekly_report', 'enabled', 'season', '📊', 1, 8),

-- 年度会员额外权益
('学习资料包', '免费下载所有资料', 'resource_pack', 'enabled', 'year', '📚', 1, 9),
('错题精讲', 'AI错题深度讲解', 'error_analysis', 'enabled', 'year', '🎓', 1, 10),

-- 终身会员额外权益
('终身更新', '所有功能终身免费更新', 'lifetime_update', 'enabled', 'lifetime', '♾️', 1, 11),
('专属徽章', '终身会员专属标识', 'badge', 'vip_forever', 'lifetime', '👑', 1, 12);

-- 查看插入结果
SELECT '会员套餐数据:' as '';
SELECT id, name, plan_type, price, duration_days, is_recommended FROM membership_plans;

SELECT '' as '';
SELECT '会员权益数据:' as '';
SELECT id, name, membership_type, benefit_type FROM membership_benefits;

SELECT '' as '';
SELECT '✅ 会员系统初始化数据插入成功！' as '';
