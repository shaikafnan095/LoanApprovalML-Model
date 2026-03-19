const form = document.getElementById('loanForm');
const submitBtn = document.getElementById('submitBtn');
const resultCard = document.getElementById('resultCard');
const resultIcon = document.getElementById('resultIcon');
const resultStatus = document.getElementById('resultStatus');
const resultMessage = document.getElementById('resultMessage');
const resetBtn = document.getElementById('resetBtn');
const errorCard = document.getElementById('errorCard');
const errorText = document.getElementById('errorText');

const API_URL = 'http://127.0.0.1:8000/get_loan_status';

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  hideError();

  // Get form values
  const params = {
    education: parseInt(document.getElementById('education').value),
    cibil_score: parseInt(document.getElementById('cibil_score').value),
    income_annum: parseInt(document.getElementById('income_annum').value),
    loan_amount: parseInt(document.getElementById('loan_amount').value),
    no_of_dependents: parseInt(document.getElementById('no_of_dependents').value),
    residential_assets_value: parseInt(document.getElementById('residential_assets_value').value),
    commercial_assets_value: parseInt(document.getElementById('commercial_assets_value').value),
    luxury_assets_value: parseInt(document.getElementById('luxury_assets_value').value),
    bank_asset_value: parseInt(document.getElementById('bank_asset_value').value),
  };

  // Validate
  for (const [key, val] of Object.entries(params)) {
    if (isNaN(val)) {
      showError(`Please fill in all fields correctly.`);
      return;
    }
  }

  setLoading(true);

  try {
    const urlParams = new URLSearchParams(params);
    const response = await fetch(`${API_URL}?${urlParams}`);

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || `Server error: ${response.status}`);
    }

    const data = await response.json();
    const status = data['Predicted Loan Status'];

    showResult(status);

  } catch (err) {
    if (err.message.includes('Failed to fetch')) {
      showError('Cannot connect to server. Make sure your FastAPI server is running on http://127.0.0.1:8000');
    } else {
      showError(err.message);
    }
  } finally {
    setLoading(false);
  }
});

resetBtn.addEventListener('click', () => {
  resultCard.classList.remove('show', 'approved', 'rejected');
  form.style.display = 'block';
  form.reset();
  hideError();
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

function showResult(status) {
  const isApproved = status === 'Approved';

  form.style.display = 'none';
  resultCard.classList.add('show', isApproved ? 'approved' : 'rejected');
  resultCard.classList.remove(isApproved ? 'rejected' : 'approved');

  resultIcon.textContent = isApproved ? '✅' : '❌';
  resultStatus.textContent = isApproved ? 'Loan Approved!' : 'Loan Rejected';
  resultMessage.textContent = isApproved
    ? 'Congratulations! Based on your profile, your loan application is likely to be approved.'
    : 'Unfortunately, based on your profile, your loan application is not likely to be approved at this time.';

  resultCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function setLoading(state) {
  submitBtn.disabled = state;
  if (state) {
    submitBtn.classList.add('loading');
    submitBtn.querySelector('.btn-text').textContent = 'Analyzing';
    submitBtn.querySelector('.btn-icon').textContent = '';
  } else {
    submitBtn.classList.remove('loading');
    submitBtn.querySelector('.btn-text').textContent = 'Check Eligibility';
    submitBtn.querySelector('.btn-icon').textContent = '→';
  }
}

function showError(msg) {
  errorText.textContent = msg;
  errorCard.classList.add('show');
}

function hideError() {
  errorCard.classList.remove('show');
}