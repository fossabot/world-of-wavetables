import { WebAudioService } from '../audio/web-audio.service';
import { AfterViewChecked, AfterViewInit, Component, ElementRef, Input, OnChanges, OnInit, SimpleChanges, ViewChild } from '@angular/core';

@Component({
  selector: 'wowt-waveform',
  templateUrl: './waveform.component.html',
  styleUrls: ['./waveform.component.scss']
})
export class WaveformComponent implements OnInit, AfterViewInit, OnChanges {

  @Input() file: File | undefined = undefined;
  @Input() width = 640;
  @Input() height = 240;

  @ViewChild('waveform', { static: false }) waveform: ElementRef<HTMLCanvasElement> | undefined;

  _context: CanvasRenderingContext2D | null | undefined;

  get context(): CanvasRenderingContext2D {
    return this._context!
  }

  constructor(
    private webAudioService: WebAudioService
  ) { }


  ngOnChanges(changes: SimpleChanges): void {
    this.loadWaveform()
  }

  loadWaveform() {
    if (this.file) {
      const analyser = this.webAudioService.audioContext?.createAnalyser()
      if (analyser) {
        analyser.fftSize = 2048
      }

      const reader = new FileReader()
      console.log(reader.readAsArrayBuffer(this.file))
    }
  }

  ngAfterViewInit(): void {

    this._context = this.waveform?.nativeElement.getContext("2d")

    this.context.scale(this.deviceDPR(), this.deviceDPR())

    this.drawBoundary()



    // this.translateYToCenter()
    // this.drawCenterLine()
    // this.drawSinusCurve()
  }

  translateYToCenter() {
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

  drawBoundary() {
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

  ngOnInit(): void {
    this.webAudioService.activateAudioContext()

    console.log(this.file)

  }

  errorNoCanvas() {
    if (!this.waveform) {
      console.error("Canvas could not be loaded.")
    }
  }
}
