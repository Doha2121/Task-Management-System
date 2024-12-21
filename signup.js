document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form from submitting

    const name = document.getElementById('name').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const gender = document.getElementById('gender').value;

    // Simple validation (you can enhance this with actual backend integration)
    if (name && username && password && gender) {
        // Show success message
        alert('Signup successful! You can now login.');

        // Redirect to login page after success
        window.location.href = '/login'; // Redirects to Flask login route
    } else {
        alert('Please fill out all fields!');
    }
});
