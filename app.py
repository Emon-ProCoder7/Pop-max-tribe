from flask import Flask, request, jsonify, send_from_directory
import os
import json
import shutil
import uuid
from datetime import datetime
import subprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_BASE_DIR = os.path.join(BASE_DIR, "generated_pages")
SUBMISSIONS_DIR = os.path.join(BASE_DIR, "submissions")
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

# Ensure directories exist
os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)
os.makedirs(SUBMISSIONS_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATE_DIR, exist_ok=True)

def validate_referral_data(data):
    """Validate the referral data structure."""
    errors = []
    
    # Check required fields
    if 'name' not in data or not data['name'].strip():
        errors.append("Name is required")
    
    if 'email' not in data or not data['email'].strip():
        errors.append("Email is required")
    
    if 'referrer' not in data or not data['referrer'].strip():
        errors.append("Referrer name is required")
    
    # Validate earnings if provided
    if 'earnings' in data:
        if not isinstance(data['earnings'], dict):
            errors.append("Earnings must be a dictionary")
        else:
            # Ensure daily earnings is provided
            if 'daily' not in data['earnings'] or not data['earnings']['daily']:
                errors.append("Daily earnings is required")
            
            # Convert earnings values to float
            for field in ['daily', 'weekly', 'monthly', 'yearly']:
                if field in data['earnings']:
                    try:
                        data['earnings'][field] = float(data['earnings'][field])
                    except (ValueError, TypeError):
                        errors.append(f"{field.capitalize()} earnings must be a number")
            
            # Calculate missing earnings based on daily value
            if 'daily' in data['earnings'] and isinstance(data['earnings']['daily'], (int, float)):
                daily = data['earnings']['daily']
                
                if 'weekly' not in data['earnings'] or not data['earnings']['weekly']:
                    data['earnings']['weekly'] = daily * 7
                
                if 'monthly' not in data['earnings'] or not data['earnings']['monthly']:
                    data['earnings']['monthly'] = daily * 30
                
                if 'yearly' not in data['earnings'] or not data['earnings']['yearly']:
                    data['earnings']['yearly'] = daily * 365
    else:
        errors.append("Earnings information is required")
    
    return errors, data

def create_referral_page(referral_data):
    """
    Create a personalized landing page for a referral.
    
    Args:
        referral_data (dict): Dictionary containing referral information
    
    Returns:
        dict: Result information including path and URL
    """
    # Validate referral data
    errors, referral_data = validate_referral_data(referral_data)
    if errors:
        return {"success": False, "errors": errors}
    
    # Create a sanitized directory name from referral name and unique ID
    referral_name = referral_data["name"].lower().replace(" ", "_")
    unique_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate referral ID that will be used consistently for both directory and URL
    referral_id = f"{referral_name}_{unique_id}"
    
    # Generate directory name
    page_dir = os.path.join(OUTPUT_BASE_DIR, referral_id)
    
    # Create output directory
    os.makedirs(page_dir, exist_ok=True)
    
    # Create the referral data injection script
    print(f"Creating referral data injection script for {referral_data['name']}...")
    referral_data_js = f"""
// Referral data for {referral_data['name']}
window.REFERRAL_DATA = {json.dumps(referral_data, indent=2)};
"""
    
    # Write the referral data to a JavaScript file
    with open(os.path.join(page_dir, "referral-data.js"), 'w') as f:
        f.write(referral_data_js)
    
    # Format earnings with proper currency formatting
    daily = f"${referral_data['earnings']['daily']:.2f}"
    weekly = f"${referral_data['earnings']['weekly']:.2f}"
    monthly = f"${referral_data['earnings']['monthly']:.2f}"
    yearly = f"${referral_data['earnings']['yearly']:.2f}"
    
    # Create a personalized HTML file with the referral data
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Success - {referral_data['name']}'s Page</title>
    <link rel="stylesheet" href="/static/styles.css">
    <script src="referral-data.js"></script>
