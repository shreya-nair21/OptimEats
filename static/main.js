// Money Donation Form

const moneyForm = document.getElementById('moneyDonationForm');
if (moneyForm) {
  moneyForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
      donor_name: document.getElementById('donorName').value,
      amount: document.getElementById('amount').value,
<<<<<<< HEAD:frontend/main.js
      business_id: 1
=======
      business_id: document.getElementById('business-dropdown').value
>>>>>>> 6dc93cedb7800b80c6ece16c67487b20e6efe742:static/main.js
    };

    try {
      const response = await fetch('/api/donations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      if (response.ok) {
        alert('Donation submitted successfully!');
        moneyForm.reset();
      } else {
        alert('Error: ' + (result.error || 'Unknown error'));
      }
      console.log(result);
    } catch (error) {
      alert('Error submitting donation.');
      console.error(error);
    }
  });
}

// Food Donation Form (similar)
const foodForm = document.getElementById('foodDonationForm');
if (foodForm) {
  foodForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
      donor_name: document.getElementById('donorName').value,
      food_type: document.getElementById('foodType').value,
      quantity: document.getElementById('quantity').value
    };


    alert('Food donation feature coming soon!');
  });
}
// Business Registration Form
const businessForm = document.getElementById('businessForm');
if (businessForm) {
  businessForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
      name: document.getElementById('businessName').value,
      contact: document.getElementById('contact').value,
      email: document.getElementById('email').value,
      password: document.getElementById('password').value,
      address: document.getElementById('address').value
    };

<<<<<<< HEAD:frontend/main.js
    try {
      const response = await fetch('/api/businesses', {
=======
try {
      const response = await fetch('http://localhost:5000/businesses/register', {
>>>>>>> 6dc93cedb7800b80c6ece16c67487b20e6efe742:static/main.js
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

<<<<<<< HEAD:frontend/main.js
      const result = await response.json();
      if (response.ok) {
        alert('Business registered successfully!');
        businessForm.reset();
      } else {
        alert('Error: ' + (result.error || 'Unknown error'));
      }
      console.log(result);
=======
      if (response.ok) { // Check if the response status is 200-299 (success)
        alert('Business registered successfully!');
        window.location.href = '/'; 
        
      } else {
        const errorData = await response.json();
        alert(`Registration failed: ${errorData.error || response.statusText}`);
      }
      
>>>>>>> 6dc93cedb7800b80c6ece16c67487b20e6efe742:static/main.js
    } catch (error) {
      alert('Error submitting business registration.');
      console.error(error);
    }
  });
}
