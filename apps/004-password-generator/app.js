const ALPHA = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
const SPECIAL = '!@#$%^&*()_+-=[]{}|;:,.<>?';
const ALL = ALPHA + SPECIAL;

function generatePassword(length, useSpecial) {
  const charset = useSpecial ? ALL : ALPHA;
  const array = new Uint32Array(length);
  crypto.getRandomValues(array);
  let password = '';
  for (let i = 0; i < length; i++) {
    password += charset[array[i] % charset.length];
  }
  return password;
}

function checkStrength(password) {
  const checks = [
    { label: 'At least 8 characters', pass: password.length >= 8 },
    { label: 'At least 12 characters', pass: password.length >= 12 },
    { label: 'Contains lowercase letter', pass: /[a-z]/.test(password) },
    { label: 'Contains uppercase letter', pass: /[A-Z]/.test(password) },
    { label: 'Contains a number', pass: /[0-9]/.test(password) },
    { label: 'Contains a special character', pass: /[^a-zA-Z0-9]/.test(password) },
    { label: 'No repeated characters (3+)', pass: !/(.)\1{2,}/.test(password) },
  ];

  const score = checks.reduce((s, c) => s + (c.pass ? 1 : 0), 0);

  let level, barClass, barWidth;
  if (score <= 2) {
    level = 'Weak';
    barClass = 'weak';
    barWidth = 25;
  } else if (score <= 4) {
    level = 'Fair';
    barClass = 'fair';
    barWidth = 50;
  } else if (score <= 5) {
    level = 'Good';
    barClass = 'good';
    barWidth = 75;
  } else {
    level = 'Strong';
    barClass = 'strong';
    barWidth = 100;
  }

  return { checks, level, barClass, barWidth };
}

document.getElementById('generateBtn').addEventListener('click', () => {
  const lengthInput = document.getElementById('length');
  let length = parseInt(lengthInput.value, 10);
  if (isNaN(length) || length < 4) length = 4;
  if (length > 128) length = 128;
  lengthInput.value = length;

  const useSpecial = document.querySelector('input[name="charset"]:checked').value === 'special';
  const password = generatePassword(length, useSpecial);

  document.getElementById('generatedPassword').textContent = password;
  document.getElementById('result').classList.remove('hidden');
});

document.getElementById('copyBtn').addEventListener('click', () => {
  const pw = document.getElementById('generatedPassword').textContent;
  navigator.clipboard.writeText(pw).then(() => {
    const btn = document.getElementById('copyBtn');
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy', 1500);
  });
});

document.getElementById('toggleVisibility').addEventListener('click', () => {
  const input = document.getElementById('checkPassword');
  const btn = document.getElementById('toggleVisibility');
  if (input.type === 'password') {
    input.type = 'text';
    btn.textContent = 'Hide';
  } else {
    input.type = 'password';
    btn.textContent = 'Show';
  }
});

document.getElementById('checkPassword').addEventListener('input', (e) => {
  const pw = e.target.value;
  const resultEl = document.getElementById('strengthResult');

  if (!pw) {
    resultEl.classList.add('hidden');
    return;
  }

  resultEl.classList.remove('hidden');
  const { checks, level, barClass, barWidth } = checkStrength(pw);

  const bar = document.getElementById('strengthBar');
  bar.style.width = barWidth + '%';
  bar.className = 'strength-bar bar-' + barClass;

  const label = document.getElementById('strengthLabel');
  label.textContent = level;
  label.className = 'strength-label strength-' + barClass;

  const details = document.getElementById('strengthDetails');
  details.innerHTML = checks
    .map(c => `<li class="${c.pass ? 'pass' : 'fail'}">${c.label}</li>`)
    .join('');
});