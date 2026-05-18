"""
初始化 baseline 数据库
"""
import sqlite3
import os
import json

db_path = os.path.join(os.path.dirname(__file__), 'data', 'baseline.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 创建表
cursor.execute('''
CREATE TABLE IF NOT EXISTS baseline_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL,
    metric_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# 插入示例数据
categories = ['food', 'fashion', 'tech', 'travel', 'beauty', 'fitness', 'lifestyle', 'home']

for cat in categories:
    cursor.execute('INSERT OR IGNORE INTO baseline_stats (category, metric_name, metric_value) VALUES (?, ?, ?)', 
                  (cat, 'avg_title_length', 18))
    cursor.execute('INSERT OR IGNORE INTO baseline_stats (category, metric_name, metric_value) VALUES (?, ?, ?)', 
                  (cat, 'viral_avg_title_length', 20))
    cursor.execute('INSERT OR IGNORE INTO baseline_stats (category, metric_name, metric_value) VALUES (?, ?, ?)', 
                  (cat, 'avg_tag_count', 6))
    cursor.execute('INSERT OR IGNORE INTO baseline_stats (category, metric_name, metric_value) VALUES (?, ?, ?)', 
                  (cat, 'cover_avg_saturation', 0.55))
    cursor.execute('INSERT OR IGNORE INTO baseline_stats (category, metric_name, metric_value) VALUES (?, ?, ?)', 
                  (cat, 'viral_cover_avg_saturation', 0.6))
    cursor.execute('INSERT OR IGNORE INTO baseline_stats (category, metric_name, metric_value) VALUES (?, ?, ?)', 
                  (cat, 'cover_avg_text_ratio', 0.2))
    cursor.execute('INSERT OR IGNORE INTO baseline_stats (category, metric_name, metric_value) VALUES (?, ?, ?)', 
                  (cat, 'cover_face_rate', 30))
    cursor.execute('INSERT OR IGNORE INTO baseline_stats (category, metric_name, metric_value) VALUES (?, ?, ?)', 
                  (cat, 'viral_rate', 5))
    cursor.execute('INSERT OR IGNORE INTO baseline_stats (category, metric_name, metric_value) VALUES (?, ?, ?)', 
                  (cat, 'avg_engagement', 1250))
    
    top_tags = [{'tag': f'{cat}_热门1', 'count': 1000}, {'tag': f'{cat}_热门2', 'count': 800}]
    cursor.execute('INSERT OR IGNORE INTO baseline_stats (category, metric_name, metric_json) VALUES (?, ?, ?)', 
                  (cat, 'top_tags', json.dumps(top_tags)))
    
    hour_dist = [{'hour': 18, 'avg_engagement': 2000}, {'hour': 19, 'avg_engagement': 2500}, {'hour': 20, 'avg_engagement': 2300}]
    cursor.execute('INSERT OR IGNORE INTO baseline_stats (category, metric_name, metric_json) VALUES (?, ?, ?)', 
                  (cat, 'hour_distribution', json.dumps(hour_dist)))

conn.commit()
conn.close()
print('Database initialized successfully!')
