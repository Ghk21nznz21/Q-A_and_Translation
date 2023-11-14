import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { OnInit } from '@angular/core';
import { initFlowbite } from 'flowbite';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent implements OnInit {
  title = 'QA';
  conversation : string[] = [];
  allowQuestion = true; 
  fileName: string = "all"; 
  fileContent: any = '';
  language: string = 'en'
  task: string = 'QA'

  // Database Files 
  allFiles: string[] = ["All"];
  languages = ['en', 'fr', 'pt', 'es'];
  tasks = ['QA', 'Translation'];

  // toast
  message = ''
  
  httpHeader = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json' 
    })
  };

  constructor(private http: HttpClient) {
    console.log('Start')
  }

    ngOnInit(): void {
    initFlowbite();
    // reset message
    setInterval(() => {this.message = '';}, 5000);
  }

  onFileSelected(fileList: FileList) {
    this.message = ''
    let file = fileList[0];
    let fileReader: FileReader = new FileReader();
    let text: any = '';
    let self = this;
    fileReader.onloadend = function (x) {
      // async
      text = fileReader.result;
      self.uploadFile(file.name, file.type, text);
    };
    fileReader.readAsText(file);
  }


  onLanguageChange(language: string) {
    console.log('language', language)
    if (language != this.language){
      // restore conversation on change 
      this.conversation = []
      this.language = language;
    }
  }
  onFileChange(fileName: string) {
    if (fileName != this.fileName){
      // restore conversation on change 
      this.conversation = []
      this.fileName = fileName;
    }
  }

  onTaskChange(task: string) {
    if (task != this.task){
      // restore conversation on change 
      this.conversation = []
      this.task = task;
      console.log('Task', this.task)
    }
  }

  uploadFile(name: string, type:string, text: string) {
    this.http.post('http://localhost:5000/upload', {'name': name, 'type': type, 'text': text}, this.httpHeader).subscribe({
      next: (data: any) => {
        console.log('data',data)
        this.message = data.message
        if (this.message == "Document Added") {this.allFiles.push(name)}
      },
      error: (error) => {
        console.log('Error upload', error),
        this.message = 'Error'
      }
    })
  }

  sendQuestion(text: string) {
    if (this.allowQuestion) {
      this.conversation.push(text);
      this.allowQuestion = false 
      console.log('Sending', {'text': text, "fileName": this.fileName, "language": this.language, "task": this.task})
      this.http.post('http://localhost:5000/query', 
          {'text': text, "fileName": this.fileName, "language": this.language, "task": this.task}, 
          this.httpHeader).subscribe({
        next: (data: any) => {
          this.conversation.push(data.message) 
          this.allowQuestion = true;
          console.log('Received', data.message)
          this.message = data.message
        },
        error: (error) => {
          const message_error = 'Message Error';
          this.conversation.push(message_error);
          this.allowQuestion = true;
          console.log('Error', error)
          this.message = 'Error'
        }
      })
    }
  }

}
