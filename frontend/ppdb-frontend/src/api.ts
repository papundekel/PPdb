import { Configuration, PersonsApi } from "@api/index.js";

const configuration = new Configuration({ "basePath": "" })
export const persons_api = new PersonsApi(configuration);
