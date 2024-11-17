import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http'; // Make sure this is imported

import { AppComponent } from './app.component';
import { ProfileListComponent } from './components/profile-list/profile-list.component';
import { ProfileService } from './services/profile.service';

@NgModule({
  declarations: [
    AppComponent,
    ProfileListComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule // Ensure this is included here
  ],
  providers: [ProfileService],
  bootstrap: [AppComponent]
})
export class AppModule { }
