"""
验证词书数据导入是否成功
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('.env.dict_import')

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '123456'),
    'database': os.getenv('DB_NAME', 'xuebadict'),
    'charset': os.getenv('DB_CHARSET', 'utf8mb4')
}


def test_connection():
    """测试数据库连接"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✓ 数据库连接成功")
        print(f"  MySQL版本: {version[0]}")
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"✗ 数据库连接失败: {e}")
        return False


def check_tables(cursor):
    """检查表是否存在"""
    tables = [
        'word_books',
        'words',
        'word_translations',
        'word_sentences',
        'word_phrases',
        'word_synonyms',
        'word_related'
    ]
    
    print("\n检查数据库表:")
    all_exist = True
    for table in tables:
        cursor.execute(f"SHOW TABLES LIKE '{table}'")
        result = cursor.fetchone()
        if result:
            print(f"  ✓ {table}")
        else:
            print(f"  ✗ {table} (不存在)")
            all_exist = False
    
    return all_exist


def get_statistics(cursor):
    """获取统计信息"""
    print("\n数据统计:")
    
    # 词书数量
    cursor.execute("SELECT COUNT(*) FROM word_books")
    book_count = cursor.fetchone()[0]
    print(f"  词书总数: {book_count}")
    
    # 单词数量
    cursor.execute("SELECT COUNT(*) FROM words")
    word_count = cursor.fetchone()[0]
    print(f"  单词总数: {word_count:,}")
    
    # 释义数量
    cursor.execute("SELECT COUNT(*) FROM word_translations")
    trans_count = cursor.fetchone()[0]
    print(f"  释义总数: {trans_count:,}")
    
    # 例句数量
    cursor.execute("SELECT COUNT(*) FROM word_sentences")
    sent_count = cursor.fetchone()[0]
    print(f"  例句总数: {sent_count:,}")
    
    # 短语数量
    cursor.execute("SELECT COUNT(*) FROM word_phrases")
    phrase_count = cursor.fetchone()[0]
    print(f"  短语总数: {phrase_count:,}")
    
    # 近义词数量
    cursor.execute("SELECT COUNT(*) FROM word_synonyms")
    syn_count = cursor.fetchone()[0]
    print(f"  近义词数: {syn_count:,}")
    
    # 同根词数量
    cursor.execute("SELECT COUNT(*) FROM word_related")
    rel_count = cursor.fetchone()[0]
    print(f"  同根词数: {rel_count:,}")


def show_sample_books(cursor):
    """显示示例词书"""
    print("\n示例词书（按背诵人数排序）:")
    cursor.execute("""
    SELECT id, title, word_num, recite_user_num, tags
    FROM word_books
    ORDER BY recite_user_num DESC
    LIMIT 10
    """)
    
    results = cursor.fetchall()
    print(f"\n  {'ID':<20} {'标题':<35} {'单词数':<10} {'背诵人数':<12} {'标签'}")
    print("  " + "-" * 100)
    for row in results:
        book_id, title, word_num, recite_num, tags = row
        # 截断过长的标题
        title_display = title[:32] + "..." if len(title) > 35 else title
        print(f"  {book_id:<20} {title_display:<35} {word_num:<10} {recite_num:<12,} {tags}")


def show_sample_word(cursor):
    """显示示例单词详情"""
    print("\n示例单词详情:")
    
    # 查询一个单词
    cursor.execute("""
    SELECT w.word_id, w.head_word, w.us_phone, w.uk_phone
    FROM words w
    WHERE w.book_id = 'CET4_3'
    LIMIT 1
    """)
    
    word_result = cursor.fetchone()
    if not word_result:
        print("  未找到示例单词")
        return
    
    word_id, head_word, us_phone, uk_phone = word_result
    
    print(f"\n  单词: {head_word}")
    print(f"  美音: {us_phone}")
    print(f"  英音: {uk_phone}")
    
    # 查询释义
    cursor.execute("""
    SELECT pos, tran_cn FROM word_translations
    WHERE word_id = %s LIMIT 3
    """, (word_id,))
    
    translations = cursor.fetchall()
    if translations:
        print("\n  释义:")
        for pos, tran_cn in translations:
            print(f"    {pos}. {tran_cn}")
    
    # 查询例句
    cursor.execute("""
    SELECT s_content, s_cn FROM word_sentences
    WHERE word_id = %s LIMIT 2
    """, (word_id,))
    
    sentences = cursor.fetchall()
    if sentences:
        print("\n  例句:")
        for idx, (s_content, s_cn) in enumerate(sentences, 1):
            print(f"    {idx}. {s_content}")
            print(f"       {s_cn}")


def check_data_integrity(cursor):
    """检查数据完整性"""
    print("\n数据完整性检查:")
    
    # 检查是否有单词没有对应的词书
    cursor.execute("""
    SELECT COUNT(*) FROM words w
    LEFT JOIN word_books b ON w.book_id = b.id
    WHERE b.id IS NULL
    """)
    orphan_words = cursor.fetchone()[0]
    if orphan_words == 0:
        print("  ✓ 所有单词都关联到有效词书")
    else:
        print(f"  ⚠ 有 {orphan_words} 个孤立单词（未关联词书）")
    
    # 检查是否有词书没有单词
    cursor.execute("""
    SELECT COUNT(*) FROM word_books b
    LEFT JOIN words w ON b.id = w.book_id
    WHERE w.id IS NULL
    """)
    empty_books = cursor.fetchone()[0]
    if empty_books == 0:
        print("  ✓ 所有词书都有单词数据")
    else:
        print(f"  ⚠ 有 {empty_books} 个空词书（无单词数据）")


def main():
    """主函数"""
    print("=" * 80)
    print("词书数据导入验证")
    print("=" * 80)
    
    # 测试连接
    if not test_connection():
        return
    
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 检查表
        if not check_tables(cursor):
            print("\n✗ 部分表不存在，请先运行导入脚本")
            return
        
        # 获取统计信息
        get_statistics(cursor)
        
        # 显示示例词书
        show_sample_books(cursor)
        
        # 显示示例单词
        show_sample_word(cursor)
        
        # 检查数据完整性
        check_data_integrity(cursor)
        
        print("\n" + "=" * 80)
        print("验证完成！")
        print("=" * 80)
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"\n✗ 验证过程出错: {e}")


if __name__ == '__main__':
    main()
