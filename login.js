document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form from submitting

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Simple validation (you can enhance this with actual user verification)
    if (username === 'user' && password === 'password') {
        // Redirect to the homepage after successful login
        window.location.href = 'Home page.html';
    } else {
        alert('Incorrect username or password!');
    }
});
