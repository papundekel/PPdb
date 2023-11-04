import { Configuration, PersonsApi, UsersApi } from "@api/index.js";

const configuration = new Configuration({
    basePath: "",
    accessToken: () => `Bearer ${localStorage.getItem("token")}`,
});

export const persons_api = new PersonsApi(configuration);
export const users_api = new UsersApi(configuration);
