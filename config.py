import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()


class Settings:
    """Application settings - Simple class approach (no Pydantic)"""

    # Supabase Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    SUPABASE_DB_URL: str = os.getenv("SUPABASE_DB_URL", "")
    SCHEMA: str = os.getenv("SCHEMA", "")

    # Application Configuration
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    APP_NAME: str = os.getenv("APP_NAME", "FinOrbit Backend")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")

    @property
    def is_supabase_configured(self) -> bool:
        """Check if Supabase is properly configured"""
        return all([
            self.SCHEMA,
            self.SUPABASE_URL,
            self.SUPABASE_KEY,
            self.SUPABASE_DB_URL
        ])

    def __repr__(self):
        return f"Settings(DEBUG={self.DEBUG}, SUPABASE_URL={'configured' if self.SUPABASE_URL else 'not set'})"


# Create settings instance
settings = Settings()

# Print status on import
print(f"Settings loaded: {settings}")
print(f"Supabase configured: {settings.is_supabase_configured}")