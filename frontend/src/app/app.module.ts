import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { WOWT_ROUTER_CONFIG } from './routing/wowt-router.config';
import { WavetableEditComponent } from './wavetable-edit/wavetable-edit.component';
import { MicrosampleEditorComponent } from './microsampler/microsample-editor/microsample-editor.component';
import { FileUploadComponent } from './file-upload/file-upload.component';
import { WaveformComponent } from './waveform/waveform.component';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [
    AppComponent,
    WavetableEditComponent,
    MicrosampleEditorComponent,
    FileUploadComponent,
    WaveformComponent,
   ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    RouterModule.forRoot(WOWT_ROUTER_CONFIG)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
