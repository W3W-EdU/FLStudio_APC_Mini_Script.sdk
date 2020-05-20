#name=AKAI APC Mini (Mixer Control)

# Import the required modules

import mixer 
import midi
import device
import ui

def OnInit():
	global selectedBank
	selectedBank = 1
	clearAllLEDs()
	device.midiOutMsg(0x90 + (0x40 << 8) + (0x01 << 16))


def OnNoteOn(event):   #Let's tell FL what to do when it recieves a note on event through midi
	#print('Midi note on:', event.data1, " ", event.data2)
	if event.data1 > 63 and event.data1 < 81 or event.data1 > 81 and event.data1 < 88:	#Check to see if the note is in the range used by the patch selector
		event.handled = True #Start by telling FL we are dealing with this note to stop it from playing a tone
		setPatchBank(event.data1) #If it is, pass it through to the function that selects patches
		ui.setHintMsg("Bank " + str(selectedBank) + " selected (" + str(((selectedBank-1)*9)) + "-" + str(((selectedBank-1)*9)+8) + ")")
	elif event.data1 == 98:
		ui.setHintMsg("LEDs Turned off")
		clearAllLEDs()
		event.handled = True
	else:
		event.handled = False #Allows you to continue to use the pads inside of the FPC if you want to

def OnNoteOff(event):	#Tell FL what to do with note off data
	event.handled = True	#Not much here, just stop FL from getting too excited and playing a tone


def OnControlChange(event):	 #Let's define what FL will do when a slider moves
	if (event.pmeFlags & midi.PME_System != 0):	#Not entirely sure what this does, (pretty certian it rate limits) but it seems to improve performance, so I'll leave it in.
		mixer.setTrackVolume(bankSliderToChan(selectedBank, event.data1), event.data2/127) #Set the mixer track volume according to the input

def setPatchBank(bank): 	#This allows us to set the patch bank we are using
	global selectedBank #Makes the variable accessable everywhere
	if bank < 80:	#See if we are in the bottom row
		selectedBank = bank - 63	#perform the expression needed to convert from midi to mixer channel data
		clearAllLEDs() #Clears the LEDs that are on
		device.midiOutMsg(0x90 + (bank << 8) + (0x01 << 16)) #Turns on the appropriate LED
	if bank > 80:	#See if we are in the side row
		selectedBank = bank - 73	#perform the expression needed to convert from midi to mixer channel data
		clearAllLEDs() #Clears all of the LEDs
		device.midiOutMsg(0x90 + (bank << 8) + (0x01 << 16))
	return selectedBank	#Return the selected bank as an integer.

def bankSliderToChan(bank, slider):
	slider = slider-47 #Convert from midi to channel number
	return (((bank-1)*9)+slider-1) # Get the base number in the bank by subtracting 1 from it and multiplying by 9. Then add the slider -1 to this to get the channel number.
def clearAllLEDs():
	LEDNumber = 0
	for LEDNumber in range(0, 89):
		device.midiOutMsg(0x90 + (LEDNumber << 8) + (0x00 << 16))