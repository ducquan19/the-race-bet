"""Supabase configuration."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Validate configuration
if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError("Missing Supabase configuration. Check your .env file.")
