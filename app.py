from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import shutil
import hashlib
import time

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)  # Enable CORS for all routes

# Directories for storing data
SUBMISSIONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'submissions')
GENERATED_PAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generated_pages')

# Ensure directories exist
os.makedirs(SUBMISSIONS_DIR, exist_ok=True)
os.makedirs(GENERATED_PAGES_DIR, exist_ok=True)

# Root route to serve the main landing page
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# API endpoint to process referral form submissions
@app.route('/api/submit-referral', methods=['POST'])
def submit_referral():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # Generate a unique ID for this referral
        timestamp = int(time.time())
        name_slug = data['name'].lower().replace(' ', '_')
        unique_hash = hashlib.md5(f"{name_slug}_{timestamp}".encode()).hexdigest()[:8]
        referral_id = f"{name_slug}_{unique_hash}"
        
        # Create a sanitized directory name
        dir_name = referral_id
        
        # Save submission data for reference
        submission_path = os.path.join(SUBMISSIONS_DIR, f"{dir_name}.json")
        with open(submission_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Create directory for the personalized page
        page_dir = os.path.join(GENERATED_PAGES_DIR, dir_name)
        os.makedirs(page_dir, exist_ok=True)
        
        # Generate the personalized HTML page
        html_content = generate_personalized_page(data)
        
        # Save the personalized page
        with open(os.path.join(page_dir, 'index.html'), 'w') as f:
            f.write(html_content)
        
        # Copy necessary static files (CSS, JS, etc.)
        copy_static_files(page_dir)
        
        # Return success with the referral URL
        referral_url = f"/referral/{dir_name}"
        return jsonify({
            'success': True, 
            'referral_id': referral_id,
            'referral_url': referral_url
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Serve generated referral pages
@app.route('/referral/<referral_id>')
def serve_referral_page(referral_id):
    page_path = os.path.join(GENERATED_PAGES_DIR, referral_id, 'index.html')
    if os.path.exists(page_path):
        return send_from_directory(os.path.join(GENERATED_PAGES_DIR, referral_id), 'index.html')
    else:
        return "Referral page not found", 404

# Helper function to generate personalized HTML content
def generate_personalized_page(data):
    name = data.get('name', 'User')
    email = data.get('email', '')
    phone = data.get('phone', '')
    daily_earnings = data.get('daily_earnings', 95.50)
    weekly_earnings = data.get('weekly_earnings', float(daily_earnings) * 7)
    monthly_earnings = data.get('monthly_earnings', float(daily_earnings) * 30)
    yearly_earnings = data.get('yearly_earnings', float(daily_earnings) * 365)
    referrer = data.get('referrer', 'a friend')
    
    # Format earnings with 2 decimal places
    daily_earnings_formatted = f"${float(daily_earnings):.2f}"
    weekly_earnings_formatted = f"${float(weekly_earnings):.2f}"
    monthly_earnings_formatted = f"${float(monthly_earnings):.2f}"
    yearly_earnings_formatted = f"${float(yearly_earnings):.2f}"
    
    # Generate HTML with personalized content
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Success - {name}'s Page</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <div class="logo">CryptoSuccess</div>
        <nav>
            <ul>
                <li><a href="#home">Home</a></li>
                <li><a href="#earnings">Earnings</a></li>
                <li><a href="#testimonial">Testimonial</a></li>
                <li><a href="#join">Join Now</a></li>
            </ul>
        </nav>
    </header>
    
    <section id="home" class="hero">
        <h1>Join {name}'s Crypto Success Story</h1>
        <p>Discover how you can earn passive income through our proven crypto business model</p>
        <a href="#join" class="cta-button">Get Started Now</a>
    </section>
    
    <section id="earnings" class="earnings">
        <h2>{name}'s Actual Earnings</h2>
        <div class="earnings-grid">
            <div class="earnings-card">
                <h3>Daily</h3>
                <p class="amount">{daily_earnings_formatted}</p>
            </div>
            <div class="earnings-card">
                <h3>Weekly</h3>
                <p class="amount">{weekly_earnings_formatted}</p>
            </div>
            <div class="earnings-card">
                <h3>Monthly</h3>
                <p class="amount">{monthly_earnings_formatted}</p>
            </div>
            <div class="earnings-card">
                <h3>Yearly</h3>
                <p class="amount">{yearly_earnings_formatted}</p>
            </div>
        </div>
    </section>
    
    <section id="testimonial" class="testimonial">
        <h2>Hear From {name} Directly</h2>
        <div class="video-placeholder">Video testimonial coming soon</div>
        <blockquote>
            "I never thought crypto could change my life until I discovered this business model. Now I'm earning passive income every day!"
        </blockquote>
        <p class="author">- {name}</p>
    </section>
    
    <section id="join" class="join-form">
        <h2>Ready to Start Your Crypto Journey?</h2>
        <p>Join through {name}'s referral and get exclusive bonuses!</p>
        
        <form id="referralForm">
            <div class="form-group">
                <label for="name">Your Name</label>
                <input type="text" id="name" name="name" placeholder="Your Full Name" required>
            </div>
            
            <div class="form-group">
                <label for="email">Your Email</label>
                <input type="email" id="email" name="email" placeholder="Your Email Address" required>
            </div>
            
            <div class="form-group">
                <label for="phone">Your Phone</label>
                <input type="tel" id="phone" name="phone" placeholder="Your Phone Number" required>
            </div>
            
            <div class="form-group">
                <label for="daily_earnings">Daily Earnings ($)</label>
                <input type="number" id="daily_earnings" name="daily_earnings" placeholder="e.g., 100.00" step="0.01">
            </div>
            
            <div class="form-group">
                <label for="weekly_earnings">Weekly Earnings ($)</label>
                <input type="number" id="weekly_earnings" name="weekly_earnings" placeholder="e.g., 700.00" step="0.01">
            </div>
            
            <div class="form-group">
                <label for="monthly_earnings">Monthly Earnings ($)</label>
                <input type="number" id="monthly_earnings" name="monthly_earnings" placeholder="e.g., 3000.00" step="0.01">
            </div>
            
            <div class="form-group">
                <label for="yearly_earnings">Yearly Earnings ($)</label>
                <input type="number" id="yearly_earnings" name="yearly_earnings" placeholder="e.g., 36000.00" step="0.01">
            </div>
            
            <div class="form-group hidden">
                <input type="hidden" id="referrer" name="referrer" value="{name}">
            </div>
            
            <button type="submit" class="submit-button">Create My Personalized Page</button>
        </form>
        <div id="formResponse" class="form-response"></div>
    </section>
    
    <footer>
        <p>&copy; 2025 Crypto Success. Referred by {name}</p>
    </footer>
    
    <script src="form-handler.js"></script>
</body>
</html>
"""
    return html

# Helper function to copy static files to the generated page directory
def copy_static_files(page_dir):
    # Copy CSS
    static_css = os.path.join(app.static_folder, 'styles.css')
    if os.path.exists(static_css):
        shutil.copy2(static_css, page_dir)
    
    # Copy JS
    static_js = os.path.join(app.static_folder, 'form-handler.js')
    if os.path.exists(static_js):
        shutil.copy2(static_js, page_dir)
    
    # Copy any other static files as needed

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
