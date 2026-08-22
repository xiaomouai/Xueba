"""
Dict词库数据导入脚本
将Dict ZIP文件中的单词数据导入到MySQL数据库

使用方法:
    python import_dict_to_db.py --books PEPXiaoXue3_1,PEPXiaoXue3_2
    python import_dict_to_db.py --all  # 导入所有词书
    python import_dict_to_db.py --category 小学  # 导入指定分类
"""

import os
import sys
import json
import zipfile
import argparse
from datetime import datetime
import pymysql
from typing import List, Dict, Any
import uuid

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'lioneng_db',
    'charset': 'utf8mb4'
}

# Dict词库路径
DICT_PATH = './xuebaBackend/dict/book/'

# 词书元数据
BOOKS_METADATA = [
    {'id': 'PEPXiaoXue3_1', 'title': '人教版小学英语-三年级上册', 'wordCount': 64, 'category': '小学', 'grade': 3, 'term': 1},
    {'id': 'PEPXiaoXue3_2', 'title': '人教版小学英语-三年级下册', 'wordCount': 72, 'category': '小学', 'grade': 3, 'term': 2},
    {'id': 'PEPXiaoXue4_1', 'title': '人教版小学英语-四年级上册', 'wordCount': 84, 'category': '小学', 'grade': 4, 'term': 1},
    {'id': 'PEPXiaoXue4_2', 'title': '人教版小学英语-四年级下册', 'wordCount': 104, 'category': '小学', 'grade': 4, 'term': 2},
    {'id': 'PEPXiaoXue5_1', 'title': '人教版小学英语-五年级上册', 'wordCount': 131, 'category': '小学', 'grade': 5, 'term': 1},
    {'id': 'PEPXiaoXue5_2', 'title': '人教版小学英语-五年级下册', 'wordCount': 156, 'category': '小学', 'grade': 5, 'term': 2},
    {'id': 'PEPXiaoXue6_1', 'title': '人教版小学英语-六年级上册', 'wordCount': 130, 'category': '小学', 'grade': 6, 'term': 1},
    {'id': 'PEPXiaoXue6_2', 'title': '人教版小学英语-六年级下册', 'wordCount': 108, 'category': '小学', 'grade': 6, 'term': 2},
    {'id': 'PEPChuZhong7_1', 'title': '人教版初中英语-七年级上册', 'wordCount': 392, 'category': '初中', 'grade': 7, 'term': 1},
    {'id': 'PEPChuZhong7_2', 'title': '人教版初中英语-七年级下册', 'wordCount': 492, 'category': '初中', 'grade': 7, 'term': 2},
    {'id': 'PEPChuZhong8_1', 'title': '人教版初中英语-八年级上册', 'wordCount': 419, 'category': '初中', 'grade': 8, 'term': 1},
    {'id': 'PEPChuZhong8_2', 'title': '人教版初中英语-八年级下册', 'wordCount': 466, 'category': '初中', 'grade': 8, 'term': 2},
    {'id': 'PEPChuZhong9_1', 'title': '人教版初中英语-九年级全册', 'wordCount': 551, 'category': '初中', 'grade': 9, 'term': 1},
]


