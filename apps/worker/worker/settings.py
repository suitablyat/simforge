import os
from pydantic import BaseModel, Field

class Settings(BaseModel):
    redis_url: str = Field(default_factory=lambda: os.getenv("REDIS_URL", "redis://redis:6379/0"))
    simc_bin: str | None = Field(default_factory=lambda: os.getenv("SIMC_BIN", None))
    simc_bin_nightly: str = Field(
        default_factory=lambda: os.getenv("SIMC_BIN_NIGHTLY", "/opt/simc/nightly/simc")
    )
    simc_bin_weekly: str = Field(
        default_factory=lambda: os.getenv("SIMC_BIN_WEEKLY", "/opt/simc/weekly/simc")
    )
    simc_default_channel: str = Field(default_factory=lambda: os.getenv("SIMC_DEFAULT_CHANNEL", "latest"))
    simc_threads: int = int(os.getenv("SIMC_THREADS", "4"))
    simc_timeout_sec: int = int(os.getenv("SIMC_TIMEOUT_SEC", "120"))
    simc_log_dir: str = os.getenv("SIMC_LOG_DIR", "/app/logs")

settings = Settings()
