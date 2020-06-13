<h1> Demo Django website created for the Exhibit Experience team at the New York Hall of Science </h1>

<p> I created this website to create a way to track data for the daily operations of Design Lab. 
The technologies used in this website are Django, Gmail and Google Sheets API.</p>

<h3> What data does the website help keep track of? </h3>
<p> The website allows the team to track: <br>
  1. Activities that can be run in Design Lab. <br>
  2. Activities that are unrunnable in Design Lab. <br>
  3. How often an acitivty is run in Design Lab. <br>
  4. How often an acitivity breaks. <br>
  5. A log for each activity, to keep track of why certain activities break, or are removed. <br>
  6. Visitor statistics: Lowest, Highest and Average visitation for the month. <br>
  
<h3> Gmail API </h3>
<p> Information about museum group visitation for a specific day are sent to the team via email in a google sheets format. The website contains a script under management/commands that filters through the Gmail API for the email and processes it to display on the website. </p>

<h3> Google Sheets API </h3>
<p> The google sheets API is used to create and save a spreadsheet containing all the data for that month. </p>


