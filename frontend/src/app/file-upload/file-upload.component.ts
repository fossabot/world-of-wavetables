import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { isObject } from '../type-utils/object-guard';

interface FileInputElement {
  files: Array<string | Blob>,
  value: string
}

@Component({
  selector: 'wowt-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.scss']
})
export class FileUploadComponent implements OnInit {

  @Input() filetypes: string[] | '*' = ['wav', 'png']

  selectedFiles: File[] | undefined = undefined;

  @Output() fileSelection = new EventEmitter<File[]>()

  readonly FORMDATA_FILE = "file"

  constructor() { }

  ngOnInit(): void {}

  isFileInputElement(value: unknown): value is FileInputElement {
    return isObject(value) && 'files' in value && 'value' in value
  }

  emitFileSelection(ev: Event) {
    if(!this.isFileInputElement(ev.target)) {
      this.errorInvalidElement()
      return
    }

    const fileInputElement = ev.target;

    if (!this.hasFilesSelected(fileInputElement)) {
      this.errorNoFiles()
      return
    }

    this.selectedFiles = this.queryFiles(fileInputElement)

    if (this.selectedFiles) {
      this.fileSelection.next(this.selectedFiles)
    }
  }

  hasFilesSelected(ev: FileInputElement) {
    return ev?.files?.length > 0
  }

  queryFiles(ev: FileInputElement): File[] | undefined {
    if (!this.hasFilesSelected(ev)) {
      this.errorNoFiles()
      return undefined
    }

    // TODO: Typecheck

    const files = this.convertFilelistToArray(ev.files as unknown as FileList)

    if (!this.hasCorrectFiletypes(files)) {
      this.errorInvalidFileType()
      return undefined
    }

    return files
  }

  hasCorrectFiletypes(files: File[]) {
    return files.every((file) => {
      const [_, extension] = file.name.split('.')

      return Array.isArray(this.filetypes) ? this.filetypes.some((filetype) => filetype === extension) : true
    })
  }

  convertFilelistToArray(filelist: FileList) {
    const result: File[] = []

    for (let index = 0; index < filelist.length; index++) {
      const file = filelist.item(index)
      if (!file) { continue; }

      result.push(file)
    }

    return result
  }

  errorNoFiles() {
    console.error("No files present.")
  }

  errorInvalidElement() {
    console.error("Given value is not of an FileInputElement")
  }

  errorInvalidFileType() {
    console.error("Filetypes are invalid, allowed", this.filetypes)
  }

  appendFilesToFormData(formData: FormData, files: File[]) {
    files.forEach((file) => {
      if (!file) { return; }
      formData.append(this.FORMDATA_FILE, file, file.name)
    })
  }

  createFormData() {
    const formData = new FormData()

    if (this.selectedFiles) {
      this.appendFilesToFormData(formData, this.selectedFiles)
    }

    return formData
  }
}