class DictImporter:
    """Dict数据导入器"""
    
    def __init__(self, db_config: Dict[str, Any]):
        self.db_config = db_config
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """连接数据库"""
        try:
            self.conn = pymysql.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            print("✅ 数据库连接成功")
        except Exception as e:
            print(f"❌ 数据库连接失败: {e}")
            sys.exit(1)
    
    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("✅ 数据库连接已关闭")
    
    def create_tables(self):
        """创建数据表"""
        print("\n📋 创建数据表...")
        
        # 创建词书表
        create_books_sql = """
        CREATE TABLE IF NOT EXISTS dict_books (
            id VARCHAR(32) PRIMARY KEY,
            book_id VARCHAR(50) UNIQUE NOT NULL,
            title VARCHAR(100) NOT NULL,
            word_count INT DEFAULT 0,
            category VARCHAR(20),
            tag VARCHAR(20) DEFAULT '人教版',
            grade INT,
            term INT,
            popularity INT DEFAULT 0,
            icon VARCHAR(255),
            zip_file VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_category (category),
            INDEX idx_grade (grade)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        # 创建单词表
        create_words_sql = """
        CREATE TABLE IF NOT EXISTS dict_words (
            id VARCHAR(32) PRIMARY KEY,
            book_id VARCHAR(50) NOT NULL,
            word_rank INT NOT NULL,
            head_word VARCHAR(100) NOT NULL,
            uk_phone VARCHAR(100),
            us_phone VARCHAR(100),
            uk_speech VARCHAR(255),
            us_speech VARCHAR(255),
            translations JSON,
            sentences JSON,
            phrases JSON,
            synonyms JSON,
            rel_words JSON,
            exams JSON,
            content JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY uk_book_rank (book_id, word_rank),
            INDEX idx_head_word (head_word),
            INDEX idx_book_id (book_id),
            FULLTEXT KEY ft_head_word (head_word)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        try:
            self.cursor.execute(create_books_sql)
            print("  ✅ dict_books 表创建成功")
            
            self.cursor.execute(create_words_sql)
            print("  ✅ dict_words 表创建成功")
            
            self.conn.commit()
        except Exception as e:
            print(f"  ❌ 创建表失败: {e}")
            self.conn.rollback()
            sys.exit(1)
    
    def find_zip_file(self, book_id: str) -> str:
        """查找ZIP文件"""
        try:
            zip_files = [
                f for f in os.listdir(DICT_PATH) 
                if book_id in f and f.endswith('.zip')
            ]
            if zip_files:
                return os.path.join(DICT_PATH, zip_files[0])
            return None
        except Exception as e:
            print(f"  ❌ 查找ZIP文件失败: {e}")
            return None
    
    def read_words_from_zip(self, zip_path: str) -> List[Dict[str, Any]]:
        """从ZIP文件读取单词"""
        words = []
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                json_files = [f for f in zip_ref.namelist() if f.endswith('.json')]
                
                for json_file in json_files:
                    with zip_ref.open(json_file) as f:
                        content = f.read().decode('utf-8')
                        
                        try:
                            data = json.loads(content)
                            if isinstance(data, list):
                                words.extend(data)
                            elif isinstance(data, dict):
                                words.append(data)
                        except json.JSONDecodeError:
                            for line in content.strip().split('\n'):
                                if line.strip():
                                    try:
                                        word_data = json.loads(line)
                                        words.append(word_data)
                                    except json.JSONDecodeError:
                                        continue
        except Exception as e:
            print(f"  ❌ 读取ZIP文件失败: {e}")
        
        return words
    
    def extract_word_data(self, word_data: Dict[str, Any]) -> Dict[str, Any]:
        """提取单词数据"""
        content = {}
        if 'content' in word_data and isinstance(word_data['content'], dict):
            if 'word' in word_data['content'] and isinstance(word_data['content']['word'], dict):
                content = word_data['content']['word'].get('content', {})
        
        head_word = word_data.get('headWord', '')
        uk_phone = content.get('ukphone', '')
        us_phone = content.get('usphone', '')
        
        return {
            'head_word': head_word,
            'uk_phone': uk_phone,
            'us_phone': us_phone,
            'uk_speech': f"https://dict.youdao.com/dictvoice?audio={head_word}&type=1",
            'us_speech': f"https://dict.youdao.com/dictvoice?audio={head_word}&type=2",
            'translations': json.dumps(content.get('trans', []), ensure_ascii=False),
            'sentences': json.dumps(content.get('sentence', {}), ensure_ascii=False),
            'phrases': json.dumps(content.get('phrase', {}), ensure_ascii=False),
            'synonyms': json.dumps(content.get('syno', {}), ensure_ascii=False),
            'rel_words': json.dumps(content.get('relWord', {}), ensure_ascii=False),
            'exams': json.dumps(content.get('exam', []), ensure_ascii=False),
            'content': json.dumps(content, ensure_ascii=False)
        }
    
    def import_book(self, book_meta: Dict[str, Any]) -> bool:
        """导入单个词书"""
        book_id = book_meta['id']
        print(f"\n📚 导入词书: {book_meta['title']} ({book_id})")
        
        # 查找ZIP文件
        zip_path = self.find_zip_file(book_id)
        if not zip_path:
            print(f"  ❌ 未找到ZIP文件")
            return False
        
        print(f"  📦 ZIP文件: {os.path.basename(zip_path)}")
        
        # 读取单词数据
        words = self.read_words_from_zip(zip_path)
        if not words:
            print(f"  ❌ 未读取到单词数据")
            return False
        
        print(f"  📖 读取到 {len(words)} 个单词")
        
        # 插入词书记录
        try:
            insert_book_sql = """
            INSERT INTO dict_books (id, book_id, title, word_count, category, grade, term, zip_file)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                title = VALUES(title),
                word_count = VALUES(word_count),
                updated_at = CURRENT_TIMESTAMP
            """
            
            self.cursor.execute(insert_book_sql, (
                str(uuid.uuid4().hex[:24]),
                book_id,
                book_meta['title'],
                len(words),
                book_meta.get('category', ''),
                book_meta.get('grade', 0),
                book_meta.get('term', 0),
                os.path.basename(zip_path)
            ))
            
            print(f"  ✅ 词书记录已插入")
        except Exception as e:
            print(f"  ❌ 插入词书记录失败: {e}")
            return False
        
        # 插入单词记录
        insert_word_sql = """
        INSERT INTO dict_words (
            id, book_id, word_rank, head_word, uk_phone, us_phone,
            uk_speech, us_speech, translations, sentences, phrases,
            synonyms, rel_words, exams, content
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        ) ON DUPLICATE KEY UPDATE
            head_word = VALUES(head_word),
            uk_phone = VALUES(uk_phone),
            us_phone = VALUES(us_phone),
            content = VALUES(content)
        """
        
        success_count = 0
        error_count = 0
        
        for word_data in words:
            try:
                word_rank = word_data.get('wordRank', 0)
                extracted = self.extract_word_data(word_data)
                
                self.cursor.execute(insert_word_sql, (
                    str(uuid.uuid4().hex[:24]),
                    book_id,
                    word_rank,
                    extracted['head_word'],
                    extracted['uk_phone'],
                    extracted['us_phone'],
                    extracted['uk_speech'],
                    extracted['us_speech'],
                    extracted['translations'],
                    extracted['sentences'],
                    extracted['phrases'],
                    extracted['synonyms'],
                    extracted['rel_words'],
                    extracted['exams'],
                    extracted['content']
                ))
                
                success_count += 1
                
                if success_count % 50 == 0:
                    print(f"  ⏳ 已导入 {success_count}/{len(words)} 个单词...")
                    
            except Exception as e:
                error_count += 1
                print(f"  ⚠️  单词 {word_data.get('headWord', 'unknown')} 导入失败: {e}")
        
        # 提交事务
        try:
            self.conn.commit()
            print(f"  ✅ 导入完成: 成功 {success_count} 个，失败 {error_count} 个")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"  ❌ 提交事务失败: {e}")
            return False
    
    def import_books(self, book_ids: List[str] = None, category: str = None):
        """批量导入词书"""
        books_to_import = BOOKS_METADATA
        
        if book_ids:
            books_to_import = [b for b in BOOKS_METADATA if b['id'] in book_ids]
        elif category:
            books_to_import = [b for b in BOOKS_METADATA if b.get('category') == category]
        
        print(f"\n🚀 开始导入 {len(books_to_import)} 个词书...")
        print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        success_count = 0
        for book_meta in books_to_import:
            if self.import_book(book_meta):
                success_count += 1
        
        print(f"\n{'='*60}")
        print(f"📊 导入统计:")
        print(f"  总词书数: {len(books_to_import)}")
        print(f"  成功: {success_count}")
        print(f"  失败: {len(books_to_import) - success_count}")
        print(f"⏰ 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Dict词库数据导入工具')
    parser.add_argument('--books', type=str, help='指定词书ID，多个用逗号分隔')
    parser.add_argument('--category', type=str, choices=['小学', '初中', '高中'], help='指定分类')
    parser.add_argument('--all', action='store_true', help='导入所有词书')
    parser.add_argument('--create-tables', action='store_true', help='仅创建数据表')
    
    args = parser.parse_args()
    
    # 创建导入器
    importer = DictImporter(DB_CONFIG)
    importer.connect()
    
    # 创建表
    importer.create_tables()
    
    if args.create_tables:
        print("\n✅ 数据表创建完成")
        importer.close()
        return
    
    # 导入数据
    if args.all:
        importer.import_books()
    elif args.books:
        book_ids = [b.strip() for b in args.books.split(',')]
        importer.import_books(book_ids=book_ids)
    elif args.category:
        importer.import_books(category=args.category)
    else:
        print("\n❌ 请指定导入选项: --books, --category, 或 --all")
        print("示例:")
        print("  python import_dict_to_db.py --books PEPXiaoXue3_1,PEPXiaoXue3_2")
        print("  python import_dict_to_db.py --category 小学")
        print("  python import_dict_to_db.py --all")
    
    importer.close()


if __name__ == '__main__':
    main()
