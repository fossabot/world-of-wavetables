import { isNullOrUndefined } from 'src/app/type-utils/is-empty';
import { Injectable } from '@angular/core';

declare var WaveSurfer: any;

@Injectable({
  providedIn: 'root'
})
export class WavesurferService {

  private _wavesurfer: any;

  activate() {
    this._wavesurfer = WaveSurfer.create({
      container: '#waveform'
    })
  }

  load(blob: Blob | File) {
    if (isNullOrUndefined(this._wavesurfer)) { console.error("Missing wavesurfer instance."); return; }

    this._wavesurfer.loadBlob(blob)
  }

  constructor() { }
}
