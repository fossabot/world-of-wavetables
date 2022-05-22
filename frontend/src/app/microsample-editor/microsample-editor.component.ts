import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'wowt-microsample-editor',
  templateUrl: './microsample-editor.component.html',
  styleUrls: ['./microsample-editor.component.scss']
})
export class MicrosampleEditorComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

  printFiles(ev: unknown) {
    console.log(ev)
  }

}
