import { endStream } from './../streams/stream-unsubscriber';
import { Injectable } from '@angular/core';
import { filter, from, map, Observable, pipe, switchMap } from 'rxjs';
import { isNullOrUndefined } from '../type-utils/is-empty';

@Injectable({
  providedIn: 'root'
})
export class WebAudioService {

  readonly sampleRate = 44100;

  audioContext: AudioContext | undefined;

  constructor() { }

  initAudioContext(contextOptions: AudioContextOptions = {
    sampleRate: this.sampleRate
  }) {
    try {
      if (isNullOrUndefined(this.audioContext)) {
        this.audioContext = new (window.AudioContext || (window as unknown as { webkitAudioContext: unknown }).webkitAudioContext)(contextOptions);
      } else {
        console.warn("AudioContext has been initialized before.")
      }
    } catch (error) {
      window.alert(
        `Sorry, but your browser doesn't support the Web Audio API!`
      );
    }
  }

  calculateAverage(samples: Float32Array) {
    return ([...samples].map((s) => Math.abs(s)).reduce((a, b) => a + b) * 2 / samples.length)
  }

  decodeSample$(file: File) {
    return from(file.arrayBuffer())
    .pipe(
      this.filterIfNoAudioContext(),
      switchMap((buffer: ArrayBuffer) => from(this.audioContext!.decodeAudioData(buffer))),
      endStream()
    ) as Observable<AudioBuffer>
  }

  filterIfNoAudioContext<T>() {
    return pipe(filter<T>(() => {
      const result = !isNullOrUndefined(this.audioContext)
      if (!result) { console.warn("AudioContext has not been initialized.") }
      return result;
    }))
  }
}
