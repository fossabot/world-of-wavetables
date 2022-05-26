import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class WebAudioService {

  audioContext: AudioContext | undefined;

  constructor() { }

  load(file: File) {
    if (!file) {
      this.errorNoFile()
    }


  }

  activateAudioContext() {
    try {
      this.audioContext = new (window.AudioContext || (window as unknown as { webkitAudioContext: unknown }).webkitAudioContext)();
    } catch (error) {
      window.alert(
        `Sorry, but your browser doesn't support the Web Audio API!`
      );
    }
  }

  errorNoFile() {
    console.error("Invalid file or missing.")
  }
}
