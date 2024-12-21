document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form from submitting

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const data = {
        username: username,
        password: password
    };

    // Send login data via fetch
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)  // Send the data as JSON
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();  // Parse the JSON response
    })
    .then(data => {
        if (data.success) {
            window.location.href = '/home';  // Redirect on successful login
        } else {
            alert(data.error);  // Show error message if login failed
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error with the login process. Please try again.');
    });
});
