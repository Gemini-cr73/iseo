from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # -----------------------------
    # APP
    # -----------------------------
    env: str = Field(default="dev", alias="ISEO_ENV")
    app_name: str = Field(default="ISEO v2", alias="ISEO_APP_NAME")
    log_level: str = Field(default="INFO", alias="ISEO_LOG_LEVEL")

    # -----------------------------
    # DATABASE
    # -----------------------------
    # Priority:
    # 1. DATABASE_URL (Railway / Postgres)
    # 2. ISEO_DB_PATH (local SQLite fallback)
    database_url: str | None = Field(default=None, alias="DATABASE_URL")

    db_path: str = Field(
        default="./data/iseo.sqlite",
        alias="ISEO_DB_PATH",
    )

    # -----------------------------
    # VECTOR STORE (RAG)
    # -----------------------------
    chroma_dir: str = Field(
        default="/app/data/chroma",  # container-safe
        alias="ISEO_CHROMA_DIR",
    )

    chroma_collection: str = Field(
        default="iseo_knowledge",
        alias="ISEO_CHROMA_COLLECTION",
    )

    # -----------------------------
    # EMBEDDINGS
    # -----------------------------
    embed_model: str = Field(
        default="all-MiniLM-L6-v2",
        alias="ISEO_EMBED_MODEL",
    )

    # -----------------------------
    # LLM (GROQ)
    # -----------------------------
    llm_provider: str = Field(default="groq", alias="LLM_PROVIDER")

    groq_api_key: str = Field(default="", alias="GROQ_API_KEY")

    groq_model: str = Field(
        default="llama-3.3-70b-versatile",
        alias="GROQ_MODEL",
    )


settings = Settings()
