import { FormDataBuilderService } from '../../forms/form-data-builder.service';
import { Component, OnInit } from '@angular/core';
import { SamplingApi } from 'src/environments/server/sampling.api';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'wowt-microsample-editor',
  templateUrl: './microsample-editor.component.html',
  styleUrls: ['./microsample-editor.component.scss']
})
export class MicrosampleEditorComponent implements OnInit {

  file: File | undefined

  constructor(
    private formDataBuilder: FormDataBuilderService,
    private http: HttpClient
  ) { }

  ngOnInit(): void {

  }

  processFirstFile(files: File[]) {
    const [file] = files
    if (file) {
      this.file = file;
      const formData = this.formDataBuilder.new().append('file', file, file.name).build()

      this.http.post(SamplingApi.waveform, formData).subscribe((v) => {
        console.log(v)
      })
    }
  }
}
