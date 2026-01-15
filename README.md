# 招待キリスト教会説教内容中国版検索システム

## SETUP
```shell
mkdir sermon_article
cd sermon_article
conda create -n sermon-article python=3.11 -y
conda activate sermon-article
pip install django djangorestframework
pip install django-debug-toolbar
django-admin startproject sermon_article
pip install Pillow
```

## DB(SQLite3)
```sqlite3
CREATE TABLE "sermon_article" (
    "id" varchar(16) PRIMARY KEY DEFAULT (lower(hex(randomblob(8)))), 
    "member_id" INTEGER, -- 外部キー用のカラムを追加
    "content_title" text,
    "content_summary" text,
    "content_scripture" text,
    "content_sermon_original" text,
    "content_sermon_translate" text,
    "content_tips" text,
    "language" varchar(2),
    "sermon_at" datetime NOT NULL,
    "updated_at" datetime NOT NULL,
    "created_at" datetime NOT NULL,
    -- 外部キー制約の定義
    FOREIGN KEY("member_id") REFERENCES "members"("id")
);

CREATE TABLE members ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL, -- 氏名 
    kana TEXT, -- カナ（日本語教会ではよく使う） 
    gender TEXT, -- male / female / other 
    image TEXT,  -- 写真
    birth_date TEXT, -- YYYY-MM-DD 
    role TEXT NOT NULL, -- pastor（牧師） / evangelist（伝道師） / elder（長老） / deacon（執事） / staff / volunteer
    join_date TEXT, -- 入会日 
    baptism_date TEXT, -- 洗礼日 
    phone TEXT, 
    email TEXT, 
    address TEXT, 
    notes TEXT -- 備考 
);

```

```shell
python manage.py makemigrations
python manage.py migrate
```