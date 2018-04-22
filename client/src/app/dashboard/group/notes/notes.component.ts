import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/switchMap';

import { Note } from '../../../models/note';
import { NoteService } from '../../../services/note.service';
import { GroupIDService } from '../../../services/group-id.service';

/**
 * Represents the page for posting study group notes.
 */
@Component({
  selector: 'app-notes',
  templateUrl: './notes.component.html',
  styleUrls: ['./notes.component.css']
})
export class NotesComponent implements OnInit {

  /**
   * The group's unique ID.
   */
  groupID: number;

  /**
   * An array of notes.
   */
  notes: Note[] = [];

  /**
   * Keys for use when displaying the notes in the template.
   */
  keys = [];

  /**
   * A note object for creating a new note.
   */
  note: Note = new Note();

  /**
   * Any error that the note service returns.
   */
  error: any;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private noteService: NoteService,
    private groupIDService: GroupIDService
  ) {
    groupIDService.paramSource.subscribe((params) => {
      this.groupID = params.id;
    });
  }

  /**
   * Runs when the component initializes.
   */
  ngOnInit() {
    this.getNotes();
  }

  /**
   * Calls the note service to get all the notes for this group.
   */
  getNotes() {
    this.noteService.getNotes(this.groupID).subscribe(
      data => {
        this.notes = { ...data };
        this.keys = Object.keys(this.notes);
      },
      error => this.error = error,
    )
  }

  /**
   * Calls the note service to create a new note.
   */
  createNote() {
    this.noteService.createNote(this.groupID, this.note).subscribe(
      () => {
        this.getNotes();
        this.note.text = "";
      }
    )
  }

  /**
   * Calls the service to delete a note.
   * @param {number} noteID The note to delete.
   */
  deleteNote(noteID: number) {
    this.noteService.deleteNote(this.groupID, noteID).subscribe(
      () => this.getNotes()
    );
  }

}
