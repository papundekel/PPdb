import { Configuration, PersonsApi, UsersApi } from "@api/index.js";

const token = localStorage.getItem("token");

const configuration = new Configuration({
    basePath: "",
    accessToken: token ? `Bearer ${token}` : null,
});

export const persons_api = new PersonsApi(configuration);
export const users_api = new UsersApi(configuration);
