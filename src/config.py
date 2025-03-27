"""
Configuration management for the AI-powered project.
"""
import os
from typing import Optional

from pydantic import BaseSettings, Field, validator
from pydantic.networks import PostgresDsn, RedisDsn

from .types import (
    CacheConfig,
    DatabaseConfig,
    LogConfig,
    MetricsConfig,
    RateLimitConfig,
    SecurityConfig,
)

class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    APP_NAME: str = "AI-Powered Project"
    APP_ENV: str = "development"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALLOWED_HOSTS: list[str] = Field(default_factory=list)
    CORS_ORIGINS: list[str] = Field(default_factory=list)
    
    # Database
    POSTGRES_SERVER: str = Field(..., env="POSTGRES_SERVER")
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")
    POSTGRES_PORT: str = Field(..., env="POSTGRES_PORT")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    
    # Redis
    REDIS_HOST: str = Field(..., env="REDIS_HOST")
    REDIS_PORT: int = Field(..., env="REDIS_PORT")
    REDIS_PASSWORD: Optional[str] = Field(None, env="REDIS_PASSWORD")
    REDIS_DB: int = 0
    REDIS_URI: Optional[RedisDsn] = None
    
    # AI Models
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    GOOGLE_API_KEY: Optional[str] = Field(None, env="GOOGLE_API_KEY")
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: Optional[str] = None
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 60
    RATE_LIMIT_BURST: int = 10
    RATE_LIMIT_STORAGE: str = "memory"
    
    # Metrics
    METRICS_ENABLED: bool = True
    METRICS_PORT: int = 9090
    METRICS_PATH: str = "/metrics"
    
    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, any]) -> PostgresDsn:
        """Assemble database connection string."""
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
    
    @validator("REDIS_URI", pre=True)
    def assemble_redis_connection(cls, v: Optional[str], values: dict[str, any]) -> RedisDsn:
        """Assemble Redis connection string."""
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme="redis",
            host=values.get("REDIS_HOST"),
            port=values.get("REDIS_PORT"),
            password=values.get("REDIS_PASSWORD"),
            path=f"/{values.get('REDIS_DB') or '0'}",
        )
    
    def get_database_config(self) -> DatabaseConfig:
        """Get database configuration."""
        return DatabaseConfig(
            host=self.POSTGRES_SERVER,
            port=int(self.POSTGRES_PORT),
            database=self.POSTGRES_DB,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
        )
    
    def get_cache_config(self) -> CacheConfig:
        """Get cache configuration."""
        return CacheConfig(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            password=self.REDIS_PASSWORD,
            db=self.REDIS_DB,
        )
    
    def get_log_config(self) -> LogConfig:
        """Get logging configuration."""
        return LogConfig(
            level=self.LOG_LEVEL,
            format=self.LOG_FORMAT,
            file=self.LOG_FILE,
        )
    
    def get_security_config(self) -> SecurityConfig:
        """Get security configuration."""
        return SecurityConfig(
            secret_key=self.SECRET_KEY,
            algorithm=self.ALGORITHM,
            access_token_expire_minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES,
            refresh_token_expire_days=self.REFRESH_TOKEN_EXPIRE_DAYS,
            allowed_hosts=self.ALLOWED_HOSTS,
            cors_origins=self.CORS_ORIGINS,
        )
    
    def get_rate_limit_config(self) -> RateLimitConfig:
        """Get rate limiting configuration."""
        return RateLimitConfig(
            enabled=self.RATE_LIMIT_ENABLED,
            requests_per_minute=self.RATE_LIMIT_REQUESTS,
            burst_size=self.RATE_LIMIT_BURST,
            storage=self.RATE_LIMIT_STORAGE,
        )
    
    def get_metrics_config(self) -> MetricsConfig:
        """Get metrics configuration."""
        return MetricsConfig(
            enabled=self.METRICS_ENABLED,
            port=self.METRICS_PORT,
            path=self.METRICS_PATH,
        )
    
    class Config:
        """Pydantic configuration."""
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create global settings instance
settings = Settings() 