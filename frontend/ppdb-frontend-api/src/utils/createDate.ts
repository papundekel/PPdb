export function createDate(date_string: string): Date {
    const date = new Date(date_string)

    if (isNaN(+date)) {
        throw Error("invalid date")
    }

    return date
}
