import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

import { AgmCoreModule } from '@agm/core';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/switchMap';

import { Meeting } from '../../../models/meeting';
import { MeetingService } from '../../../services/meeting.service';
import { MapService } from '../../../services/map.service';

/**
 * The page for displaying study group meetings.
 */
@Component({
  selector: 'app-meetings',
  templateUrl: './meetings.component.html',
  styleUrls: ['./meetings.component.css']
})
export class MeetingsComponent implements OnInit {

  /**
   * The group's unique ID.
   */
  groupID: number;

  /**
   * An array of meetings.
   */
  meetings = [];

  /**
   * Keys for displaying the meetings in the template.
   */
  keys = [];

  /**
   * A meeting object for creating a new note.
   */
  meeting = new Meeting();

  /**
   * A place to store the typing timer.
   */
  typingTimer: any;

  /**
   * The interval to count down from once the user stops typing.
   */
  doneTypingInterval: number = 1000;

  /**
   * Form error, if any.
   */
  meetingError: string = '';

  /**
   * Any error that the note service returns.
   */
  error: any;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private meetingService: MeetingService,
    private mapService: MapService,
  ) {}

  /**
   * Runs when the component initializes.
   */
  ngOnInit() {
    this.groupID = +this.route.snapshot.paramMap.get('id');
    this.getMeetings();
  }

  /**
   * Calls the meeting service to get all the meetings for this group.
   */
  getMeetings() {
    this.meetingService.getMeetings(this.groupID).subscribe(
      data => {
        this.meetings = { ...data };
        this.keys = Object.keys(this.meetings);
        for (let key of this.keys) {
          this.setMeetingLatLng(key);
        }
      },
      error => this.error = error,
    )
  }

  /**
   * Calls the meeting service to create a new meeting.
   */
  createMeeting() {
    this.meetingService.createMeeting(this.groupID, this.meeting).subscribe(
      () => {
        this.getMeetings();
        this.meeting = new Meeting();
      },
      error => this.meetingError = 'Please fill out all fields.'
    );
  }

  /**
   * Calls the service to delete a meeting.
   * @param {number} id - The meeting to delete.
   */
  deleteMeeting(meetingID: number) {
    this.meetingService.deleteMeeting(this.groupID, meetingID).subscribe(
      () => this.getMeetings()
    );
  }

  /**
   * Toggles the map for meetings in the list.
   * @returns {void}
   */
  toggleMap(key: number, meetingID: number): void {
    if (document.getElementById('meeting-' + meetingID).style.display === 'none') {
      document.getElementById('meeting-' + meetingID).style.display = 'block';
    } else {
      document.getElementById('meeting-' + meetingID).style.display = 'none';
    }
  }

  /**
   * Sets the latitude and longitude for a meeting in the list based on its
   * location.
   * @param {number} key - The meeting to get data for.
   * @returns {void}
   */
  setMeetingLatLng(key: number): void {
    this.mapService.getLocationData(this.meetings[key].location).subscribe(
      data => {
        let result = data.results[0].geometry.location;
        this.meetings[key].lat = result.lat;
        this.meetings[key].lng = result.lng;
      }
    );
  }

  /**
   * Gets the latitude and longitude for the map in the create meeting form
   * given a location in string form.
   * @param {string} location - The location in the meeting form.
   * @returns {void}
   */
  getLatLng(location: string): void {
    this.mapService.getLocationData(location).subscribe(
      data => {
        let location = data.results[0].geometry.location;
        this.meeting.lat = location.lat;
        this.meeting.lng = location.lng;
      }
    );
  }

  /**
   * Places a pin on the map after the user stops typing.
   * @param event - The location that the user entered.
   * @returns {void}
   */
  updateMap(event): void {
    clearTimeout(this.typingTimer);
    this.typingTimer = setTimeout(
      () => {
        this.getLatLng(event);
      }, this.doneTypingInterval
    );
  }

  /**
   * Sends a photo to the server for classification.
   * @returns {void}
   */
  uploadImage(): void {
    let element = (document.getElementById("fileInput") as HTMLInputElement);
    let image = element.files[0];
    var reader = new FileReader();
    reader.onloadend = () => {
      this.meetingService.sendImageForClassification(reader.result).subscribe(
        response => {
          this.meeting.location = response;
          this.getLatLng(this.meeting.location);
        }
      );
    }
    reader.readAsDataURL(image);
  }

}
