"""
Type definitions for the AI-powered project.
"""
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    TypeAlias,
    Union,
    runtime_checkable,
)

from pydantic import BaseModel, Field

# Basic Types
JSON: TypeAlias = Dict[str, Any]
JSONList: TypeAlias = List[JSON]
StringOrList: TypeAlias = Union[str, List[str]]
Number: TypeAlias = Union[int, float]

# AI Model Types
ModelName: TypeAlias = Literal[
    "gpt-4",
    "gpt-4-turbo-preview",
    "gpt-3.5-turbo",
    "claude-3-opus",
    "claude-3-sonnet",
    "claude-2.1",
    "claude-2",
]

ModelProvider: TypeAlias = Literal["openai", "anthropic", "google"]

# API Types
class APIResponse(BaseModel):
    """Base API response model."""
    success: bool = Field(..., description="Whether the request was successful")
    message: Optional[str] = Field(None, description="Response message")
    data: Optional[Any] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message if any")

class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(10, ge=1, le=100, description="Items per page")
    total: Optional[int] = Field(None, description="Total number of items")

class PaginatedResponse(APIResponse):
    """Paginated API response."""
    pagination: PaginationParams

# AI Request/Response Types
class AIRequest(BaseModel):
    """Base AI request model."""
    prompt: str = Field(..., min_length=1, max_length=4000)
    model: ModelName = Field(..., description="AI model to use")
    temperature: float = Field(0.7, ge=0.0, le=1.0)
    max_tokens: Optional[int] = Field(None, ge=1, le=4000)
    top_p: float = Field(1.0, ge=0.0, le=1.0)
    frequency_penalty: float = Field(0.0, ge=-2.0, le=2.0)
    presence_penalty: float = Field(0.0, ge=-2.0, le=2.0)
    stop: Optional[List[str]] = Field(None, max_items=4)
    system_message: Optional[str] = Field(None, max_length=4000)

class AIResponse(BaseModel):
    """Base AI response model."""
    text: str = Field(..., description="Generated text")
    model: ModelName = Field(..., description="Model used")
    usage: Dict[str, int] = Field(..., description="Token usage")
    finish_reason: str = Field(..., description="Reason for completion")
    created: int = Field(..., description="Timestamp")

# Data Processing Types
class DataProcessor(Protocol):
    """Protocol for data processing classes."""
    
    def process(self, data: Any) -> Any:
        """Process the input data."""
        ...

    def validate(self, data: Any) -> bool:
        """Validate the input data."""
        ...

@runtime_checkable
class AsyncDataProcessor(Protocol):
    """Protocol for async data processing classes."""
    
    async def process(self, data: Any) -> Any:
        """Process the input data asynchronously."""
        ...

    async def validate(self, data: Any) -> bool:
        """Validate the input data asynchronously."""
        ...

# Database Types
class DatabaseConfig(BaseModel):
    """Database configuration."""
    host: str
    port: int
    database: str
    user: str
    password: str
    ssl_mode: Optional[str] = "prefer"
    pool_size: int = 5
    max_overflow: int = 10

# Cache Types
class CacheConfig(BaseModel):
    """Cache configuration."""
    host: str
    port: int
    db: int = 0
    password: Optional[str] = None
    ttl: int = 3600  # Default TTL in seconds

# Logging Types
class LogConfig(BaseModel):
    """Logging configuration."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[str] = None
    max_size: int = 10485760  # 10MB
    backup_count: int = 5

# Security Types
class SecurityConfig(BaseModel):
    """Security configuration."""
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    allowed_hosts: List[str] = Field(default_factory=list)
    cors_origins: List[str] = Field(default_factory=list)

# Rate Limiting Types
class RateLimitConfig(BaseModel):
    """Rate limiting configuration."""
    enabled: bool = True
    requests_per_minute: int = 60
    burst_size: int = 10
    storage: Literal["memory", "redis"] = "memory"

# Monitoring Types
class MetricsConfig(BaseModel):
    """Metrics configuration."""
    enabled: bool = True
    port: int = 9090
    path: str = "/metrics"
    labels: Dict[str, str] = Field(default_factory=dict)

# Error Types
class APIError(Exception):
    """Base API error."""
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)

class ValidationError(APIError):
    """Validation error."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 422, details)

class AuthenticationError(APIError):
    """Authentication error."""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401)

class AuthorizationError(APIError):
    """Authorization error."""
    def __init__(self, message: str = "Not authorized"):
        super().__init__(message, 403)

class NotFoundError(APIError):
    """Not found error."""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)

class RateLimitError(APIError):
    """Rate limit error."""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, 429)

# Utility Types
class TimestampedModel(BaseModel):
    """Base model with timestamps."""
    created_at: int = Field(..., description="Creation timestamp")
    updated_at: int = Field(..., description="Last update timestamp")

class IDModel(TimestampedModel):
    """Base model with ID and timestamps."""
    id: str = Field(..., description="Unique identifier")

# Type Guards
def is_valid_json(value: Any) -> bool:
    """Check if value is valid JSON."""
    try:
        if isinstance(value, (dict, list, str, int, float, bool, type(None))):
            return True
        return False
    except Exception:
        return False

def is_valid_timestamp(value: Any) -> bool:
    """Check if value is a valid timestamp."""
    try:
        if isinstance(value, (int, float)) and value > 0:
            return True
        return False
    except Exception:
        return False 