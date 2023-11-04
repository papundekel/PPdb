import { users_api } from "@this/api.js";

function handler(event: Event) {
    event.preventDefault();

    users_api
        .logoutApiUsersLoginDelete()
        .then(() => localStorage.removeItem("token"));
}

document.getElementById("form").addEventListener("submit", handler);
