#!/usr/bin/env python3
"""
Dict词库数据导入SQLite数据库
从ZIP文件中读取JSON数据并存入SQLite数据库
"""
import os
import sys
import json
import zipfile
import sqlite3
import uuid
from datetime import datetime
from typing import List, Dict, Any


# 词书元数据（从README.md提取）
BOOKS_METADATA = [
    # 人教版小学
    {'id': 'PEPXiaoXue3_1', 'title': '人教版小学英语-三年级上册', 'wordCount': 64, 'category': '小学', 'grade': 3, 'term': 1, 'tag': '人教版', 'popularity': 378234, 'icon': 'https://nos.netease.com/ydschool-online/2_youdao_PEPXiaoXue3_1.jpg', 'zipFile': '1521164661774_PEPXiaoXue3_1.zip'},
    {'id': 'PEPXiaoXue3_2', 'title': '人教版小学英语-三年级下册', 'wordCount': 72, 'category': '小学', 'grade': 3, 'term': 2, 'tag': '人教版', 'popularity': 103262, 'icon': 'https://nos.netease.com/ydschool-online/2_youdao_PEPXiaoXue3_2.jpg', 'zipFile': '1521164656604_PEPXiaoXue3_2.zip'},
    {'id': 'PEPXiaoXue4_1', 'title': '人教版小学英语-四年级上册', 'wordCount': 84, 'category': '小学', 'grade': 4, 'term': 1, 'tag': '人教版', 'popularity': 89159, 'icon': 'https://nos.netease.com/ydschool-online/2_youdao_PEPXiaoXue4_1.jpg', 'zipFile': '1521164677447_PEPXiaoXue4_1.zip'},
    {'id': 'PEPXiaoXue4_2', 'title': '人教版小学英语-四年级下册', 'wordCount': 104, 'category': '小学', 'grade': 4, 'term': 2, 'tag': '人教版', 'popularity': 50627, 'icon': 'https://nos.netease.com/ydschool-online/2_youdao_PEPXiaoXue4_2.jpg', 'zipFile': '1521164663086_PEPXiaoXue4_2.zip'},
    {'id': 'PEPXiaoXue5_1', 'title': '人教版小学英语-五年级上册', 'wordCount': 131, 'category': '小学', 'grade': 5, 'term': 1, 'tag': '人教版', 'popularity': 65368, 'icon': 'https://nos.netease.com/ydschool-online/2_youdao_PEPXiaoXue5_1.jpg', 'zipFile': '1530101080610_PEPXiaoXue5_1.zip'},
    {'id': 'PEPXiaoXue5_2', 'title': '人教版小学英语-五年级下册', 'wordCount': 156, 'category': '小学', 'grade': 5, 'term': 2, 'tag': '人教版', 'popularity': 37829, 'icon': 'https://nos.netease.com/ydschool-online/2_youdao_PEPXiaoXue5_2.jpg', 'zipFile': '1530101073491_PEPXiaoXue5_2.zip'},
    {'id': 'PEPXiaoXue6_1', 'title': '人教版小学英语-六年级上册', 'wordCount': 130, 'category': '小学', 'grade': 6, 'term': 1, 'tag': '人教版', 'popularity': 69570, 'icon': 'https://nos.netease.com/ydschool-online/2_youdao_PEPXiaoXue6_1.jpg', 'zipFile': '1530101075331_PEPXiaoXue6_1.zip'},
    {'id': 'PEPXiaoXue6_2', 'title': '人教版小学英语-六年级下册', 'wordCount': 108, 'category': '小学', 'grade': 6, 'term': 2, 'tag': '人教版', 'popularity': 38501, 'icon': 'https://nos.netease.com/ydschool-online/2_youdao_PEPXiaoXue6_2.jpg', 'zipFile': '1521164632445_PEPXiaoXue6_2.zip'},
    # 人教版初中
    {'id': 'PEPChuZhong7_1', 'title': '人教版初中英语-七年级上册', 'wordCount': 392, 'category': '初中', 'grade': 7, 'term': 1, 'tag': '人教版', 'popularity': 126509, 'icon': 'https://nos.netease.com/ydschool-online/3_youdao_PEPChuZhong7_1.jpg', 'zipFile': '1530101067588_PEPChuZhong7_1.zip'},
    {'id': 'PEPChuZhong7_2', 'title': '人教版初中英语-七年级下册', 'wordCount': 492, 'category': '初中', 'grade': 7, 'term': 2, 'tag': '人教版', 'popularity': 40795, 'icon': 'https://nos.netease.com/ydschool-online/3_youdao_PEPChuZhong7_2.jpg', 'zipFile': '1521164677043_PEPChuZhong7_2.zip'},
    {'id': 'PEPChuZhong8_1', 'title': '人教版初中英语-八年级上册', 'wordCount': 419, 'category': '初中', 'grade': 8, 'term': 1, 'tag': '人教版', 'popularity': 69006, 'icon': 'https://nos.netease.com/ydschool-online/3_youdao_PEPChuZhong8_1.jpg', 'zipFile': '1530101070747_PEPChuZhong8_1.zip'},
    {'id': 'PEPChuZhong8_2', 'title': '人教版初中英语-八年级下册', 'wordCount': 466, 'category': '初中', 'grade': 8, 'term': 2, 'tag': '人教版', 'popularity': 31355, 'icon': 'https://nos.netease.com/ydschool-online/3_youdao_PEPChuZhong8_2.jpg', 'zipFile': '1521164666522_PEPChuZhong8_2.zip'},
    {'id': 'PEPChuZhong9_1', 'title': '人教版初中英语-九年级全册', 'wordCount': 551, 'category': '初中', 'grade': 9, 'term': 1, 'tag': '人教版', 'popularity': 69649, 'icon': 'https://nos.netease.com/ydschool-online/3_youdao_PEPChuZhong9_1.jpg', 'zipFile': '1530101078234_PEPChuZhong9_1.zip'},
]


