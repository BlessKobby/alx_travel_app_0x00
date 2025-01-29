# settings.py

# Celery Configuration
CELERY_BROKER_URL = 'amqp://localhost'  # RabbitMQ as the message broker
CELERY_RESULT_BACKEND = 'rpc://'  # Optional: For storing task results
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Email Configuration (for sending emails)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Example: Gmail SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'  # Replace with your email
EMAIL_HOST_PASSWORD = 'your_email_password'  # Replace with your email password