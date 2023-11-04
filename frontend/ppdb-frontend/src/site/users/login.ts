import { users_api } from "@this/api.js";
import { get_form_data } from "@this/form.js";

users_api.currentApiUsersCurrentGet().then(
    () => {
        window.location.replace("/");
    },
    () => {
        function handler(event: Event) {
            event.preventDefault();

            const form = event.target as HTMLFormElement;

            const login_json = get_form_data(form);

            users_api
                .loginApiUsersLoginPost({
                    username: login_json["email"],
                    password: login_json["password"],
                })
                .then((token) => {
                    localStorage.setItem("token", token.accessToken);
                    form.reset();
                });
        }

        document.getElementById("form").addEventListener("submit", handler);
    }
);
