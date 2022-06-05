import { pipe, take } from "rxjs"

export const endStream = () => pipe(take(1))
