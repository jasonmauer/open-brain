"""
Open Brain Setup Wizard

Interactive first-run setup for Open Brain.
Configures database, embedder, and notifications.
"""

import os
import yaml
from pathlib import Path


def run_setup():
    """Run the interactive setup wizard."""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                  Open Brain Setup Wizard                  ║
║                                                           ║
║  Let's configure your personal semantic memory system.    ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    config = {}
    
    # 1. Database Configuration
    print("\n📀 DATABASE CONFIGURATION")
    print("-" * 40)
    config['database'] = {
        'host': input("Database host [localhost]: ") or "localhost",
        'port': input("Database port [5432]: ") or "5432",
        'name': input("Database name [openbrain]: ") or "openbrain",
        'user': input("Database user [postgres]: ") or "postgres",
        'password': input("Database password: "),
    }
    
    # 2. Embedder Configuration  
    print("\n🧠 EMBEDDING PROVIDER")
    print("-" * 40)
    print("Choose your embedding provider:")
    print("  1. OpenRouter (FREE - recommended)")
    print("  2. OpenAI")
    print("  3. Ollama (local)")
    print("  4. Custom (any OpenAI-compatible API)")
    
    provider_choice = input("\nChoose [1-4]: ") or "1"
    
    provider_map = {'1': 'openrouter', '2': 'openai', '3': 'ollama', '4': 'custom'}
    provider = provider_map.get(provider_choice, 'openrouter')
    
    config['embedder'] = {'provider': provider}
    
    if provider == 'openrouter':
        config['embedder']['model'] = input("Model [text-embedding-3-small]: ") or "text-embedding-3-small"
        api_key = input("\n🔑 OpenRouter API Key: ")
        if api_key:
            print(f"  Set OPENROUTER_API_KEY={api_key[:10]}...")
            os.environ['OPENROUTER_API_KEY'] = api_key
            
    elif provider == 'openai':
        config['embedder']['model'] = input("Model [text-embedding-3-small]: ") or "text-embedding-3-small"
        api_key = input("\n🔑 OpenAI API Key (sk-...): ")
        if api_key:
            os.environ['OPENAI_API_KEY'] = api_key
            
    elif provider == 'ollama':
        config['embedder']['model'] = input("Model [nomic-embed-text]: ") or "nomic-embed-text"
        config['embedder']['ollama_base_url'] = input("Ollama URL [http://localhost:11434]: ") or "http://localhost:11434"
        
    elif provider == 'custom':
        config['embedder']['model'] = input("Model name: ")
        config['embedder']['custom_base_url'] = input("API Base URL: ")
        api_key = input("🔑 API Key: ")
        if api_key:
            os.environ['CUSTOM_API_KEY'] = api_key
    
    config['embedder']['dimensions'] = 768
    
    # 3. Notifications (Optional)
    print("\n📬 NOTIFICATIONS (Optional)")
    print("-" * 40)
    
    enable_telegram = input("Enable Telegram notifications? [y/N]: ").lower() == 'y'
    if enable_telegram:
        config['analytics']['notifications']['telegram'] = {
            'enabled': True,
            'bot_token': input("Telegram Bot Token: "),
            'chat_id': input("Telegram Chat ID: "),
        }
    
    enable_email = input("Enable email notifications? [y/N]: ").lower() == 'y'
    if enable_email:
        config['analytics']['notifications']['email'] = {
            'enabled': True,
            'smtp_host': input("SMTP Host: "),
            'smtp_port': input("SMTP Port [587]: ") or "587",
            'smtp_user': input("SMTP User: "),
            'smtp_password': input("SMTP Password: "),
            'from_email': input("From Email: "),
        }
    
    # 4. API Server
    print("\n🌐 API SERVER")
    print("-" * 40)
    config['api'] = {
        'host': '0.0.0.0',
        'port': int(input("API port [8000]: ") or "8000"),
        'cors_origins': ["*"],
    }
    
    config['mcp'] = {
        'host': '0.0.0.0',
        'port': int(input("MCP port [8080]: ") or "8080"),
    }
    
    config['dashboard'] = {
        'port': int(input("Dashboard port [8501]: ") or "8501"),
    }
    
    # 5. Security
    print("\n🔒 SECURITY")
    print("-" * 40)
    security_mode = input("Security mode (direct/sandbox) [direct]: ") or "direct"
    config['security'] = {
        'mode': security_mode,
    }
    
    # Save configuration
    print("\n💾 SAVING CONFIGURATION")
    print("-" * 40)
    
    config_path = Path(__file__).parent.parent / "config" / "settings.yaml"
    config_path.parent.mkdir(exist_ok=True)
    
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    print(f"✓ Configuration saved to: {config_path}")
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║                   SETUP COMPLETE!                         ║
║                                                           ║
║  Next steps:                                              ║
║  1. Start PostgreSQL with pgvector                      ║
║  2. Run: python scripts/setup_db.py                     ║
║  3. Run: docker compose up -d                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    return config


if __name__ == "__main__":
    run_setup()
