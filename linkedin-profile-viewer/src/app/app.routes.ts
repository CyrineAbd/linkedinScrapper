import { Routes } from '@angular/router';
import { ProfileListComponent } from './components/profile-list/profile-list.component';

export const routes: Routes = [
  { path: 'profiles', component: ProfileListComponent },
  { path: '', redirectTo: '/profiles', pathMatch: 'full' } // Redirect to profiles on load
];
