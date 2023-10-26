import DataTable from "@modules/datatables.net-bs5/js/dataTables.bootstrap5.min.mjs";

export function table<T>(id: string, request: Promise<T[]>, columns: any) {
    request.then((data) => {
        new DataTable(id, { "data": data, "columns": columns });
    });
}
