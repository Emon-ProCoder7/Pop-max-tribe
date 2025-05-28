// Enhanced form submission handler for the crypto referral landing page
document.addEventListener('DOMContentLoaded', function() {
  // Get the signup form element
  const signupForm = document.getElementById('referralForm');
  const formSuccess = document.getElementById('formSuccess');
  const newPageUrl = document.getElementById('newPageUrl');
  
  // Auto-calculate earnings based on daily amount
  const dailyInput = document.getElementById('earningsDaily');
  const weeklyInput = document.getElementById('earningsWeekly');
  const monthlyInput = document.getElementById('earningsMonthly');
  const yearlyInput = document.getElementById('earningsYearly');
  
  // Calculate other earnings when daily amount changes
  if (dailyInput) {
    dailyInput.addEventListener('input', function() {
      const dailyValue = parseFloat(this.value) || 0;
      
      if (!weeklyInput.value || weeklyInput.dataset.autoCalculated) {
        weeklyInput.value = (dailyValue * 7).toFixed(2);
        weeklyInput.dataset.autoCalculated = 'true';
      }
      
      if (!monthlyInput.value || monthlyInput.dataset.autoCalculated) {
        monthlyInput.value = (dailyValue * 30).toFixed(2);
        monthlyInput.dataset.autoCalculated = 'true';
      }
      
      if (!yearlyInput.value || yearlyInput.dataset.autoCalculated) {
        yearlyInput.value = (dailyValue * 365).toFixed(2);
        yearlyInput.dataset.autoCalculated = 'true';
      }
    });
  }
  
  // Remove auto-calculated flag when user manually edits
  [weeklyInput, monthlyInput, yearlyInput].forEach(input => {
    if (input) {
      input.addEventListener('input', function() {
        this.dataset.autoCalculated = 'false';
      });
    }
  });
  
  if (signupForm) {
    signupForm.addEventListener('submit', function(event) {
      event.preventDefault();
      
      // Get form input values
      const userName = document.getElementById('userName').value.trim();
      const userEmail = document.getElementById('userEmail').value.trim();
      const userPhone = document.getElementById('userPhone').value.trim();
      const earningsDaily = parseFloat(document.getElementById('earningsDaily').value) || 0;
      const earningsWeekly = parseFloat(document.getElementById('earningsWeekly').value) || (earningsDaily * 7);
      const earningsMonthly = parseFloat(document.getElementById('earningsMonthly').value) || (earningsDaily * 30);
      const earningsYearly = parseFloat(document.getElementById('earningsYearly').value) || (earningsDaily * 365);
      const referrerName = document.getElementById('referrerName').value.trim();
      
      // Basic validation
      if (!userName) {
        alert('Please enter your name');
        document.getElementById('userName').focus();
        return;
      }
      
      if (!userEmail) {
        alert('Please enter your email');
        document.getElementById('userEmail').focus();
        return;
      }
      
      if (!earningsDaily || earningsDaily <= 0) {
        alert('Please enter a valid daily earnings amount');
        document.getElementById('earningsDaily').focus();
        return;
      }
      
      if (!referrerName) {
        alert('Please enter who referred you');
        document.getElementById('referrerName').focus();
        return;
      }
      
      // Prepare data for submission
      const referralData = {
        name: userName,
        email: userEmail,
        phone: userPhone,
        earnings: {
          daily: earningsDaily,
          weekly: earningsWeekly,
          monthly: earningsMonthly,
          yearly: earningsYearly
        },
        referrer: referrerName
      };
      
      // Show loading state
      const submitButton = signupForm.querySelector('button[type="submit"]');
      const originalButtonText = submitButton.textContent;
      submitButton.textContent = 'Processing...';
      submitButton.disabled = true;
      
      // Submit data to backend API
      fetch('/api/submit-referral', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(referralData)
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // Success - show confirmation and redirect if URL is provided
          signupForm.style.display = 'none';
          formSuccess.style.display = 'block';
          
          if (data.page_url) {
            const fullUrl = window.location.origin + data.page_url;
            newPageUrl.innerHTML = `You can access it at: <a href="${fullUrl}" target="_blank">${fullUrl}</a>`;
          }
        } else {
          // Error handling
          const errorMessage = data.errors ? data.errors.join(', ') : 'An error occurred. Please try again.';
          alert(`Submission failed: ${errorMessage}`);
          submitButton.textContent = originalButtonText;
          submitButton.disabled = false;
        }
      })
      .catch(error => {
        console.error('Error submitting form:', error);
        alert('An error occurred while submitting the form. Please try again.');
        submitButton.textContent = originalButtonText;
        submitButton.disabled = false;
      });
    });
  }
});
