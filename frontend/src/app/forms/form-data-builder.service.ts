import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class FormDataBuilderService {

  private instance: FormData | undefined = undefined;

  constructor() { }

  new() {
    this.instance = new FormData()

    return this
  }

  append(key: string, value: string | Blob, filename: string) {
    this.instance?.append(key, value, filename)

    return this
  }

  build() {
    const result = this.instance

    this.instance = undefined;

    return result;
  }
}
