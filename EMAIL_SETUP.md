# Email Configuration Guide

The application can send email notifications for grade disputes. To enable email functionality, you need to configure SMTP settings.

## Configuration

Add the following environment variables to your `.env` file:

```env
# Email/SMTP Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_USE_TLS=true
```

## Gmail Setup

If using Gmail, you'll need to:

1. Enable 2-Factor Authentication on your Google account
2. Generate an "App Password" (not your regular password):
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
   - Use this app password as `SMTP_PASSWORD`

## Other Email Providers

### Outlook/Hotmail
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USE_TLS=true
```

### Yahoo
```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USE_TLS=true
```

### Custom SMTP Server
```env
SMTP_HOST=your-smtp-server.com
SMTP_PORT=587
SMTP_USE_TLS=true
```

## Testing

When a student disputes a grade, an email will be automatically sent to the instructor's email address (from the User model) with:
- Subject: "<Student name> <course name> <exam name> GRADE DISPUTED"
- Content: Full exam details including questions, answers, grades, and dispute reason

If email is not configured, the application will log a warning but continue to function normally (in-app notifications will still work).
