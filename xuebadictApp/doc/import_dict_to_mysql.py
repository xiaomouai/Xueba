"""
词书数据导入MySQL数据库脚本
从dict/book目录读取所有JSON文件并导入到数据库
"""
import os
import json
import zipfile
import mysql.connector
from mysql.connector import Error
import sys
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('.env')

# 数据库配置（从环境变量读取）
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '123456'),
    'database': os.getenv('DB_NAME', 'xuebadict'),
    'charset': os.getenv('DB_CHARSET', 'utf8mb4')
}

# 词书根目录
DICT_DIR = os.path.join(os.path.dirname(__file__), 'dict')
BOOK_DIR = os.path.join(DICT_DIR, 'book')
BOOKLISTS_FILE = os.path.join(DICT_DIR, 'bookLists.txt')


def create_database_tables(cursor):
    """创建数据库表"""
    
    # 词书表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS word_books (
        id VARCHAR(50) PRIMARY KEY COMMENT '词书ID',
        title VARCHAR(200) NOT NULL COMMENT '词书标题',
        cover VARCHAR(500) COMMENT '封面图片URL',
        word_num INT DEFAULT 0 COMMENT '单词数量',
        recite_user_num INT DEFAULT 0 COMMENT '背诵人数',
        size INT DEFAULT 0 COMMENT '文件大小',
        introduce TEXT COMMENT '简介',
        origin_name VARCHAR(100) COMMENT '来源名称',
        version VARCHAR(20) COMMENT '版本号',
        tags VARCHAR(200) COMMENT '标签（逗号分隔）',
        offline_data VARCHAR(500) COMMENT '离线数据URL',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_title (title),
        INDEX idx_tags (tags)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='词书表'
    """)
    
    # 单词表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS words (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        book_id VARCHAR(50) NOT NULL COMMENT '词书ID',
        word_id VARCHAR(100) NOT NULL COMMENT '单词唯一ID',
        word_rank INT NOT NULL COMMENT '单词序号',
        head_word VARCHAR(100) NOT NULL COMMENT '单词',
        us_phone VARCHAR(100) COMMENT '美式音标',
        uk_phone VARCHAR(100) COMMENT '英式音标',
        us_speech VARCHAR(200) COMMENT '美式发音参数',
        uk_speech VARCHAR(200) COMMENT '英式发音参数',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY uk_word_id (word_id),
        INDEX idx_book_id (book_id),
        INDEX idx_head_word (head_word),
        INDEX idx_word_rank (book_id, word_rank),
        FOREIGN KEY (book_id) REFERENCES word_books(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='单词表'
    """)
    
    # 单词释义表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS word_translations (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        word_id VARCHAR(100) NOT NULL COMMENT '单词ID',
        pos VARCHAR(20) COMMENT '词性',
        tran_cn TEXT COMMENT '中文释义',
        tran_other TEXT COMMENT '英文释义',
        desc_cn VARCHAR(50) COMMENT '中文说明',
        desc_other VARCHAR(50) COMMENT '其他说明',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_word_id (word_id),
        FOREIGN KEY (word_id) REFERENCES words(word_id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='单词释义表'
    """)
    
    # 例句表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS word_sentences (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        word_id VARCHAR(100) NOT NULL COMMENT '单词ID',
        s_content TEXT NOT NULL COMMENT '英文例句',
        s_cn TEXT COMMENT '中文翻译',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_word_id (word_id),
        FOREIGN KEY (word_id) REFERENCES words(word_id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='例句表'
    """)
    
    # 短语表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS word_phrases (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        word_id VARCHAR(100) NOT NULL COMMENT '单词ID',
        p_content VARCHAR(200) NOT NULL COMMENT '英文短语',
        p_cn TEXT COMMENT '中文翻译',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_word_id (word_id),
        FOREIGN KEY (word_id) REFERENCES words(word_id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='短语表'
    """)
    
    # 近义词表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS word_synonyms (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        word_id VARCHAR(100) NOT NULL COMMENT '单词ID',
        pos VARCHAR(20) COMMENT '词性',
        tran VARCHAR(200) COMMENT '词义',
        synonym VARCHAR(100) NOT NULL COMMENT '近义词',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_word_id (word_id),
        FOREIGN KEY (word_id) REFERENCES words(word_id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='近义词表'
    """)
    
    # 同根词表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS word_related (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        word_id VARCHAR(100) NOT NULL COMMENT '单词ID',
        pos VARCHAR(20) COMMENT '词性',
        related_word VARCHAR(100) NOT NULL COMMENT '同根词',
        tran TEXT COMMENT '翻译',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_word_id (word_id),
        FOREIGN KEY (word_id) REFERENCES words(word_id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='同根词表'
    """)
    
    print("[成功] 数据库表创建成功")


def load_book_lists():
    """加载词书列表"""
    try:
        with open(BOOKLISTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['data']['normalBooksInfo']
    except Exception as e:
        print(f"加载词书列表失败: {e}")
        return []


def extract_zip_file(zip_path, extract_to):
    """解压ZIP文件"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return True
    except Exception as e:
        print(f"  解压失败: {e}")
        return False


def find_json_file(directory):
    """在目录中查找JSON文件"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                return os.path.join(root, file)
    return None


def import_word_book(cursor, book_info):
    """导入单个词书"""
    book_id = book_info['id']
    title = book_info['title']
    
    print(f"\n正在导入: {title} ({book_id})")
    
    # 插入词书信息
    tags = ','.join([tag['tagName'] for tag in book_info.get('tags', [])])
    
    cursor.execute("""
    INSERT INTO word_books (id, title, cover, word_num, recite_user_num, size, 
                           introduce, origin_name, version, tags, offline_data)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    title=VALUES(title), cover=VALUES(cover), word_num=VALUES(word_num),
    recite_user_num=VALUES(recite_user_num), size=VALUES(size),
    introduce=VALUES(introduce), origin_name=VALUES(origin_name),
    version=VALUES(version), tags=VALUES(tags), offline_data=VALUES(offline_data)
    """, (
        book_id,
        title,
        book_info.get('cover', ''),
        book_info.get('wordNum', 0),
        book_info.get('reciteUserNum', 0),
        book_info.get('size', 0),
        book_info.get('introduce', ''),
        book_info.get('bookOrigin', {}).get('originName', ''),
        book_info.get('version', ''),
        tags,
        book_info.get('offlinedata', '')
    ))
    
    # 查找词书数据文件
    json_file = None
    
    # 1. 先检查是否已有解压的目录
    for item in os.listdir(BOOK_DIR):
        item_path = os.path.join(BOOK_DIR, item)
        if os.path.isdir(item_path) and book_id in item:
            json_file = find_json_file(item_path)
            if json_file:
                break
    
    # 2. 如果没找到，尝试解压ZIP文件
    if not json_file:
        for file in os.listdir(BOOK_DIR):
            if file.endswith('.zip') and book_id in file:
                zip_path = os.path.join(BOOK_DIR, file)
                extract_dir = os.path.join(BOOK_DIR, file.replace('.zip', ''))
                
                if not os.path.exists(extract_dir):
                    print(f"  解压: {file}")
                    if extract_zip_file(zip_path, extract_dir):
                        json_file = find_json_file(extract_dir)
                break
    
    # 3. 检查根目录是否有同名JSON文件
    if not json_file:
        direct_json = os.path.join(BOOK_DIR, f"{book_id}.json")
        if os.path.exists(direct_json):
            json_file = direct_json
    
    if not json_file:
        print(f"  [警告] 未找到词书数据文件")
        return 0
    
    # 加载并导入单词数据
    try:
        word_count = 0
        with open(json_file, 'r', encoding='utf-8') as f:
            # 逐行读取JSON（JSONL格式）
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:  # 跳过空行
                    continue
                    
                try:
                    word_item = json.loads(line)
                    import_word(cursor, book_id, word_item)
                    word_count += 1
                except json.JSONDecodeError as je:
                    print(f"  [警告] 第{line_num}行JSON解析错误: {je}")
                    continue
                except Exception as e:
                    headword = word_item.get('headWord', 'unknown') if 'word_item' in locals() else 'unknown'
                    print(f"  [警告] 导入单词失败 {headword}: {e}")
                    continue
        
        print(f"  [成功] 成功导入 {word_count} 个单词")
        return word_count
        
    except Exception as e:
        print(f"  [错误] 读取词书数据失败: {e}")
        return 0


def import_word(cursor, book_id, word_data):
    """导入单个单词及其详细信息"""
    word_rank = word_data.get('wordRank', 0)
    head_word = word_data.get('headWord', '')
    
    if not head_word:
        return
    
    content = word_data.get('content', {}).get('word', {})
    word_content = content.get('content', {})
    
    word_id = content.get('wordId', f"{book_id}_{word_rank}")
    
    # 插入单词基本信息
    cursor.execute("""
    INSERT INTO words (book_id, word_id, word_rank, head_word, 
                      us_phone, uk_phone, us_speech, uk_speech)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    word_rank=VALUES(word_rank), head_word=VALUES(head_word),
    us_phone=VALUES(us_phone), uk_phone=VALUES(uk_phone),
    us_speech=VALUES(us_speech), uk_speech=VALUES(uk_speech)
    """, (
        book_id,
        word_id,
        word_rank,
        head_word,
        word_content.get('usphone', ''),
        word_content.get('ukphone', ''),
        word_content.get('usspeech', ''),
        word_content.get('ukspeech', '')
    ))
    
    # 插入释义
    trans = word_content.get('trans', [])
    for tran in trans:
        cursor.execute("""
        INSERT INTO word_translations (word_id, pos, tran_cn, tran_other, desc_cn, desc_other)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            word_id,
            tran.get('pos', ''),
            tran.get('tranCn', ''),
            tran.get('tranOther', ''),
            tran.get('descCn', ''),
            tran.get('descOther', '')
        ))
    
    # 插入例句
    sentences = word_content.get('sentence', {}).get('sentences', [])
    for sent in sentences:
        cursor.execute("""
        INSERT INTO word_sentences (word_id, s_content, s_cn)
        VALUES (%s, %s, %s)
        """, (
            word_id,
            sent.get('sContent', ''),
            sent.get('sCn', '')
        ))
    
    # 插入短语
    phrases = word_content.get('phrase', {}).get('phrases', [])
    for phrase in phrases:
        cursor.execute("""
        INSERT INTO word_phrases (word_id, p_content, p_cn)
        VALUES (%s, %s, %s)
        """, (
            word_id,
            phrase.get('pContent', ''),
            phrase.get('pCn', '')
        ))
    
    # 插入近义词
    synos = word_content.get('syno', {}).get('synos', [])
    for syno in synos:
        pos = syno.get('pos', '')
        tran = syno.get('tran', '')
        for hwd in syno.get('hwds', []):
            cursor.execute("""
            INSERT INTO word_synonyms (word_id, pos, tran, synonym)
            VALUES (%s, %s, %s, %s)
            """, (
                word_id,
                pos,
                tran,
                hwd.get('w', '')
            ))
    
    # 插入同根词
    rels = word_content.get('relWord', {}).get('rels', [])
    for rel in rels:
        pos = rel.get('pos', '')
        for word_item in rel.get('words', []):
            cursor.execute("""
            INSERT INTO word_related (word_id, pos, related_word, tran)
            VALUES (%s, %s, %s, %s)
            """, (
                word_id,
                pos,
                word_item.get('hwd', ''),
                word_item.get('tran', '')
            ))


