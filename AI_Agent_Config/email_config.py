# Email backend settings for Django
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587  # Use 465 if using SSL instead of TLS
EMAIL_USE_TLS = True  # Use SSL if you selected port 465
EMAIL_HOST_USER = 'security@web.afriwallstreet.com'
EMAIL_HOST_PASSWORD = '3S9Fnsh7sRTm'  # Replace with your actual email password
DEFAULT_FROM_EMAIL = '"Afriwallstreet" <security@web.afriwallstreet.com>'


PASSWORD_RESET_TIMEOUT = 900