# Website-Maitainence-

The attached code is used to update the HTML, XML and required javascript code for each blog entry.  The program generates new files for each to maintain an archive on my personal device. 

Each file contains a "Catch Comment" used to identify where the blog entries will be added to the corresponding code.  Using the catch comment, all code prior to and after the comment is stored and the blog entry is inserted in-between.  

For HTML and XML it was straight forward:
  HTML: generate the heading and paragraphs then write them into the new file in-between "before" and "after"
  XML: Same as HTML with the additional data at the front end of the XML Entry.
  
For the javascript file it was slightly more complicated.  The blog entries are stored in an object with the key being the title of the entry and the value being the date the entry was published.  In order to add the entry to the file, the location of the "{" was needed and then the new key:value pair was concatenated to the string.
