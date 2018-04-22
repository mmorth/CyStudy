import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { HttpModule } from '@angular/http';
import { AgmCoreModule } from '@agm/core';

import { AppComponent } from './app.component';
import { NotFoundComponent } from './not-found.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { CreateComponent } from './dashboard/create/create.component';
import { CoursesComponent } from './dashboard/courses/courses.component';
import { ModerationComponent } from './dashboard/moderation/moderation.component';
import { GroupComponent } from './dashboard/group/group.component';
import { MeetingsComponent } from './dashboard/group/meetings/meetings.component';
import { NotesComponent } from './dashboard/group/notes/notes.component';
import { ChatComponent } from './dashboard/group/chat/chat.component';
import { HomeComponent } from './dashboard/home/home.component';
import { JoinComponent } from './dashboard/join/join.component';
import { MenuComponent } from './dashboard/menu/menu.component';
import { LoginComponent } from './login/login.component';
import { SignUpComponent } from './sign-up/sign-up.component';

import { AuthGuard } from './services/auth-guard.service';
import { AdminGuard } from './services/admin-guard.service';
import { ModGuard } from './services/mod-guard.service';
import { AuthenticationService } from './services/authentication.service';
import { UserService } from './services/user.service';
import { StudyGroupService } from './services/study-group.service';
import { MeetingService } from './services/meeting.service';
import { NoteService } from './services/note.service';
import { GroupIDService } from './services/group-id.service';
import { CourseService } from './services/course.service';
import { MapService } from './services/map.service';

import { APP_CONFIG, AppConfig } from './app.config';

const appRoutes: Routes = [
  {
    path: '',
    component: LoginComponent
  },
  {
    path: 'sign-up',
    component: SignUpComponent
  },
  {
    path: 'dashboard',
    component: DashboardComponent,
    canActivate: [AuthGuard],
    children: [
      {
        path: '',
        component: HomeComponent
      },
      {
        path: 'join',
        component: JoinComponent
      },
      {
        path: 'create',
        component: CreateComponent
      },
      {
        path: 'group/:id',
        component: GroupComponent,
        children: [
          {
            path: '',
            component: MeetingsComponent
          },
          {
            path: 'notes',
            component: NotesComponent
          },
          {
            path: 'chat',
            component: ChatComponent
          }
        ]
      },
      {
        path: 'courses',
        component: CoursesComponent,
        canActivate: [AdminGuard]
      },
      {
        path: 'moderation',
        component: ModerationComponent,
        canActivate: [ModGuard]
      }
    ]
  },
  { path: '**', component: NotFoundComponent }
];

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    NotFoundComponent,
    HomeComponent,
    MenuComponent,
    JoinComponent,
    CreateComponent,
    SignUpComponent,
    GroupComponent,
    NotesComponent,
    MeetingsComponent,
    ChatComponent,
    DashboardComponent,
    CoursesComponent,
    ModerationComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(
      appRoutes,
      { enableTracing: false }
    ),
    FormsModule,
    HttpClientModule,
    HttpModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyBfqgkKAkaJIhtQQ20ZeO7nr8N9yw9hLOg'
    })
  ],
  providers: [
    AuthGuard,
    AdminGuard,
    ModGuard,
    AuthenticationService,
    StudyGroupService,
    UserService,
    MeetingService,
    NoteService,
    GroupIDService,
    CourseService,
    MapService,
    { provide: APP_CONFIG, useValue: AppConfig }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
