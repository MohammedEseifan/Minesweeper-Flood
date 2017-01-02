names = ['easy','normal','hard']
tempString = ""
for name in names:
    outfile = open(name+'_scores.score','w')
    outfile.write(tempString)
    outfile.close()
    