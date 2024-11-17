import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'; // Ensure this is correct
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProfileService {

  private apiUrl = 'http://127.0.0.1:5000/api/profiles';

  constructor(private http: HttpClient) { }

  getProfiles(): Observable<any> {
    return this.http.get(this.apiUrl);
  }
}
