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

       // <div class="button change-password"><a onclick="changePassword()">Change Password</a></div>
if (document.getElementById('first_name')) {
    button = document.createElement("button")
    button.innerHTML="Achievements"
    button.setAttribute("onclick", "achievements()")
    button.setAttribute("class", "button achievements")
    document.querySelector(".button-container").appendChild(button)
    button = document.createElement("button")
    button.innerHTML="Delete account"
    button.setAttribute("onclick", "deleteAccount()")
    button.setAttribute("class", "button delete-account")
    document.querySelector(".button-container").appendChild(button)
}

function achievements() {
    window.location.href = "/achievements?user=" + data["username"];
}

function deleteAccount() {
    document.querySelector(".search-bar-container").innerHTML = "";
    document.querySelector(".main").innerHTML = `<div class="delete-account-container">
            <a href="/profile"  class="close">X</a>
            <h3 id="warning">Warning: Accounts cannot be restored!</h3></br>
            <p id="reenter-password">Enter your password again to confirm you wish to delete your account</p>
            <input type="password" class="input-bar confirm-password" placeholder="Enter your password">
    </div>`
    document.querySelector(".confirm-password").onkeydown = deleteUser;
}

function changePassword() {
    document.querySelector(".search-bar-container").innerHTML = "";
    document.querySelector(".main").innerHTML = `<div class="change-password-container">
            <a href="/profile"  class="close">X</a>
            <h3 id="warning">Change Password</h3></br>
            <p>Please enter your old password</p>
            <input type="password" class="input-bar confirm-password old-password" placeholder="Enter your password">
            <p>Please enter your new password</p>
            <input type="password" class="input-bar confirm-password new-password" placeholder="Enter your password">
            <div class="button change-password"><a onclick="changePwd()">Confirm</a></div>
    </div>`
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
        d = deleteSelfAccount(password);
    }
}

function changePwd() {
    var old_password = document.querySelector(".old-password").value;
    var new_password = document.querySelector(".new-password").value;
    //d = deleteSelfAccount(password);
    console.log(old_password);
    console.log(new_password);
}
