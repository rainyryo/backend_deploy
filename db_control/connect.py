# db_control/connect.py

from sqlalchemy import create_engine
import os
from pathlib import Path
from dotenv import load_dotenv

# デバッグ用：プラットフォーム情報
import platform
print("platform:", platform.uname())

# .envの読み込み（プロジェクトのルート直下にあることを前提）
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

# 環境変数からMySQL接続情報を取得
DB_USER     = os.getenv("DB_USER")     # 例: tech0gen10student@rdbs-xxx
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST     = os.getenv("DB_HOST")     # 例: rdbs-xxx.mysql.database.azure.com
DB_PORT     = os.getenv("DB_PORT", "3306")
DB_NAME     = os.getenv("DB_NAME")
SSL_CA_PATH = os.getenv("SSL_CA_PATH") # 例: DigiCertGlobalRootCA.crt.pem

# 必須変数が無い場合はエラー
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
    raise RuntimeError("DB_USER, DB_PASSWORD, DB_HOST, DB_NAME のいずれかが設定されていません")

# MySQL用のSQLAlchemy URL
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# SSL証明書設定（必要なら）
connect_args = {}
if SSL_CA_PATH:
    ca_file = Path(__file__).resolve().parent.parent / SSL_CA_PATH
    if not ca_file.is_file():
        raise FileNotFoundError(f"SSL CA file not found: {ca_file}")
    connect_args["ssl"] = {"ca": str(ca_file)}

# SQLAlchemyエンジン生成（MySQL用）
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args=connect_args
)