</head>
<body>
    <header class="header">
        <div class="logo">CryptoSuccess</div>
        <nav class="nav">
            <a href="#home">Home</a>
            <a href="#earnings">Earnings</a>
            <a href="#testimonial">Testimonial</a>
            <a href="#join">Join Now</a>
        </nav>
    </header>

    <section id="home" class="hero-section">
        <div class="hero-content">
            <h1>Join {referral_data['name']}'s Crypto Success Story</h1>
            <p>Discover how you can earn passive income through our proven crypto business model</p>
            <button class="cta-button">Get Started Now</button>
        </div>
    </section>

    <section id="earnings" class="earnings-section">
        <h2>{referral_data['name']}'s Actual Earnings</h2>
        <div class="earnings-grid">
            <div class="earnings-card">
                <h3>Daily</h3>
                <p class="amount">{daily}</p>
            </div>
            <div class="earnings-card">
                <h3>Weekly</h3>
                <p class="amount">{weekly}</p>
            </div>
            <div class="earnings-card">
                <h3>Monthly</h3>
                <p class="amount">{monthly}</p>
            </div>
            <div class="earnings-card">
                <h3>Yearly</h3>
                <p class="amount">{yearly}</p>
            </div>
        </div>
    </section>

    <section id="testimonial" class="video-section">
        <h2>Hear From {referral_data['name']} Directly</h2>
        <div class="video-container">
            <div class="video-placeholder">
                <p>Video testimonial coming soon</p>
            </div>
        </div>
        <div class="testimonial-text">
            <p>"I never thought crypto could change my life until I discovered this business model. Now I'm earning passive income every day!"</p>
            <p class="testimonial-author">- {referral_data['name']}</p>
        </div>
    </section>

    <section id="join" class="join-section">
        <h2>Ready to Start Your Crypto Journey?</h2>
        <p>Join through {referral_data['name']}'s referral and get exclusive bonuses!</p>
        <form class="signup-form" id="referralForm">
            <div class="form-group">
                <label for="userName">Your Name</label>
                <input type="text" id="userName" placeholder="Your Full Name" required>
            </div>
            
            <div class="form-group">
                <label for="userEmail">Your Email</label>
                <input type="email" id="userEmail" placeholder="Your Email Address" required>
            </div>
            
            <div class="form-group">
                <label for="userPhone">Your Phone</label>
                <input type="tel" id="userPhone" placeholder="Your Phone Number">
            </div>
            
            <div class="form-section">
                <h3>Your Expected Earnings</h3>
                
                <div class="form-group">
                    <label for="earningsDaily">Daily Earnings ($)</label>
                    <input type="number" id="earningsDaily" placeholder="e.g., 100.00" step="0.01" min="0" required>
                </div>
                
                <div class="form-group">
                    <label for="earningsWeekly">Weekly Earnings ($)</label>
                    <input type="number" id="earningsWeekly" placeholder="e.g., 700.00" step="0.01" min="0">
                </div>
                
                <div class="form-group">
                    <label for="earningsMonthly">Monthly Earnings ($)</label>
                    <input type="number" id="earningsMonthly" placeholder="e.g., 3000.00" step="0.01" min="0">
                </div>
                
                <div class="form-group">
                    <label for="earningsYearly">Yearly Earnings ($)</label>
                    <input type="number" id="earningsYearly" placeholder="e.g., 36000.00" step="0.01" min="0">
                </div>
                
                <p class="form-help">Only Daily Earnings is required. Other values will be calculated automatically if left empty.</p>
            </div>
            
            <div class="form-group">
                <label for="referrerName">Referred By</label>
                <input type="text" id="referrerName" placeholder="Who referred you?" value="{referral_data['name']}" required>
            </div>
            
            <button type="submit" class="submit-button">Create My Referral Page</button>
        </form>
        <div id="formSuccess" class="success-message" style="display: none;">
            <h3>Thank you for joining!</h3>
            <p>Your personalized referral page has been created.</p>
            <p id="newPageUrl"></p>
            <p>We've sent the details to your email address.</p>
        </div>
    </section>

    <footer class="footer">
        <p>© 2025 CryptoSuccess. All rights reserved.</p>
        <p>This is a referral page by {referral_data['name']}</p>
        <div class="footer-links">
            <a href="#">Privacy Policy</a>
            <a href="#">Terms of Service</a>
            <a href="#">Contact Us</a>
        </div>
    </footer>

    <script src="/static/form-handler.js"></script>
</body>
</html>
"""
    
    with open(os.path.join(page_dir, "index.html"), 'w') as f:
        f.write(html_content)
    
    # Save submission data for reference
    submission_path = os.path.join(SUBMISSIONS_DIR, f"{referral_id}.json")
    with open(submission_path, 'w') as f:
        json.dump({
            "referral_data": referral_data,
            "timestamp": timestamp,
            "page_dir": page_dir,
            "referral_id": referral_id
        }, f, indent=2)
    
    # Generate URL for the page
    page_url = f"/referral/{referral_id}"
    
    print(f"Personalized landing page created at: {page_dir}")
    return {
        "success": True,
        "page_dir": page_dir,
        "page_url": page_url,
        "referral_id": referral_id
    }

@app.route('/')
def index():
    """Serve the main landing page."""
    return send_from_directory(STATIC_DIR, 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files."""
    return send_from_directory(STATIC_DIR, path)

@app.route('/referral/<referral_id>')
def serve_referral_page(referral_id):
    """Serve a specific referral page."""
    page_dir = os.path.join(OUTPUT_BASE_DIR, referral_id)
    if os.path.exists(page_dir):
        return send_from_directory(page_dir, 'index.html')
    return "Referral page not found", 404

@app.route('/referral/<referral_id>/<path:path>')
def serve_referral_assets(referral_id, path):
    """Serve assets for a specific referral page."""
    page_dir = os.path.join(OUTPUT_BASE_DIR, referral_id)
    if os.path.exists(os.path.join(page_dir, path)):
        return send_from_directory(page_dir, path)
    return "Asset not found", 404

@app.route('/api/submit-referral', methods=['POST'])
def submit_referral():
    """API endpoint to receive referral form submissions."""
    try:
        data = request.json
        
        # Basic validation
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        # Process the submission
        result = create_referral_page(data)
        
        if result["success"]:
            return jsonify({
                "success": True,
                "message": "Referral page created successfully",
                "referral_id": result["referral_id"],
                "page_url": result["page_url"]
            })
        else:
            return jsonify({
                "success": False,
                "errors": result.get("errors", ["Unknown error occurred"])
            }), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/referrals', methods=['GET'])
def list_referrals():
    """API endpoint to list all referrals."""
    referrals = []
    
    for filename in os.listdir(SUBMISSIONS_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(SUBMISSIONS_DIR, filename)
            with open(file_path, 'r') as f:
                submission = json.load(f)
                referral_id = os.path.splitext(filename)[0]
                
                referrals.append({
                    "id": referral_id,
                    "name": submission["referral_data"]["name"],
                    "email": submission["referral_data"]["email"],
                    "timestamp": submission["timestamp"],
                    "page_url": f"/referral/{referral_id}"
                })
    
    return jsonify({"success": True, "referrals": referrals})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
