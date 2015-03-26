#By RedSword :D
#And modified by JonnyBoy0719

# Python Version 3.4.x

# Need to be compiled to a win, linux and mac executable file. Somehow..
#import win32com
import Tkinter, Tkconstants, tkFileDialog

class Show_MainWindow(Tkinter.Frame):

	def __init__(self, root):

		Tkinter.Frame.__init__(self, root)

		# options for buttons
		button_opt = {'fill': Tkconstants.BOTH, 'padx': 10, 'pady': 5}

		# define buttons
		Tkinter.Button(self, text='Select resource file', command=self.askopenfilename).pack(**button_opt)
		Tkinter.Button(self, text='Wikitize resource file', command=self.asksaveasfilename).pack(**button_opt)

		# define options for opening or saving a file
		self.file_opt = options = {}
		options['initialdir'] = 'C:\\'
		#options['initialfile'] = 'modevents.res'
		options['parent'] = root
		options['title'] = 'Select Game Events file'
		
		# defining options for opening a directory
		self.dir_opt = options = {}
		options['initialdir'] = 'C:\\'
		options['mustexist'] = False
		options['parent'] = root
		options['title'] = 'Save Wikitized Game Events file'

	def askopenfilename(self):

		# get filename
		filename = tkFileDialog.askopenfilename(**self.file_opt)

		# open file on your own
		if filename:
			fileToRead = open( filename, "r")

			foundEvents = False
			foundEventsLine = 0
			depthLevel = 0
			currentEvent = 0
			currentEventArg = 0
			lineCount = 0
			argsList = []

			while True :
				lineCount += 1
				line = fileToRead.readline()
				if line == "" : #EOF
					break
				
				if foundEvents == False :
					if line.startswith('"') and line.endswith('events"\n') :# \n needed
						foundEvents = True
						foundEventsLine = lineCount
					elif line.startswith('"') and line.endswith('gameevents"\n') :# \n needed
						foundEvents = True
						foundEventsLine = lineCount
						
				else : #found events, we can start parsing
					line = line.strip(" \t\r\n")
					bracketIndex = line.find("{")
					endBracketIndex = line.find("}")
					commentIndex = line.find("//")
					quoteIndex = line.find('"')
					
					#opening bracket
					if bracketIndex == 0 :
						depthLevel += 1
						
					elif endBracketIndex == 0 :
						depthLevel -= 1
						
					#event/arg name
					elif quoteIndex == 0 :
						secondQuoteIndex = line.find( '"', quoteIndex + 1 )
						eventOrArgName = line[quoteIndex + 1:secondQuoteIndex]
						comment = ""
						if commentIndex != -1 :
							comment = line[commentIndex:].lstrip("/ \t")
						#print( eventOrArgName + " : " + comment )
						
						#do something appropriate with event, arg
						if depthLevel == 1 : #event; need to do sth w/ comment
							#argsList.
							eventList.append( ( eventOrArgName, [], comment ) ) #tuple : event : list of kv?
							
						elif depthLevel == 2 : #arg; need to get type and do sth w/ comment
							thirdQuoteIndex = line.find('"', secondQuoteIndex + 1)
							fourthQuoteIndex = line.find('"', thirdQuoteIndex + 1)
							if fourthQuoteIndex == -1 :
								print ( "Unrecognized : %s" % line )
							
							typeArg = line[thirdQuoteIndex + 1:fourthQuoteIndex]
							
							event_args_comment = eventList[ - 1 ]
							event_args_comment[ 1 ].append( ( eventOrArgName, typeArg, comment ) )
							#print( "Adding %r=%r	%r" % (eventOrArgName, typeArg, comment) )
						else :
							print( "Unrecognized : %s" % line )

			print ( "Found %d events" % len( eventList ) )

			fileToRead.close()

	def asksaveasfilename(self):

		# lazy :V
		foundEvents = False
		for event in eventList :
			foundEvents = True

		# get filename
		filename = tkFileDialog.askdirectory(**self.dir_opt)

		if foundEvents == False:
			print( "WARN: No \"Game Events\" has been found." )

		# save filename
		else:
			filename += "/wikitized.txt"
			print("wikitized.txt has been created!")

			fileToWrite = open( filename, "w")

			fileToWrite.write( ":''Refer back to [[Game Events (Source)]] for more events.''\n" )
			fileToWrite.write( "\n\n\n" )

			for event in eventList :

				fileToWrite.write( "=== " + event[ 0 ] + " ===\n" )
				fileToWrite.write( "{{qnotice|%s}}\n" % event[ 2 ] )
				fileToWrite.write( "{{begin-hl2msg|%s|string}}\n" % event[ 0 ] )
				for arg in event[ 1 ] :
					fileToWrite.write( "{{hl2msg|%s|%s|%s}}\n" % ( arg[ 1 ], arg[ 0 ], arg[ 2 ] ) )
				
				fileToWrite.write( "{{end-hl2msg}}\n\n" )

			fileToWrite.close()

if __name__=='__main__':
	eventList = []

	root = Tkinter.Tk()
	root.title("Wikitizer")
	root.resizable(0, 0)

	root.geometry("200x75")

	Show_MainWindow(root).pack()

	root.mainloop()



