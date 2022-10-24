"""This program reads in a blog entry .txt file and updates HTML, XML and JS files.
 
The program reads in a .txt file in the following format:
    line 1: Title
    Line 2: Summary
    Lines 3+: Blog entry
The entry is parsed and added to the HTML, XML and JS Files that require updating.
This program relies on the use of a Catch Comment for both HTML/XML and JavaScript.
These comments are stored as global variables.

Typical usage example:

  blogInput = FileReader()
  html = HTML(blogInput)
  js = JS(blogInput)
  xml = XML(blogInput)
"""


from datetime import datetime
import codecs

# Initialize GLobal Variables
HTML_COMMENT = "<!-- First Entry -->"   # Catch Comment for HTML/XML
JS_COMMENT = "// Post Object Location"  # Catch Comment for JavaScript

class FileReader(object):
    """Reads in blog entry and initializes attributes to be used in subclasses.

    Parses blog entry .txt file in the following format:
        line 1: Title
        Line 2: Summary
        Lines 3+: Blog entry
    Initializes all inherited attributes below

    Attributes:
        date: A date String in YYYY-mm-ddTHH:MM:SSZ format
        jsDate: A date String for the drop down menu in dd MMM YYYY format
        title: A String for the title of the blog post
        title_: A String for the title of the blog post, words connected with "_"
        summary: A String for the summary of the blog post
        content: A multi-line String for the blog content
        paragraph: A list of Strings with each element being a paragraph
            of the blog post surrounded by <p></p> tags
    """
    def __init__(self):
        
        # initialize date
        now = datetime.utcnow()
        self.date = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.jsDate = "\"" + now.strftime("%d %b %Y") + "\""
        
        # entry parsing
        entryFile = open("entry.txt")   # read in entry txt file
        
        # title and summary
        self.title = entryFile.readline().strip("\n")
        print(self.title[1])
        self.summary = entryFile.readline().strip("\n")
        
        # iterate through remaining lines for content of entry
        self.content = [""""""]
        block = 0
        for line in entryFile:
            self.content[block] += line.strip("/n")
            if "\n" in line:
                block += 1
                self.content.append("""""")
        
        for el in self.content:
            el.strip("\n")
        
        entryFile.close()
        
        # replace " " with "_" for id in html and href
        self.title_ = "_".join(self.title.split())
        
        # encapsulate blog entry in paragraph tags for HTML/XML
        self.paragraph = self.paragraph_generator()
        
    def read_in_file(self,fileName, comment):
        """
        Reads in file, fileName and parses it into two sections; before and 
        after the catch comment, comment.
        
        Parameters
        ----------
        fileName : String
            The file to be read in.
        comment : String
            The catch comment.

        Returns
        -------
        before : A List of Strings
            All code before the catch comment.
        after : A List of Strings
            All code after the catch comment.
        spaceCount : An integer
            The spaces the comment line is indented.

        """
        file = codecs.open(fileName, "r")
        commentLine = False
        before = []
        after = []
        spaceCount = 0
        
        for line in file:
            # all code before catch comment stored in before, all code after 
            #   after the catch comment stored in after
            if not commentLine:
                before.append(line)
            else:
                after.append(line)
            
            noSpaces = line.strip()
            if noSpaces == comment:
                commentLine = True
                # iterate through line catch comment is on to determine number
                #   of spaces to align code
                for i in line:
                    if i == " ":
                        spaceCount += 1
                    else:
                        break
        file.close()
        
        return (before, after, spaceCount)
    
    def paragraph_generator(self):
        """
        This method generates paragraphs from the blog entry.

        Returns
        -------
        paragraph : A List of strings
            each element is content of the blog entry between 
            HTML/XML paragraph tags.

        """
        paragraph = []
        # iterate through blocks of text and add tags
        for block in self.content:
            paragraph.append("<p>" + block + "</p>" + "\n")
        return paragraph
    
    def file_writer(self, fileName, before, after, entry):
        """
        Writes before, entry and after to file FileName

        Parameters
        ----------
        fileName : A String representing the file to be written.
        before : A List of Strings before the catch comment
        after : A List of Strings after the catch comment.
        entry : A String of content to be inserted between before and after

        Returns
        -------
        None.

        """
        file = open(fileName, "w")
        
        for line in before:
            file.write(line)
            
        file.write(entry)
            
        for line in after:
            file.write(line)
        
        file.close()
        
    def get_date(self):
        return self.date
    
    def get_jsDate(self):
        return self.jsDate
    
    def get_title(self):
        return self.title
    
    def get_underscore_title(self):
        return self.title_
    
    def get_summary(self):
        return self.summary
    
    def get_paragraph(self):
        return self.paragraph
    
        
    


