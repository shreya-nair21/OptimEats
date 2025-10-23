// Money Donation Form

const moneyForm = document.getElementById('moneyDonationForm');
if (moneyForm) {
  moneyForm.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent page reload

    const data = {
      donor_name: document.getElementById('donorName').value,
      amount: document.getElementById('amount').value,
      business_id: document.getElementById('business-dropdown').value
    };

    try {
      const response = await fetch('http://localhost:5000/api/donations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      alert('Donation submitted successfully!');
      moneyForm.reset(); // clear form
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

    try {
      const response = await fetch('http://localhost:5000/api/food-donations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      alert('Food donation submitted!');
      foodForm.reset();
      console.log(result);
    } catch (error) {
      alert('Error submitting food donation.');
      console.error(error);
    }
  });
}
// Business Registration Form
const businessForm = document.getElementById('businessForm');
if (businessForm) {
  businessForm.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent page reload

    const data = {
      name: document.getElementById('businessName').value,
      contact: document.getElementById('contact').value,
      address: document.getElementById('address').value
    };

try {
      const response = await fetch('http://localhost:5000/businesses/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      if (response.ok) { // Check if the response status is 200-299 (success)
        alert('Business registered successfully!');
        window.location.href = '/'; 
        
      } else {
        const errorData = await response.json();
        alert(`Registration failed: ${errorData.error || response.statusText}`);
      }
      
    } catch (error) {
      alert('Error submitting business registration.');
      console.error(error);
    }
  });
}
