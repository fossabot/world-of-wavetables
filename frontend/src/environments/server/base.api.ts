import { environment } from "../environment";

export class BaseAPIService {

  static get root() {
    return environment.serviceURL
  }
}