class DictImporter:
    """Dict数据导入器"""
    
    def __init__(self, db_path='lioneng.db', dict_path='./dict/book/'):
        self.db_path = db_path
        self.dict_path = dict_path
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """连接数据库"""
        print(f"📦 连接数据库: {self.db_path}")
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        print("✅ 数据库连接成功")
    
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
        
        # 词书表
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS dict_books (
            id TEXT PRIMARY KEY,
            book_id TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            word_count INTEGER DEFAULT 0,
            category TEXT,
            tag TEXT,
            grade INTEGER,
            term INTEGER,
            popularity INTEGER DEFAULT 0,
            icon TEXT,
            zip_file TEXT,
            file_size INTEGER DEFAULT 0,
            created_at TEXT,
            updated_at TEXT
        )
        """)
        
        # 单词表
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS dict_words (
            id TEXT PRIMARY KEY,
            book_id TEXT NOT NULL,
            word_rank INTEGER NOT NULL,
            head_word TEXT NOT NULL,
            uk_phone TEXT,
            us_phone TEXT,
            uk_speech TEXT,
            us_speech TEXT,
            translations TEXT,
            sentences TEXT,
            phrases TEXT,
            synonyms TEXT,
            rel_words TEXT,
            exams TEXT,
            content TEXT,
            created_at TEXT,
            UNIQUE(book_id, word_rank)
        )
        """)
        
        # 创建索引
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_book_id ON dict_books(book_id)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON dict_books(category)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_words_book_id ON dict_words(book_id)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_head_word ON dict_words(head_word)")
        
        self.conn.commit()
        print("✅ 数据表创建成功")
    
    def find_zip_file(self, book_id: str) -> str:
        """查找ZIP文件"""
        if not os.path.exists(self.dict_path):
            return None
        
        for filename in os.listdir(self.dict_path):
            if book_id in filename and filename.endswith('.zip'):
                return os.path.join(self.dict_path, filename)
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
                            # 按行解析
                            for line in content.strip().split('\n'):
                                if line.strip():
                                    try:
                                        word_data = json.loads(line)
                                        words.append(word_data)
                                    except:
                                        continue
        except Exception as e:
            print(f"  ❌ 读取ZIP文件失败: {e}")
        
        return words
    
    def extract_word_content(self, word_data: Dict[str, Any]) -> Dict[str, Any]:
        """提取单词内容"""
        content = {}
        if 'content' in word_data and isinstance(word_data['content'], dict):
            if 'word' in word_data['content'] and isinstance(word_data['content']['word'], dict):
                content = word_data['content']['word'].get('content', {})
        return content
    
    def import_book(self, book_meta: Dict[str, Any]) -> bool:
        """导入单个词书"""
        book_id = book_meta['id']
        print(f"\n📚 导入词书: {book_meta['title']} ({book_id})")
        
        # 查找ZIP文件
        zip_path = self.find_zip_file(book_id)
        if not zip_path:
            print(f"  ⚠️  未找到ZIP文件")
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
            book_uuid = str(uuid.uuid4())
            now = datetime.now().isoformat()
            
            self.cursor.execute("""
            INSERT OR REPLACE INTO dict_books 
            (id, book_id, title, word_count, category, tag, grade, term, popularity, icon, zip_file, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                book_uuid,
                book_id,
                book_meta['title'],
                len(words),
                book_meta.get('category', ''),
                book_meta.get('tag', ''),
                book_meta.get('grade', 0),
                book_meta.get('term', 0),
                book_meta.get('popularity', 0),
                book_meta.get('icon', ''),
                book_meta.get('zipFile', ''),
                now,
                now
            ))
            
            print(f"  ✅ 词书记录已插入")
        except Exception as e:
            print(f"  ❌ 插入词书记录失败: {e}")
            return False
        
        # 插入单词记录
        success_count = 0
        error_count = 0
        
        for word_data in words:
            try:
                word_rank = word_data.get('wordRank', 0)
                head_word = word_data.get('headWord', '')
                content = self.extract_word_content(word_data)
                
                uk_phone = content.get('ukphone', '')
                us_phone = content.get('usphone', '')
                uk_speech = f"https://dict.youdao.com/dictvoice?audio={head_word}&type=1"
                us_speech = f"https://dict.youdao.com/dictvoice?audio={head_word}&type=2"
                
                word_uuid = str(uuid.uuid4())
                now = datetime.now().isoformat()
                
                self.cursor.execute("""
                INSERT OR REPLACE INTO dict_words 
                (id, book_id, word_rank, head_word, uk_phone, us_phone, uk_speech, us_speech,
                 translations, sentences, phrases, synonyms, rel_words, exams, content, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    word_uuid,
                    book_id,
                    word_rank,
                    head_word,
                    uk_phone,
                    us_phone,
                    uk_speech,
                    us_speech,
                    json.dumps(content.get('trans', []), ensure_ascii=False),
                    json.dumps(content.get('sentence', {}), ensure_ascii=False),
                    json.dumps(content.get('phrase', {}), ensure_ascii=False),
                    json.dumps(content.get('syno', {}), ensure_ascii=False),
                    json.dumps(content.get('relWord', {}), ensure_ascii=False),
                    json.dumps(content.get('exam', []), ensure_ascii=False),
                    json.dumps(content, ensure_ascii=False),
                    now
                ))
                
                success_count += 1
                
                if success_count % 50 == 0:
                    print(f"  ⏳ 已导入 {success_count}/{len(words)} 个单词...")
                    
            except Exception as e:
                error_count += 1
                if error_count <= 3:  # 只显示前3个错误
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
    
    def import_all(self, books_list=None):
        """批量导入词书"""
        if books_list is None:
            books_list = BOOKS_METADATA
        
        print(f"\n🚀 开始导入 {len(books_list)} 个词书...")
        print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        success_count = 0
        for book_meta in books_list:
            if self.import_book(book_meta):
                success_count += 1
        
        print("\n" + "="*60)
        print(f"📊 导入统计:")
        print(f"  总词书数: {len(books_list)}")
        print(f"  成功: {success_count}")
        print(f"  失败: {len(books_list) - success_count}")
        print(f"⏰ 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
    
    def query_stats(self):
        """查询统计信息"""
        print("\n📊 数据库统计:")
        
        # 词书统计
        self.cursor.execute("SELECT COUNT(*) FROM dict_books")
        book_count = self.cursor.fetchone()[0]
        print(f"  词书总数: {book_count}")
        
        # 单词统计
        self.cursor.execute("SELECT COUNT(*) FROM dict_words")
        word_count = self.cursor.fetchone()[0]
        print(f"  单词总数: {word_count}")
        
        # 按分类统计
        self.cursor.execute("""
        SELECT category, COUNT(*) as count, SUM(word_count) as total_words
        FROM dict_books
        GROUP BY category
        """)
        
        print("\n  按分类统计:")
        for row in self.cursor.fetchall():
            category, count, total_words = row
            print(f"    {category}: {count}个词书, {total_words}个单词")


def main():
    """主函数"""
    print("="*60)
    print("🦁 狮子英语 - Dict词库数据导入工具")
    print("="*60)
    
    # 创建导入器
    importer = DictImporter(db_path='lioneng.db', dict_path='./dict/book/')
    
    try:
        # 连接数据库
        importer.connect()
        
        # 创建表
        importer.create_tables()
        
        # 导入数据
        importer.import_all()
        
        # 查询统计
        importer.query_stats()
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 关闭连接
        importer.close()
    
    print("\n✅ 导入完成！")
    print(f"📁 数据库文件: lioneng.db")
    print(f"💡 使用方法: sqlite3 lioneng.db")


if __name__ == '__main__':
    main()
