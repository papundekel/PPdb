export const columns = [
    { data: "firstName", title: "First Name" },
    { data: "lastName", title: "Last Name" },
    {
        data: "birthday",
        title: "Birthday",
        render: (birthday_data?: Date) =>
            birthday_data?.toLocaleDateString(),
        defaultContent: "-"
    },
];
