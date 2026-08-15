import sqlite3
import os
import uuid
from datetime import datetime
from typing import List, Optional
from .models import Memory

class MemoryStorage:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = self._get_conn()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS memories (
                        id TEXT PRIMARY KEY,
                        category TEXT NOT NULL,
                        key TEXT NOT NULL,
                        content TEXT NOT NULL,
                        importance REAL NOT NULL,
                        created_at TIMESTAMP NOT NULL,
                        updated_at TIMESTAMP NOT NULL,
                        source TEXT NOT NULL,
                        UNIQUE(category, key)
                    )
                ''')
        finally:
            conn.close()

    def create(self, category: str, key: str, content: str, importance: float = 0.5, source: str = "user") -> Memory:
        mem_id = str(uuid.uuid4())
        now = datetime.now()
        importance = max(0.0, min(1.0, importance))
        
        conn = self._get_conn()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO memories (id, category, key, content, importance, created_at, updated_at, source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (mem_id, category, key, content, importance, now, now, source))
        finally:
            conn.close()
            
        return Memory(mem_id, category, key, content, importance, now, now, source)

    def read(self, category: str, key: str) -> Optional[Memory]:
        conn = self._get_conn()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id, category, key, content, importance, created_at, updated_at, source FROM memories WHERE category = ? AND key = ?', (category, key))
                row = cursor.fetchone()
                if row:
                    return Memory(*row)
        finally:
            conn.close()
        return None

    def update(self, category: str, key: str, content: str, importance: Optional[float] = None) -> Optional[Memory]:
        now = datetime.now()
        conn = self._get_conn()
        try:
            with conn:
                cursor = conn.cursor()
                if importance is not None:
                    importance = max(0.0, min(1.0, importance))
                    cursor.execute('UPDATE memories SET content = ?, importance = ?, updated_at = ? WHERE category = ? AND key = ?',
                                   (content, importance, now, category, key))
                else:
                    cursor.execute('UPDATE memories SET content = ?, updated_at = ? WHERE category = ? AND key = ?',
                                   (content, now, category, key))
        finally:
            conn.close()
            
        return self.read(category, key)

    def delete(self, category: str, key: str) -> bool:
        conn = self._get_conn()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM memories WHERE category = ? AND key = ?', (category, key))
                rows = cursor.rowcount
            return rows > 0
        finally:
            conn.close()

    def search(self, query: str = "", category: Optional[str] = None, limit: int = 10) -> List[Memory]:
        conn = self._get_conn()
        try:
            with conn:
                cursor = conn.cursor()
                
                sql = 'SELECT id, category, key, content, importance, created_at, updated_at, source FROM memories'
                params = []
                conditions = []
                
                if category:
                    conditions.append("category = ?")
                    params.append(category)
                if query:
                    conditions.append("(key LIKE ? OR content LIKE ?)")
                    params.append(f"%{query}%")
                    params.append(f"%{query}%")
                    
                if conditions:
                    sql += " WHERE " + " AND ".join(conditions)
                    
                sql += " ORDER BY importance DESC, updated_at DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(sql, params)
                rows = cursor.fetchall()
                return [Memory(*row) for row in rows]
        finally:
            conn.close()

    def list_all(self, limit: int = 100) -> List[Memory]:
        conn = self._get_conn()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id, category, key, content, importance, created_at, updated_at, source FROM memories ORDER BY updated_at DESC LIMIT ?', (limit,))
                rows = cursor.fetchall()
                return [Memory(*row) for row in rows]
        finally:
            conn.close()
