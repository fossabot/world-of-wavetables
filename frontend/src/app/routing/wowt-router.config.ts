import { WavetableEditComponent } from './../wavetable-edit/wavetable-edit.component';
import { Routes } from "@angular/router";
import { MicrosampleEditorComponent } from '../microsample-editor/microsample-editor.component';

export const WOWT_ROUTER_CONFIG: Routes = [
  {
    path: "wavetable",
    component: WavetableEditComponent,
  },
  {
    path: "microsample/edit",
    component: MicrosampleEditorComponent
  }
]
