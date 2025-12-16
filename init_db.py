import sqlite3

conn = sqlite3.connect('tablets.db')
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS tablets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,           -- 平板編號
    owner TEXT,                   -- 使用班級 / 老師
    status TEXT NOT NULL,         -- 正常 / 借出 / 故障 / 停用
    battery INTEGER DEFAULT 100,  -- 電量 %
    location TEXT,                -- 教室 / 保管處
    note TEXT,                    -- 備註
    updated_at TEXT
)
""")

conn.commit()
conn.close()
print("✅ 資料庫初始化完成")
