#from sqlalchemy import create_engine
## import sqlalchemy

#import os
## uname() error回避
#import platform
#print("platform:", platform.uname())


#main_path = os.path.dirname(os.path.abspath(__file__))
#path = os.chdir(main_path)
#print("path:", path)
#engine = create_engine("sqlite:///CRM.db", echo=True)

from sqlalchemy import create_engine
import os
from pathlib import Path
from dotenv import load_dotenv
import platform

# 環境情報の出力 (デバッグ用)
print("platform:", platform.uname())

# このスクリプトがあるディレクトリをカレントに設定
script_dir = Path(__file__).resolve().parent
os.chdir(script_dir)
print("current working directory:", script_dir)

# プロジェクトのルートにある .env を読み込む
load_dotenv(script_dir.parent / '.env')

# 必要な環境変数を取得
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")
SSL_CA_PATH = os.getenv("SSL_CA_PATH")

# 環境変数の存在チェック
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
    raise RuntimeError("One or more required database environment variables are missing")

# SQLAlchemy 用の MySQL 接続 URL を作成
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SSL 設定があれば connect_args に追加
connect_args = {}
if SSL_CA_PATH:
    ca_path = script_dir.parent / SSL_CA_PATH
    if not ca_path.exists():
        raise FileNotFoundError(f"SSL CA file not found at {ca_path}")
    connect_args["ssl"] = { "ca": str(ca_path) }

# SQLAlchemy エンジンを作成
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args=connect_args
)
