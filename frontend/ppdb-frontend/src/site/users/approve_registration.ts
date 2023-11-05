import { RegistrationApprovalFromJSON } from "@api/index.js";
import { users_api } from "@this/api.js";
import { get_form_data } from "@this/form.js";

function handler(event: Event) {
    event.preventDefault();
    event.stopPropagation();

    const form = event.target as HTMLFormElement;

    const form_data = get_form_data(form);

    users_api
        .createApiUsersRegistrationApprovalPost({
            registrationApproval: RegistrationApprovalFromJSON(form_data),
        })
        .then(() => form.reset());
}

document.getElementById("form").addEventListener("submit", handler);
