import os

if os.getenv('ENV_CONFIG', 'development')=='development':
    from dotenv import load_dotenv
    load_dotenv()

CONFIG_NAME_MAPPER = {
    'development': '../config/config.Development.cfg',
    'production': '../config/config.Production.cfg',
}

