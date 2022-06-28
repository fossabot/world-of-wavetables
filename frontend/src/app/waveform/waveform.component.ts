import { WebAudioService } from '../audio/web-audio.service';
import { AfterViewInit, Component, ElementRef, Input, OnChanges, OnInit, SimpleChanges, ViewChild } from '@angular/core';
import { isNullOrUndefined } from '../type-utils/is-empty';

@Component({
  selector: 'wowt-waveform',
  templateUrl: './waveform.component.html',
  styleUrls: ['./waveform.component.scss']
})
export class WaveformComponent implements OnInit, AfterViewInit, OnChanges {

  @Input() samplefile: File | undefined = undefined;
  @Input() width = 640;
  @Input() height = 240;
  @Input() fftSize = 2048;

  audioBuffer: AudioBuffer | undefined;

  @ViewChild('waveform', { static: false }) waveform: ElementRef<HTMLCanvasElement> | undefined;

  _context: CanvasRenderingContext2D | null | undefined;

  get context(): CanvasRenderingContext2D {
    return this._context!
  }

  constructor(
    private webAudio: WebAudioService
  ) { }


  ngOnChanges(changes: SimpleChanges): void {
    const samplefileChanges = changes['samplefile']
    console.log(samplefileChanges)
    if (samplefileChanges.previousValue !== samplefileChanges.currentValue || isNullOrUndefined(samplefileChanges.previousValue)) {
      this.loadWaveform()
    }
  }

  loadWaveform() {
    if (this.samplefile) {
      this.webAudio.decodeSample$(this.samplefile).subscribe((value) => {
        this.audioBuffer = value;

        this.drawAverageWaveform();
      })
    }
  }

  ngOnInit(): void {
    this.webAudio.initAudioContext()
  }

  ngAfterViewInit(): void {
    this._context = this.waveform?.nativeElement.getContext("2d")

    this.context.scale(this.deviceDPR(), this.deviceDPR())

    this.drawBoundaryRectangle()
    this.drawAtCenter();

    // this.translateYToCenter()
    // this.drawCenterLine()
    // this.drawSinusCurve()
  }

  drawAverageWaveform() {
    this.context.fillStyle = '#FFFFFF'
    this.context.rect(0, 0, this.width, this.height)

    const buffer = this.audioBuffer!.getChannelData(0)
    const sampleRate = (this.webAudio.sampleRate / 2)
    const sections = Math.trunc(buffer.length / sampleRate);

    console.log("Sections", sections)

    for (let i = 0; i < sections; i++) {
      const start = i * sampleRate
      const end = (i + 1) * sampleRate
      console.log(start, end)
      const subBuffer = buffer.slice(start, end);
      // console.log(subBuffer)
      const average = this.webAudio.calculateAverage(subBuffer)
      const x = Math.trunc(this.width / sections) * i;
      const y = average * this.height

      this.context.moveTo(x, 0)
      this.context.lineTo(x, y)
      this.context.lineTo(x, -y)
    }

    this.context.stroke()

    //samples is the array and nb_samples is the length of array
    // let sum = 0;
    // for(let i = 0 ; i < buffer.length ; i++){
    //     if(buffer[i] < 0)
    //         sum += -buffer[i];
    //     else
    //         sum += buffer[i];
    // }
    // const average_point = (sum * 2) / buffer.length; //average after multiplying by 2

    // console.log(average_point)

    // this.context.moveTo(0, 0)
    // this.context.lineTo(1, 1)
    // this.context.stroke()

    // this.context.stroke()
  }

  drawAtCenter() {
    this.context.translate(0, this.height / 2)
  }

  drawSinusCurve() {
    this.context.beginPath()
    // this.context.translate(0, this.height / 2)
    this.context.fillStyle = '#000000'
    this.context.strokeStyle = '#000000'

    // [0 ... width] draw [-1 to 1]

    for (let i = 0; i < 360; i++) {
      this.drawPoint(i,Math.sin(i * Math.PI / 180) * this.height / 2)
      this.drawPoint(i,Math.cos(i * Math.PI / 180) * this.height / 2)
    }

    this.context.closePath()
  }

  drawPoint(x: number, y: number) {
    this.context.rect(x, y, 1, 1)
    this.context.stroke()
  }

  drawBoundaryRectangle() {
    this.context.clearRect(0, 0, this.width, this.height)
    this.context.fillStyle = '#000000'
    this.context.strokeStyle = '#000000'
    this.context.lineWidth = 4
    this.context.rect(0, 0, this.width, this.height)
    this.context.stroke()
  }

  drawCenterLine() {
    this.context.beginPath()
    this.context.fillStyle = '#000000'
    this.context.strokeStyle = '#000000'
    this.context.moveTo(0, 0)
    this.context.lineWidth = 2;
    this.context.lineTo(this.width, 0)
    this.context.stroke()
    this.context.closePath()
  }

  deviceDPR() {
    return window.devicePixelRatio || 1;
  }

  errorNoCanvas() {
    if (!this.waveform) {
      console.error("Canvas could not be loaded.")
    }
  }
}
