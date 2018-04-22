import { Component } from '@angular/core';

/**
 * The parent component for CyStudy.
 */
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'CyStudy';

  resetMenu(): void {
    document.getElementById("menuScript").remove();
    var menuScript = document.createElement("script");
    menuScript.setAttribute("id", "menuScript");
    menuScript.setAttribute("src", "assets/scripts/menu.js");
    document.body.appendChild(menuScript);
  }
}
