# Enhanced Dynamic Crypto Referral System - User Guide

## Overview

This system allows you to automatically generate personalized landing pages for your crypto business referrals. When someone fills out the form on your main landing page, the system creates a unique page that displays their name, earnings information, and attributes them as a referrer for future sign-ups.

## System Components

1. **Frontend Landing Page**: Collects visitor information through an enhanced form
2. **Backend API**: Processes submissions and generates personalized pages
3. **Dynamic Page Generation**: Creates unique pages with personalized content
4. **Data Storage**: Keeps records of all submissions

## Setup Instructions

### Prerequisites
- Python 3.6+ with Flask and Flask-CORS installed
- Web server with Python support
- Basic knowledge of HTML/CSS/JavaScript

### Installation Steps

1. **Extract the ZIP file** to your server directory
2. **Install dependencies**:
   ```bash
   pip install flask flask-cors
   ```
3. **Start the backend server**:
   ```bash
   cd enhanced_dynamic
   python app.py
   ```
4. **Configure your web server** to point to the enhanced_dynamic directory

## How It Works

1. **Visitor Arrives**: A potential referral visits your main landing page
2. **Form Submission**: They fill out the form with their:
   - Name (displayed throughout their page)
   - Email and phone (for contact)
   - Earnings information (daily, weekly, monthly, yearly)
   - Who referred them
3. **Backend Processing**: The system:
   - Validates the submission
   - Generates a unique referral ID
   - Creates a personalized page
   - Stores the submission data
4. **Page Generation**: A new page is created showing:
   - Their name in the title, hero section, and footer
   - Their earnings in the earnings section
   - Attribution to their referrer
5. **Confirmation**: The visitor receives a link to their personalized page

## Customization Options

### Modifying the Landing Page
- Edit `static/index.html` to change the main landing page design
- Update `static/styles.css` to modify the visual appearance

### Changing Page Templates
- Modify the HTML template in `app.py` to change the generated page layout
- Add additional fields by updating both the form and the template

### Backend Configuration
- Change the port in `app.py` if needed (default: 5000)
- Modify validation rules in the `validate_referral_data` function

## Troubleshooting

### Common Issues
- **Port already in use**: Change the port in `app.py` or stop other services using port 5000
- **Form submission errors**: Check browser console for JavaScript errors
- **Page not found**: Ensure the referral ID in the URL matches a generated directory

### Logs
- Check terminal output for server logs
- Review submission data in the `submissions` directory

## Production Deployment

For production deployment, consider:
1. Using a production WSGI server like Gunicorn
2. Setting up proper error handling and logging
3. Implementing database storage instead of file-based storage
4. Adding user authentication for admin features
5. Setting up HTTPS for secure form submissions

## Need Help?

If you encounter any issues or need further customization, please reach out for assistance.
