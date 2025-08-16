const loginPage = document.getElementById('loginPage');
const registerPage = document.getElementById('registerPage');
const dashboard = document.getElementById('dashboard');
const userInfo = document.getElementById('userInfo');

document.getElementById('showRegisterBtn').onclick = () => {
  loginPage.style.display = 'none';
  registerPage.style.display = 'block';
};

document.getElementById('showLoginBtn').onclick = () => {
  registerPage.style.display = 'none';
  loginPage.style.display = 'block';
};

document.getElementById('logoutBtn').onclick = () => {
  dashboard.style.display = 'none';
  loginPage.style.display = 'block';
};

document.getElementById('registerForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('registerUsername').value;
  const password = document.getElementById('registerPassword').value;

  const res = await fetch('/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();
  alert(data.message);

  if (res.status === 200) {
    registerPage.style.display = 'none';
    loginPage.style.display = 'block';
  }
});

document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('loginUsername').value;
  const password = document.getElementById('loginPassword').value;

  const res = await fetch('/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();
  if (res.status === 200) {
    loginPage.style.display = 'none';
    dashboard.style.display = 'block';
    userInfo.textContent = `Logged in as: ${username}`;
  } else {
    alert(data.message);
  }
});
