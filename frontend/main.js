// Helper for Notifications (replaces native alert)
function showNotification(message, type = 'success') {
  let container = document.getElementById('notification-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'notification-container';
    container.style.position = 'fixed';
    container.style.top = '20px'; // Top right
    container.style.right = '20px';
    container.style.zIndex = '1050';
    container.style.minWidth = '300px';
    document.body.appendChild(container);
  }

  const alertDiv = document.createElement('div');
  alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
  alertDiv.role = 'alert';
  alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

  container.appendChild(alertDiv);

  setTimeout(() => {
    alertDiv.classList.remove('show');
    setTimeout(() => alertDiv.remove(), 150);
  }, 5000);
}

// User Registration Form
const userRegForm = document.getElementById('userRegForm');
if (userRegForm) {
  userRegForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
      name: document.getElementById('userName').value,
      email: document.getElementById('userEmail').value,
      password: document.getElementById('userPassword').value,
      phone: document.getElementById('userPhone').value,
      dependents: parseInt(document.getElementById('userDependents')?.value) || 0
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

    const businessDropdown = document.getElementById('business-dropdown');
    const selectedBusiness = businessDropdown ? businessDropdown.value : 1;

    const data = {
      donor_name: document.getElementById('donorName').value,
      amount: document.getElementById('amount').value,
      business_id: parseInt(selectedBusiness)
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

    const data = {
      donor_name: 'Anonymous Donor',
      type: 'food',
      meal_id: 1, // Default dummy meal ID
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
      password: document.getElementById('password').value,
      address: document.getElementById('address').value,
      people_count: parseInt(document.getElementById('people')?.value) || 0,
      type: document.querySelector('input[name="type"]:checked')?.value || 'unknown'
    };

    try {
      // Correct endpoint for registration is /businesses/register
      const response = await fetch('/businesses/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();

      if (response.ok) {
        showNotification('Business registered successfully!', 'success');
        businessForm.reset();
        // Redirect to login or home
        setTimeout(() => window.location.href = '/', 2000);
      } else {
        showNotification('Error: ' + (result.error || 'Unknown error'), 'danger');
      }
    } catch (error) {
      showNotification('Error submitting business registration.', 'danger');
      console.error(error);
    }
  });
}

// Organization Dashboard Logic
async function loadOrgDashboard(businessId) {
  try {
    console.log("Loading dashboard for business:", businessId);

    // 1. Get Business Details
    const busRes = await fetch(`/api/businesses/${businessId}`);
    const business = await busRes.json();

    if (busRes.ok) {
      document.getElementById('orgName').textContent = business.name || 'Organization Dashboard';
      document.getElementById('orgBalance').textContent = '₹' + (business.balance || 0).toFixed(2);

      // Populate Edit Profile Form
      if (document.getElementById('editContact')) document.getElementById('editContact').value = business.contact || '';
      if (document.getElementById('editAddress')) document.getElementById('editAddress').value = business.address || '';
      if (document.getElementById('editNeeds')) document.getElementById('editNeeds').value = business.needs || '';
    } else {
      console.error("Failed to load business details:", business);
    }

    // 2. Get Donations History
    const donRes = await fetch(`/api/donations/business/${businessId}`);
    const donData = await donRes.json();

    if (donRes.ok) {
      console.log("Donations loaded:", donData);
      document.getElementById('totalDonationsCount').textContent = donData.total_donations || 0;

      const tbody = document.getElementById('donationsBody');
      if (tbody) {
        if (donData.donations && donData.donations.length > 0) {
          tbody.innerHTML = donData.donations.map(d => `
                        <tr>
                            <td>${new Date(d.timestamp).toLocaleDateString()}</td>
                            <td>${d.donor_name}</td>
                            <td><span class="badge bg-${d.type === 'money' ? 'success' : 'info'}">${d.type}</span></td>
                            <td>${d.type === 'money' ? '₹' + d.amount : d.quantity + ' items'}</td>
                        </tr>
                    `).join('');
        } else {
          tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted">No donations received yet.</td></tr>';
        }
      }
    } else {
      console.error("Failed to load donations:", donData);
    }

  } catch (e) {
    console.error("Error in loadOrgDashboard:", e);
    showNotification("Failed to load dashboard data", 'danger');
  }
}

// Transparency Report
async function loadTransparencyReport() {
  try {
    const response = await fetch('/api/transparency');
    const data = await response.json();

    if (data.impact_summary) {
      if (document.getElementById('total-funds')) document.getElementById('total-funds').innerText = '₹' + data.impact_summary.total_funds_raised;
      if (document.getElementById('meals-provided')) document.getElementById('meals-provided').innerText = data.impact_summary.meals_provided;
      if (document.getElementById('active-business')) document.getElementById('active-business').innerText = data.impact_summary.participating_businesses;
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
