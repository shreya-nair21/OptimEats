// Helper for Notifications (replaces native alert)
function showNotification(message, type = 'success') {
  // Check if container exists, if not create it
  let container = document.getElementById('notification-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'notification-container';
    container.style.position = 'fixed';
    container.style.top = '20px';
    container.style.right = '20px';
    container.style.zIndex = '1050';
    container.style.minWidth = '300px';
    document.body.appendChild(container);
  }

  // Create alert element
  const alertDiv = document.createElement('div');
  alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
  alertDiv.role = 'alert';
  alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

  container.appendChild(alertDiv);

  // Auto dismiss after 3 seconds
  setTimeout(() => {
    alertDiv.classList.remove('show');
    setTimeout(() => alertDiv.remove(), 150);
  }, 5000);
}

// User Registration Form (NEW)
const userRegForm = document.getElementById('userRegForm');
if (userRegForm) {
  userRegForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
      name: document.getElementById('userName').value,
      email: document.getElementById('userEmail').value,
      password: document.getElementById('userPassword').value,
      phone: document.getElementById('userPhone').value,
      dependents: parseInt(document.getElementById('userDependents').value) || 0
    };

    try {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      if (response.ok) {
        showNotification('User registered successfully! ID: ' + result.id, 'success');
        userRegForm.reset();
      } else {
        showNotification('Error: ' + (result.error || 'Unknown error'), 'danger');
      }
    } catch (error) {
      showNotification('Error registering user.', 'danger');
      console.error(error);
    }
  });
}

// Money Donation Form
const moneyForm = document.getElementById('moneyDonationForm');
if (moneyForm) {
  moneyForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
      donor_name: document.getElementById('donorName').value,
      amount: document.getElementById('amount').value,
      business_id: 1 // Default or selected
    };

    try {
      const response = await fetch('/api/donations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      if (response.ok) {
        showNotification('Donation submitted successfully!', 'success');
        moneyForm.reset();
      } else {
        showNotification('Error: ' + (result.error || 'Unknown error'), 'danger');
      }
    } catch (error) {
      showNotification('Error submitting donation.', 'danger');
      console.error(error);
    }
  });
}

// Food Donation Form
const foodForm = document.getElementById('foodDonationForm');
if (foodForm) {
  foodForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Map selection to dummy meal_id for demo purposes (or implement dynamic meal selection)
    // In a real app, you'd fetch business's menu to select what to donate.
    // Here we act as if we are "buying" a meal for someone else as a donation?
    // OR we just record it. Backend supports generic food donation if we send type='food'.

    // NOTE: The backend expects meal_id if type='food'. 
    // If this is a generic food drive, we might need a different backend handler.
    // For now, let's assume valid meal_id is needed or we send generic money equivalent? 
    // Let's stick to the backend logic: it expects meal_id. 
    // We will simulate donating "Meal ID 1" for now or use a valid one if known.

    // For simplicity in this demo, let's treat food donation as "donating money equivalent of food"
    // OR we assume there is a 'Generic Meal' with ID 1 in the system.

    const data = {
      donor_name: 'Anonymous Donor', // Can add field
      type: 'food',
      meal_id: 1, // specific meal ID
      quantity: document.getElementById('quantity').value,
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
        showNotification(result.message, 'success');
        foodForm.reset();
      } else {
        showNotification('Error: ' + (result.error || 'Unknown error'), 'danger');
      }
    } catch (error) {
      console.error(error);
      showNotification('Failed to submit food donation', 'danger');
    }
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
      address: document.getElementById('address').value,
      people_count: parseInt(document.getElementById('people').value) || 0,
      type: document.querySelector('input[name="type"]:checked')?.value || 'unknown'
    };

    try {
      const response = await fetch('/businesses/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      if (response.ok) {
        showNotification('Business registered successfully!', 'success');
        businessForm.reset();
      } else {
        showNotification('Error: ' + (result.error || 'Unknown error'), 'danger');
      }
    } catch (error) {
      showNotification('Error submitting business registration.', 'danger');
      console.error(error);
    }
  });
}

// --- NEW FEATURES ---

// Transparency Report
async function loadTransparencyReport() {
  try {
    const response = await fetch('/api/transparency');
    const data = await response.json();

    if (data.impact_summary) {
      document.getElementById('total-funds').innerText = '₹' + data.impact_summary.total_funds_raised;
      document.getElementById('meals-provided').innerText = data.impact_summary.meals_provided;
      document.getElementById('active-business').innerText = data.impact_summary.participating_businesses;
    }

    const tbody = document.getElementById('top-donors-list');
    if (tbody && data.top_donors) {
      tbody.innerHTML = data.top_donors.map((d, index) => `
                <tr>
                    <td>#${index + 1}</td>
                    <td>${d.name}</td>
                    <td class="text-end">₹${d.amount.toFixed(2)}</td>
                </tr>
            `).join('');
    }
  } catch (e) {
    console.error("Failed to load transparency report", e);
  }
}

// User Dashboard
async function loadUserDashboard() {
  const userId = document.getElementById('userIdInput').value;
  if (!userId) return alert("Please enter a User ID");

  try {
    const response = await fetch(`/api/users/${userId}/history`);
    if (!response.ok) throw new Error("User not found");

    const data = await response.json();

    document.getElementById('login-section').style.display = 'none';
    document.getElementById('dashboard-content').style.display = 'block';

    document.getElementById('user-name').innerText = data.user;
    document.getElementById('user-role').innerText = data.role.toUpperCase();

    // Donations
    const donationList = document.getElementById('donation-list');
    if (data.donations.length > 0) {
      donationList.innerHTML = data.donations.map(d => `
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <span>${d.type === 'food' ? '🍔 Food Donation' : '💰 Money Donation'}</span>
                    <span class="badge bg-primary rounded-pill">₹${d.amount}</span>
                </li>
            `).join('');
    }

    // Claims
    const mealList = document.getElementById('meal-list');
    if (data.claimed_meals.length > 0) {
      mealList.innerHTML = data.claimed_meals.map(m => `
                <li class="list-group-item">
                    Joined meal ID ${m.menu_id} <br>
                    <small class="text-muted">${new Date(m.timestamp).toLocaleDateString()}</small>
                </li>
            `).join('');
    }

  } catch (e) {
    alert(e.message);
  }
}
