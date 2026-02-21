document.addEventListener('DOMContentLoaded', () => {
    const signUpBtn = document.getElementById('signUpBtn');
    const signInBtn = document.getElementById('signInBtn');
    const nameField = document.getElementById('nameInput'); // Keep this just in case, though we won't hide it
    const title = document.getElementById('title');
    

    // Ensure name field is visible initially (it should be by default from CSS/HTML)
    if (nameField) {
        nameField.style.maxHeight = '65px';
        nameField.style.opacity = '1';
    }

    
    signInBtn.onclick = function () {
        // User requested: "when i click once a time in sign in button then i goes to user_detail page"
        // Redirecting immediately on the first click
        window.location.href = 'user_detail.html';
    }

    signUpBtn.onclick = function () {
        if (signUpBtn.classList.contains('disable')) {
            // Switch to "Sign Up" mode
            title.innerHTML = 'Sign Up';
            signInBtn.classList.add('disable');
            signUpBtn.classList.remove('disable');
        } else {
            // If already active, maybe handle sign up logic or just redirect for demo
            window.location.href = 'user_detail.html';
        }
    }
});
