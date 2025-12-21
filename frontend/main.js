// Money Donation Form
const moneyForm = document.getElementById('moneyDonationForm');
if (moneyForm) {
  moneyForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
      donor_name: document.getElementById('donorName').value,
      amount: document.getElementById('amount').value,
      business_id: 1
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

    try {
      const response = await fetch('/api/businesses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      if (response.ok) {
        alert('Business registered successfully!');
        businessForm.reset();
      } else {
        alert('Error: ' + (result.error || 'Unknown error'));
      }
      console.log(result);
    } catch (error) {
      alert('Error submitting business registration.');
      console.error(error);
    }
  });
}
