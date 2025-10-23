// Money Donation Form
const moneyForm = document.getElementById('moneyDonationForm');
if (moneyForm) {
  moneyForm.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent page reload

    const data = {
      donor_name: document.getElementById('donorName').value,
      amount: document.getElementById('amount').value
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
      const response = await fetch('http://localhost:5000/api/businesses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      alert('Business registered successfully!');
      businessForm.reset(); // clear form
      console.log(result);
    } catch (error) {
      alert('Error submitting business registration.');
      console.error(error);
    }
  });
}
