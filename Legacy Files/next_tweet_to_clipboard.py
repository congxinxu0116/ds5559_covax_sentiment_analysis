randi = random.randint(1, dictlen) #generate random index
print(f"you're reviewing tweet # {counter}\n\n") #print out progress

counter += 1 #increment counter
nextid = dicts[randi] #grab next random sample

#get link if existing and open in new tab
tok = nextid['text'].split(" ") 
tok = [x for x in tok if "http" in x]
if tok:
    webbrowser.open(tok[-1])

printout = ",\n\n{" #initialize printout string

for key, value in nextid.items():
    if key != "compound": #exclude compound VADER item, not useful
        if key in ["main_emotion", "label"]:
            value = f'"{value}"' #add quotes around strings
        elif key == "text":
            value = f'"""{value}"""' #add quotes around strings
        elif key in ["neg", "neu", "pos"]: #round VADER valence
            value = round(value,0)
        #neatly formate beginning and end of string
        space = "" if key == "index" else "\n   "
        end = "" if key == "label" else ","
        #add dict entry to output string
        printout += f"{space}'{key}': {value}{end}"

#print out finished dict string
printout += "}"
print(printout)

#copy output string to clipboard
pyperclip.copy(printout) 