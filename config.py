
class Config:
    """
    A class for general config parameters.
    """
    
    # ENCRYPTION AND DECRYPTON SECRET KEY
    ED_SECRET_KEY=b'6W1FqIqZBUsE3P1CWo4gUyORNopKU4AvnAlZy6ptdho='
    
    # ERROR MESSAGES
    EXTERNAL_ERROR_MESSAGE = "Unable to process the request"
    UNKNOWN_ERROR_MESSAGE = "Unknown error"
    CREDENTIALS_ERROR_MESSAGE = "Something went wrong with login"

    

    ELASTIC_ERROR_CODES = {400: 2003, 401: 2001, 404: 2002, 502: 2007, 520: 2005}
    ERROR_CODE_SERIES = {
        10: "SERVICE_ERROR_MESSAGE",
        20: "ELASTIC_ERROR_MESSAGE",
        11: "SERVER_ERROR_MESSAGE",
        60: "SYSTEM_ERROR_MESSAGE",
    }
    

    SERVICE_ERROR_MESSAGE = {
        1001: {
            "internal_message": None,
            "external_message": EXTERNAL_ERROR_MESSAGE,
        },
        1005: {
            "internal_message": UNKNOWN_ERROR_MESSAGE,
            "external_message": EXTERNAL_ERROR_MESSAGE,
        },
        1006: {
            "internal_message": "Invalid request!, Please provide a valid Email ID",
            "external_message": EXTERNAL_ERROR_MESSAGE,
        },
        1007: {
            "internal_message": "Invalid request!, Please provide a valid password",
            "external_message": EXTERNAL_ERROR_MESSAGE,
        },
        1008: {
            "internal_message": "Empty input request",
            "external_message": EXTERNAL_ERROR_MESSAGE,
        },
        1009: {
            "internal_message": "Invalid Excel report structure!, Please provide valid Excel repport structure!",
            "external_message": EXTERNAL_ERROR_MESSAGE,
        },
        1010: {
            "internal_message": "Invalid request!, Please provide password",
            "external_message": EXTERNAL_ERROR_MESSAGE,
        },
        1011: {
            "internal_message": "Invalid OTP!, Please provide valid OTP!",
            "external_message": EXTERNAL_ERROR_MESSAGE,
        },
        
        
        
    }

    ELASTIC_ERROR_MESSAGE = {
        2001: {
            "internal_message": "Failed to authenticate the elastic user",
            "external_message": CREDENTIALS_ERROR_MESSAGE,
        },
        2002: {
            "internal_message": "Index not found exception",
            "external_message": EXTERNAL_ERROR_MESSAGE,
        },
        2003: {
            "internal_message": "Object mapping for field is incorrect",
            "external_message": EXTERNAL_ERROR_MESSAGE,
        },
        2005: {
            "internal_message": UNKNOWN_ERROR_MESSAGE,
            "external_message": EXTERNAL_ERROR_MESSAGE,
        },
        2006: {
            "internal_message": "Record not found",
            "external_message": EXTERNAL_ERROR_MESSAGE,
        },
        2007: {
            "internal_message": "Please check your elastic host and port!",
            "external_message": EXTERNAL_ERROR_MESSAGE,
        },
    }

    

    SYSTEM_ERROR_MESSAGE = {
        6001: {
            "internal_message": None,
            "external_message": EXTERNAL_ERROR_MESSAGE,
        },
        6002: {
            "internal_message": None,
            "external_message": EXTERNAL_ERROR_MESSAGE,
        },
        6005: {
            "internal_message": UNKNOWN_ERROR_MESSAGE,
            "external_message": EXTERNAL_ERROR_MESSAGE,
        },
    }

    # ROUTES
    AUTH_ROUTE_NAME = "/login"
    
    
    # CSRF CONFIGURATION
    WTF_CSRF_CHECK_DEFAULT = False

    # CORS CONFIGURATION
    ROUTE_ENDPOINT_PATTERN = r"/*"
    DOMAIN_ORIGIN = "*"
    IS_CORS_ENABLED = True


class DevConfig(Config):
    """
    A Class for development config parameters.

    Args:
        Config (Config): General config parameters.
    """

    LOGGER_LEVEL = "debug"
    FILE_NAME = "logs.log"
    LOG_PATH = "logs"
    MAX_BYTES = 10240000
    BACKUP_COUNT = 1


class ProdConfig(Config):
    """
    A class for production config parameters.

    Args:
        Config (Config): General config parameters.
    """

    LOGGER_LEVEL = "debug"
    FILE_NAME = "logs.log"
    LOG_PATH = "logs"
    MAX_BYTES = 10240000
    BACKUP_COUNT = 1
