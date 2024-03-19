var name, value
for ([name, value] of Object.entries(data)) {
    if (name == 'first_name') {
        document.querySelector(".private-info").innerHTML = `<div class="profile-info">
            <label>First Name:</label>
            <p id="first_name">{{ user.first_name }}</p>
        </div>
        <div class="profile-info">
            <label>Last Name:</label>
            <p id="last_name">{{ user.last_name }}</p>
        </div>
        <div class="profile-info">
            <label>User Type:</label>
            <p id="user_type">{{ user.userType }}</p>
        </div>`
    }
    document.getElementById(`${name}`).innerHTML = value;
}

if (document.getElementById('first_name')) {
    document.querySelector(".button-container").innerHTML += `
        <div class="button achievements"><a onclick="achievements()">Achievements</a></div>
        <div class="button delete-account"><a onclick="deleteAccount()">Delete Account</a></div>`
}

function achievements() {
    window.location.href = "/achievements?user=" + data["username"];
}

function deleteAccount() {
    document.querySelector(".main").innerHTML = `<div class="delete-account-container">
            <a href="/profile"  class="close">X</a>
            <h3 id="warning">Warning: Accounts cannot be restored!</h3></br>
            <p id="reenter-password">Enter your password again to confirm you wish to delete your account</p>
            <input type="text" class="input-bar confirm-password" placeholder="Enter your password">
    </div>`
    document.querySelector(".confirm-password").onkeydown = deleteUser;
}

document.querySelector(".search-bar").onkeydown = function searchUser(e) {
    if (e.keyCode == 13) {
        var user = document.querySelector(".search-bar").value;
        window.location.href = "/profile?user=" + user;
    }
}

function deleteUser(e) {
    if (e.keyCode == 13) {
        var password = document.querySelector(".confirm-password").value;
        console.log(password);
        if (checkPassword(password)) {
            // send request to delete account and log out of the account
            console.log("Correct");
        } else {
            //window.location.href = "/profile";
            console.log("Incorrect");
        }
        console.log(checkPassword(password));
    }
}