def main():
    """主函数"""
    print("=" * 60)
    print("词书数据导入MySQL数据库")
    print("=" * 60)
    
    # 检查目录
    if not os.path.exists(BOOK_DIR):
        print(f"✗ 词书目录不存在: {BOOK_DIR}")
        return
    
    if not os.path.exists(BOOKLISTS_FILE):
        print(f"[错误] 词书列表文件不存在: {BOOKLISTS_FILE}")
        return
    
    # 连接数据库
    try:
        print("\n连接数据库...")
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        print("[成功] 数据库连接成功")
        
        # 创建表
        print("\n创建数据库表...")
        create_database_tables(cursor)
        connection.commit()  # 立即提交表创建
        print("[成功] 数据库表已创建并提交")
        
        # 加载词书列表
        print("\n加载词书列表...")
        book_lists = load_book_lists()
        print(f"[成功] 找到 {len(book_lists)} 个词书")
        
        # 导入每个词书
        total_words = 0
        success_count = 0
        
        for idx, book_info in enumerate(book_lists, 1):
            print(f"\n[{idx}/{len(book_lists)}]", end=' ')
            try:
                word_count = import_word_book(cursor, book_info)
                if word_count > 0:
                    success_count += 1
                    total_words += word_count
                # 每个词书导入后立即提交
                connection.commit()
            except Exception as e:
                print(f"  [错误] 导入失败: {e}")
                # 只回滚当前词书的数据，不影响已导入的词书
                connection.rollback()
        
        # 统计信息
        print("\n" + "=" * 60)
        print(f"导入完成！")
        print(f"成功导入词书: {success_count}/{len(book_lists)}")
        print(f"总计单词数: {total_words}")
        print("=" * 60)
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"[错误] 数据库错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
