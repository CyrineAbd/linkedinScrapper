import { Component, OnInit } from '@angular/core';
import { ProfileService } from '../../services/profile.service';
import { HttpClientModule } from '@angular/common/http'; // Import HttpClientModule

@Component({
  selector: 'app-profile-list',
  templateUrl: './profile-list.component.html',
  styleUrls: ['./profile-list.component.css'],
  standalone: true, // Ensure this is set if using standalone
  imports: [HttpClientModule] // Add HttpClientModule here
})
export class ProfileListComponent implements OnInit {
  profiles: any[] = [];

  constructor(private profileService: ProfileService) { }

  ngOnInit(): void {
    this.profileService.getProfiles().subscribe(
      (data: any[]) => {
        this.profiles = data;
      },
      (error: any) => {
        console.error('Error fetching profiles', error);
      }
    );
  }
}