class HTML(FileReader):
    """
    Subclass of FileReader that reads in an HTML File and inserts blog entry 
        content.
    Attributes:
        title: A String for the title of the blog post
        title_: A String for the title of the blog post, words connected with "_"
        paragraph: A list of Strings with each element being a paragraph
            of the blog post surrounded by <p></p> tags
        heading: A String of the heading conent between <h1></h1> tags.
        before: all code before the catch comment
        after: all code after the catch comment
        spaceCount: An integer of spaces to align with existing code.
    """
    
    
    def __init__(self, blogInput):
        """ Inits HTML Class and initializes all variables.  All class methods
            are called from the init method.  Writes new HTML File with updated
            content from blog entry.

        Parameters
        ----------
        blogInput : FileReader object

        """
        # Get attributes from blogInput needed for HTML File
        self.title = blogInput.get_title()
        self.title_ = blogInput.get_underscore_title()
        self.paragraph = blogInput.get_paragraph()
        
        # initialize HTML Content
        htmlFile = "index.html"
        self.heading = self.heading_generator() # class method
        self.before = """"""    # HTML Content before the blog entry
        self.after = """"""     # HTML Content after the blog entry
        self.spaceCount = 0
        
        self.before, self.after, self.spaceCount = self.read_in_file(htmlFile, HTML_COMMENT)
        entry = self.HTML_entry()
        self.file_writer("blog_entry/index.html", self.before, self.after, entry)
        
    def heading_generator(self):
        """
        Generates a heading for the blog entry.

        Returns
        -------
        A Multi-line String
            header in following format:.
            <h1 id="title">title</h1>

        """
        return """<h1 id=\"""" + self.title_ + "\">" + self.title + "</h1>"
    
    def HTML_entry(self):
        """
        Places all text entries between <p></p> tags.

        Returns
        -------
        entry : A list of multi-line Strings; each element is a paragraph of text between 
            <p></p> tags

        """
        
        entry = """"""
        entry += " "*self.spaceCount + self.heading + "\n"
        for para in self.paragraph:
            entry += " "*self.spaceCount + para
        return entry
    
        
class JS(FileReader):
    """
    Subclass of FileReader that reads in a javascript file and inserts data
        for the blog entry links drop down menu inside the blogObject Object
    
    Attributes:
        title: A String representing the title of the blog entry, pulled from
            blogInput
        jsDate: A date String for the drop down menu in dd MMM YYYY format
        jsObject: A String representing the title and date of the blog entry 
            for the drop down menu.
        before: all code before the catch comment.
        after: all code after the catch comment.  Element in index 0 updated
            with new blogObject content.
        spaceCount: An integer of spaces to align with existing code.

    """
    
    
    def __init__(self, blogInput):
        """ Inits JS Class and initializes all variables.  All class methods
            are called from the init method.  Writes new JS File with updated
            content from blog entry.

        Parameters
        ----------
        blogInput : FileReader object

        """
        # Get attributes from blogInput needed for HTML File        
        self.title_ = blogInput.get_underscore_title()
        self.jsDate = blogInput.get_jsDate()

        jsFile = "components/blog-links.js"
        self.jsObject = self.js_object()
        self.before, self.after, self.spaceCount = self.read_in_file(jsFile, JS_COMMENT)
        
        blogObject = self.after[0]
        # find location of "{": add 1 to include "{" in substrings
        startPoint = blogObject.find("{") + 1   
        # update line with new element in blogObject
        newBlogObject = blogObject[0:startPoint] + self.jsObject + blogObject[startPoint:]
        
        self.after[0] = newBlogObject   #replace first element in after with updated line
        
        self.file_writer()
        
    def js_object(self):
        """
        Generates the text used in the drop down menu for links to each blog entry.

        Returns
        -------
        A String in the following format: "Title of Blog Entry: Date".

        """
        
        return self.title_ + ":" + self.jsDate + ","
    
    def file_writer(self):
        """
        Writes before and after to file FileName.

        Overrides FileReader file_writer method.

        Returns
        -------
        None.

        """
        
        file = open("blog_entry/blog-links.js", "w")
        
        for jsline in self.before:
            file.write(jsline)
            
        for jsline in self.after:
            file.write(jsline)
        
        file.close()

class XML(FileReader):
    """
    Subclass of FileReader that reads in an HTML File and inserts blog entry 
        content.
    Attributes:
        date: A date String in YYYY-mm-ddTHH:MM:SSZ format
        title: A String for the title of the blog post
        title_: A String for the title of the blog post, words connected with "_"
        summary: A String for the summary of the blog post
        paragraph: A list of Strings with each element being a paragraph
            of the blog post surrounded by <p></p> tags
        before: all code before the catch comment
        after: all code after the catch comment
        spaceCount: An integer of spaces to align with existing code.
    """    
    
    def __init__(self, blogInput):
        """ Inits XML Class and initializes all variables.  All class methods
            are called from the init method.  Writes new XML File with updated
            content from blog entry.

        Parameters
        ----------
        blogInput : FileReader object

        """
        
        
        # FileReader.__init__(self)
        # Get attributes from blogInput needed for HTML File  
        self.date = blogInput.get_date()
        self.title = blogInput.get_title()
        self.title_ = blogInput.get_underscore_title()
        self.paragraph = blogInput.get_paragraph()
        self.summary = blogInput.get_summary()
        
        xmlFile = "feed.xml"
        
        self.before, self.after, self.spaceCount = self.read_in_file(xmlFile, HTML_COMMENT)
        
        self.xml_entry()
        
        self.file_writer("blog_entry/feed.xml", self.before, self.after, self.entry)
        
    def xml_entry(self):
        # XML entry content
        self.entry = """  <entry>
		<title>""" + self.title + """</title>
		<link href="https://jordangallivan.dev/#""" + self.title_ + """" />
		<link rel="alternate" type="text/html" href="https://jordangallivan.dev/"/>
        <published>""" + self.date + """</published>
		<updated>""" + self.date + """</updated>
		<summary>""" + self.summary + """</summary>
        <content type="html">
        """ 
        # blog entry
        for para in self.paragraph:
            self.entry += para
        # closing XML content
        self.entry += """
		</content>
		<author>
			<name>Jordan Gallivan</name>
		</author>
        </entry>"""
        
blogInput = FileReader()
html = HTML(blogInput)
js = JS(blogInput)
xml = XML(blogInput)
