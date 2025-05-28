# Enhanced Dynamic Crypto Referral System Requirements

## Overview
The enhanced crypto referral system will collect detailed information from users via a form and generate fully personalized landing pages that display the collected information. This system requires both frontend and backend components to work together.

## Form Data Collection Requirements
The form must collect the following information:
1. **User's Name** - To be displayed throughout their personalized page
2. **User's Email** - For contact purposes
3. **User's Phone Number** - For contact purposes
4. **User's Earnings Information**:
   - Daily earnings amount
   - Weekly earnings amount
   - Monthly earnings amount
   - Yearly earnings amount
5. **Referrer's Name** - The person who referred them to the site

## Personalized Page Requirements
Each generated page must display:
1. **User's Name** - Prominently displayed in:
   - Page title
   - Hero section headline
   - Testimonial section
   - Footer
2. **User's Earnings** - Displayed in the earnings section:
   - Daily amount
   - Weekly amount
   - Monthly amount
   - Yearly amount
3. **Referrer Attribution** - Text indicating who referred them

## Technical Requirements
1. **Backend Processing**:
   - Receive and validate form submissions
   - Generate unique URLs for each referral
   - Create personalized HTML pages
   - Store submission data for reference

2. **Frontend Integration**:
   - Form with all required fields
   - Client-side validation
   - Success message with link to personalized page

3. **Deployment**:
   - Backend must be accessible via public URL
   - Generated pages must be publicly accessible
   - System must handle concurrent submissions

## User Flow
1. Visitor arrives at the main landing page
2. Visitor fills out the form with their information
3. System processes the submission
4. System generates a personalized page
5. Visitor receives confirmation with their unique URL
6. Visitor can access their personalized page
7. Visitor can share their personalized page with others

## Additional Considerations
- Each personalized page should have its own unique URL
- The system should handle special characters and input sanitization
- The design should be consistent between the main page and generated pages
- Mobile responsiveness must be maintained on all pages
