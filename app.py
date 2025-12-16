from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB = 'tablets.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# 取得所有平板
@app.route('/api/tablets', methods=['GET'])
def get_tablets():
    conn = get_db()
    rows = conn.execute("SELECT * FROM tablets ORDER BY id").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

# 新增平板
@app.route('/api/tablets', methods=['POST'])
def add_tablet():
    data = request.json
    conn = get_db()
    conn.execute("""
        INSERT INTO tablets
        (code, owner, status, battery, location, note, updated_at)
        VALUES (?,?,?,?,?,?,?)
    """, (
        data['code'],
        data.get('owner', ''),
        data.get('status', '正常'),
        data.get('battery', 100),
        data.get('location', ''),
        data.get('note', ''),
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# 更新平板
@app.route('/api/tablets/<int:tid>', methods=['PUT'])
def update_tablet(tid):
    data = request.json
    conn = get_db()
    conn.execute("""
        UPDATE tablets SET
        code=?, owner=?, status=?, battery=?, location=?, note=?, updated_at=?
        WHERE id=?
    """, (
        data['code'],
        data['owner'],
        data['status'],
        data['battery'],
        data['location'],
        data.get('note', ''),
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        tid
    ))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# 刪除平板
@app.route('/api/tablets/<int:tid>', methods=['DELETE'])
def delete_tablet(tid):
    conn = get_db()
    conn.execute("DELETE FROM tablets WHERE id=?", (tid,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
