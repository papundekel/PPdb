import { users_api } from "@this/api.js";

users_api.currentApiUsersCurrentGet().then(
    (user) => {
        document.getElementById(
            "logged-in"
        ).textContent = `Logged in as ${user.email}`;
    },
    () => {
        window.location.replace("/users/login");
    }
);
