# CyStudy
During my Sophomore semester in college, I took a semester-long project course (COM S 309) where I was a member of a group of four students who built a web application from scratch. This included generating the features, requirements, code, tests, and deployment.

Our group created a study group finder web application using the Angular front-end framework, the Django back-end framework, and MySQL for the database. The features of this project can be found below:

User Authentication: This application uses the built-in Django authentication system to authenticate users
Study Groups: This application allows Student users to create and join a study group. The deletion of a study group is controlled by the Course Admin user. Each study group has the following functionality:
Creating a meeting: A study group meeting can be set up by any student in the study group. The Google Maps API is used to choose and show the location of the meeting. The time, date, and description of the meeting are also input.
Real-time Messaging: Django Channels and JavaScript are used to create web sockets to allow for real-time messaging between users in a study group. Each study group has its own messaging room.
Notes Creation: Each study group has a notes section where they can create “sticky notes” style notes. These notes can be created and deleted.
Building Identifier: The building identifier allows the user to take a picture of an Iowa State University campus building, and the application will identify that specific building. This helps students know where they are on campus.
Course Admin and Moderator Functionality: The course admin is in charge of creating and deleting courses. They also have the ability to delete study groups. The Moderator can report and ban students from participating in study groups.
For this application, I mainly worked on the Django back-end and the MySQL database. During the project, I learned a lot about the software development process. I also learned about the difference between front and back end development and how to integrate the two together. I also learned more about approaches to learning new frameworks and programming languages by utilizing online resources (tutorials, discussion boards), my group members, and TAs.


# Installation
Change to the directory you want to clone this git repository to and clone the repository.
```
cd directory_location
git clone https://github.com/mmorth/CyStudy.git
```

Install Python using the following [link](https://www.python.org/downloads/)

Create a virtual enviornment using the following [link](https://virtualenv.pypa.io/en/stable/installation/)

Use pip to install the necessary modules.
```
pip install -r requirements.txt
```

Install npm from the following [link](https://www.npmjs.com/get-npm)

Install redis server from the following [link](https://redis.io/topics/quickstart)
https://www.python.org/downloads/

# Run Application
From the main project directory, change into the client directory and run ng serve.
```
cd client
ng serve
```

In a separate command line window, change into the server directory and start Django.
```
cd server
python manage.py runserver
```

Navigate to the address given by the ng serve command. You now have access to the entire application.
