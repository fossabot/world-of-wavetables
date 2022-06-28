import { WavesurferService } from './wavesurfer.service';
import { Component, Input, OnInit, SimpleChanges } from '@angular/core';
import { WebAudioService } from 'src/app/audio/web-audio.service';
import { isNullOrUndefined } from 'src/app/type-utils/is-empty';

@Component({
  selector: 'wowt-wavesurfer',
  templateUrl: './wavesurfer.component.html',
  styleUrls: ['./wavesurfer.component.scss']
})
export class WavesurferComponent implements OnInit {

  @Input() samplefile: File | undefined = undefined;
  @Input() width = 640;
  @Input() height = 240;
  @Input() fftSize = 2048;

  audioBuffer: AudioBuffer | undefined;

  constructor(
    private webAudio: WebAudioService,
    private wavesurfer: WavesurferService
  ) { }

  ngOnInit(): void {
    this.wavesurfer.activate()
  }

  ngOnChanges(changes: SimpleChanges): void {
    const samplefileChanges = changes['samplefile']
    console.log(samplefileChanges)
    if (samplefileChanges.previousValue !== samplefileChanges.currentValue || isNullOrUndefined(samplefileChanges.previousValue)) {
      if (this.samplefile) {
        this.loadWaveform(samplefileChanges.currentValue)
      }
    }
  }

  loadWaveform(blob: File | Blob) {
    this.wavesurfer.load(blob)
  }
}
