# Enhanced Dynamic Crypto Referral System - Backend Design

## API Endpoints

### 1. Submit Referral Form
- **Endpoint**: `/api/submit-referral`
- **Method**: POST
- **Purpose**: Process form submissions and generate personalized pages
- **Request Body**:
  ```json
  {
    "name": "User's full name",
    "email": "user@example.com",
    "phone": "555-123-4567",
    "earnings": {
      "daily": 100.00,
      "weekly": 700.00,
      "monthly": 3000.00,
      "yearly": 36000.00
    },
    "referrer": "Name of person who referred them"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Referral page created successfully",
    "referral_id": "unique_identifier",
    "page_url": "/referral/unique_identifier"
  }
  ```

### 2. List Referrals
- **Endpoint**: `/api/referrals`
- **Method**: GET
- **Purpose**: Retrieve list of all referrals (admin functionality)
- **Response**:
  ```json
  {
    "success": true,
    "referrals": [
      {
        "id": "unique_identifier",
        "name": "User's name",
        "email": "user@example.com",
        "timestamp": "2025-05-28T20:57:40Z",
        "page_url": "/referral/unique_identifier"
      }
    ]
  }
  ```

## Data Storage

### Referral Submissions
- Store all form submissions as JSON files
- File naming: `{sanitized_name}_{unique_id}.json`
- Directory: `/submissions/`
- Content structure:
  ```json
  {
    "referral_data": {
      "name": "User's full name",
      "email": "user@example.com",
      "phone": "555-123-4567",
      "earnings": {
        "daily": 100.00,
        "weekly": 700.00,
        "monthly": 3000.00,
        "yearly": 36000.00
      },
      "referrer": "Name of person who referred them"
    },
    "timestamp": "2025-05-28T20:57:40Z",
    "page_dir": "/path/to/generated/page",
    "referral_id": "unique_identifier"
  }
  ```

## Page Generation

### Directory Structure
- Base directory: `/generated_pages/`
- Each referral gets its own directory: `/generated_pages/{referral_id}/`
- Files in each directory:
  - `index.html` - Main personalized page
  - `referral-data.js` - JavaScript file with referral data
  - Static assets (shared or copied)

### Generation Process
1. Validate incoming form data
2. Generate a unique referral ID
3. Create directory for the referral
4. Generate personalized HTML using templates
5. Create referral data JavaScript file
6. Save submission data for reference
7. Return success response with URL

## Validation Logic

### Form Validation
- **Name**: Required, string, trim whitespace
- **Email**: Required, valid email format
- **Phone**: Optional, standardize format
- **Earnings**:
  - All values must be numeric
  - All values must be positive
  - Weekly should be ~7x daily
  - Monthly should be ~30x daily
  - Yearly should be ~365x daily
  - If any value is missing, calculate based on provided values
- **Referrer**: Required, string, trim whitespace

## Security Considerations

### Input Sanitization
- Sanitize all user inputs to prevent XSS attacks
- Escape special characters in HTML output
- Validate numeric inputs for earnings

### URL Generation
- Use sanitized name (lowercase, spaces to underscores)
- Append unique identifier to prevent collisions
- Ensure URLs are predictable but unique

## Error Handling
- Validate all inputs and return specific error messages
- Log errors for debugging
- Provide user-friendly error responses
- Handle edge cases (duplicate submissions, invalid data)

## Performance Considerations
- Optimize page generation for speed
- Use caching where appropriate
- Ensure concurrent submissions are handled properly
- Implement rate limiting to prevent abuse
