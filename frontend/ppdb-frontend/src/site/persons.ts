import { persons_api } from "@this/api.js";
import { columns } from "@this/persons/table.js";
import { table } from "@this/table.js";

table("#persons-table", persons_api.getAllApiPersonsGet(), columns);
