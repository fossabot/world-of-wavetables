import { BaseAPIService } from './base.api';

export class SamplingApi {

  static get root() {
    return BaseAPIService.root + 'sampling/'
  }

  static get waveform() {

    return this.root + 'waveform'
  }
}
