#!/usr/bin/env python2.2
#
#  Create_options.py :
#  Manuel Barbera Asin, 14 November 2005
#
#  create an options file from a decay files
#============================================================================
# 060616 - fixes
#============================================================================
 
import sys,os,re, string
import time,fileinput

#
# Options for particle guns
# 
def genParticleGuns(eventType):

    global optionsdirroot

    data = ''

    # Momentum Keyword is mandatory
    momentumValues = OptionsValue(decdir,"Momentum")
    if momentumValues != None:
        momentumValues = momentumValues.strip().split()
    else:
        print '\nError: There is not a correct value for the keyword Momentum in '+decdir+'\n'
        sys.exit()

    # Check if exists ExtraOptions keyword
    incl = OptionsValue(decdir,"ExtraOptions")
    if incl != None:
        if len(incl) == 1:
            print "WARNING: There is an ExtraOptions keyword with no value in "+decdir
	else:
            data += "#include \"$DECFILESROOT/options/"+string.strip(incl)+".opts\"\n"

    data += 'Generator.Members -= { "Generation" };\n'
    data += 'Generator.Members -= { "GaudiSequencer/GenMonitor" };\n'
    data += 'Generator.Members += { "ParticleGun", "GaudiSequencer/GenMonitor" };\n'
    data += 'ParticleGun.GunMode = 1;\n'

    if eventType[2] == '0':
        if eventType[1] == '1':
            value = '11'
        elif eventType[1] == '2':
            value = '13'
        elif eventType[1] == '3':
            value = '211'
        elif eventType[1] == '4':
            value = '321'
        elif eventType[1] == '5':
            value = '2212'
        elif eventType[1] == '6':
            value = '22'
        elif eventType[1] == '7':
            value = '111'
    elif eventType[2] == '1':
        if eventType[1] == '1':
            value = '-11'
        elif eventType[1] == '2':
            value = '-13'
        elif eventType[1] == '3':
            value = '-211'
        elif eventType[1] == '4':
            value = '-321'
        elif eventType[1] == '5':
            value = '-2212'
        elif eventType[1] == '6':
            value = '22'
        elif eventType[1] == '7':
            value = '111'

    data += 'ParticleGun.PdgCodes = { %s };\n' % value
    data += 'ToolSvc.EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/%s.dec";\n' % DecayName
    
    # Check if exists ParticleTable keyword
    arg = OptionsValue(decdir,"ParticleTable:")
    if arg != None:
        if len(string.strip(arg)) == 0:
            print "WARNING: The Keyword ParticleTable has no value\n"
        data += "ParticlePropertySvc.ParticlePropertiesFile = \"$PARAMFILESROOT/data/ParticleTable,"+string.strip(arg)+".txt\";"

    # C = 0
    if eventType[3] == '0':
        values = []

        for val in momentumValues:
            values.append( '%s' % val.split('*GeV')[0] )

        for momentum in values:
            dataAux = data
            momentumRound = '%0.f' % float(momentum)
            dataAux += 'ParticleGun.MomentumMin = %s*GeV;\n' % momentum
            dataAux += 'ParticleGun.MomentumMax = %s*GeV;\n' % momentum
            dataAux += 'ParticleGun.EventType = %s%s;\n' % ( eventType[0:8-len(momentumRound)], momentumRound )
            file = optionsdirroot+eventType[0:8-len(momentumRound)]+momentumRound+'.opts'
            if os.path.exists(file):
                print "\n *****  The file "+file+" exists. CHECK it ****"
                print " ***** to overwrite it, you should remove it first\n"
            else:
                f = open(file,'w')
                f.write("// file  "+eventType[0:8-len(momentumRound)]+momentumRound+".opts generated: "+time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())+"\n")
                f.write("//\n")
                f.write("// Event Type:"+eventType[0:8-len(momentumRound)]+momentumRound+"\n")
                f.write("//\n")
                f.write("// ASCII decay Descriptor: "+AsciiName+"\n")
                f.write("//\n")
                f.write(dataAux)
                f.close
            OptionsNickAux = OptionsNick+'%s*GeV' % momentum
            OptionsNameAux = eventType[0:8-len(momentumRound)]+momentumRound
            writeBkkTable(OptionsNameAux,AsciiName,OptionsNickAux,clean)
            writeSQLTable(OptionsNameAux,AsciiName,OptionsNickAux,clean)
    else:
        print 'Warning: Case C!=0 for ParticleGun not implemented yet'
        writeBkkTable(OptionsName,AsciiName,OptionsNick,clean)
        writeSQLTable(OptionsName,AsciiName,OptionsNick,clean)
        sys.exit()

#
#  return the value of the correponding string
#
def OptionsValue(filename,word):
    fd = open(filename)
    fdlines = fd.readlines()
    for fdline in fdlines:
        if fdline.find(word) != -1:
            # every keyword is at the beginning of the line
            if fdline.strip().split(word)[0].strip() == '#':
                return string.strip(string.split(fdline,":")[1])
 
#
#  write the options file
#
def writeOptions(filename,word):
    fd = open(filename,"a+")
    fd.write(word)
    fd.close()
 
#
#  write the header of the options file
#
def HeaderOptions(filename):
    fd = open(filename,"w")
    fd.write("// file  "+OptionsName+".opts generated: "+time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())+"\n")
    fd.write("//\n")
    fd.write("// Event Type:"+OptionsName+"\n")
    fd.write("//\n")
    fd.write("// ASCII decay Descriptor: "+AsciiName+"\n")
    fd.write("//\n")
    fd.close()
     
#
# add the line(# Clean: Yes) in the Decay file
#
#def writeCleanParam(filename):
#    print "The Clean parameter is added in the Decay file ",filename,"\n"
#    for line in fileinput.input(filename,inplace=1):
#        print line[:-1]
#        if line.find("EventType:") != -1:
#            print "#\n# Clean: Yes"
# 
#    os.system("cvs -n update "+filename)
 
#
# write the file to create the entry in the ORACLE database
#
def writeBkkTable(evttypeid,descriptor,nickname,cleanvalue):
    TableName = os.environ["DECFILESROOT"]+"/doc/table_event.txt"
    if not os.path.exists(TableName):
        os.system("touch "+TableName)
        line = "EventTypeID | NickName | Description\n"
        writeOptions(TableName,line)
         
    insert_event = "true"
    for line in fileinput.input(TableName,inplace=1):
        print line[:-1]
        if line.find(evttypeid) != -1:
            insert_event = "false"


    nick = nickname[:min(len(nickname),255)]
    desc = descriptor[:min(len(descriptor),255)]
    if insert_event == "true":
        if cleanvalue == "true":
            line = evttypeid+" | "+nick+" | "+desc+" (clean)\n"
        else:
            line = evttypeid+" | "+nick+" | "+desc+"\n"
             
        writeOptions(TableName,line)
 
         
#
# write the file to create the entry in the ORACLE database
#
def writeSQLTable(evttypeid,descriptor,nickname,cleanvalue):
    TableName = os.environ["DECFILESROOT"]+"/doc/table_event.sql"
    if not os.path.exists(TableName):
        os.system("touch "+TableName)
         
    insert_event = "true"
    for line in fileinput.input(TableName,inplace=1):
        print line[:-1]
        if line.find(evttypeid) != -1:
            insert_event = "false"
            
    # the ORACLE table does not accept names > 256 characters
    # single quote is used in nickname and descriptor so it cannot be used in 'line'
    # use double quotes instead
    nick = nickname[:min(len(nickname),255)]
    desc = descriptor[:min(len(descriptor),255)]
    if insert_event == "true":
        if cleanvalue == "true":
            line = 'svc.addEvtType('+evttypeid+',"'+nick+'","'+desc+'","clean")\n'
        else:
            line = 'svc.addEvtType('+evttypeid+',"'+nick+'","'+desc+'","")\n'
                         
        writeOptions(TableName,line)
 

#
#  create an options file corresponding to a single Decay file
#
def run_create(clean):
    global optionsdir,OptionsName,AsciiName, decdir, OptionsNick
 
    if clean == "true":
        title = DecayName+" clean"
    else:
        title = DecayName
         
    print "Creation of options file for Decay ",title
     
#  Build the name of the dkfiles
    decdir = os.environ["DECFILESROOT"]+"/dkfiles/"+DecayName+".dec"
 
# check if the Decay files exists
    if not os.path.exists(decdir):
        print "The file"+decdir+" does not exist"
        sys.exit()
             
# Get the equivalent eventtype
# convention add +5 to the last for a clean event..
    OptionsName = OptionsValue(decdir,"EventType")
 
# Check if the Nickname is the correct
    OptionsNick = OptionsValue(decdir,"NickName")
    if OptionsNick != DecayName:
        print "WARNING: The nickname "+OptionsNick+" is not equal to the "+DecayName+".dec"
 
# Check if the Descriptor is correct
    AsciiName = OptionsValue(decdir,"Descriptor")
    if AsciiName is None:
        print "ERROR: The Descriptor is not correct.\nIt must have some value"
        print "The options file for "+DecayName+".dec file can't be generated"
        sys.exit()
 
# Check if EventType is 5xxxxxxxx --> particle guns
    if OptionsName[0] == '5':
        genParticleGuns(OptionsName)
        sys.exit()

#check if the options file already exist and do not overwrite it
    if clean == 'true':
        optionsdir = optionsdirroot+OptionsName[0:7]+"5.opts"
    else:
        optionsdir = optionsdirroot+OptionsName+".opts"
    if os.path.exists(optionsdir):
        print " *****  The file "+optionsdir+" exists. CHECK it ****"
        print " ***** to overwrite it, you should remove it first\n"
        
        writeBkkTable(OptionsName,AsciiName,OptionsNick,clean)
        writeSQLTable(OptionsName,AsciiName,OptionsNick,clean)
        sys.exit()
 
# EventType must have 8 digits ( GSDCTNXU, G<>0 )
# Check if the EventType is correct
    if OptionsName is None:
        print "ERROR: The EventType is not correct.\nIt must have some value"
        print "The options file for "+DecayName+".dec file can't be generated"
        sys.exit()
    # The EventType mustn't start by zero
    if OptionsName[0] == '0':
        print "ERROR: The EventType is not correct.\nIt mustn't start by 0"
        print "The options file for "+DecayName+".dec file can't be generated"
        sys.exit()
    # The EventType must have at least 8 digits
    if len(OptionsName) < 8:
        print "ERROR: The EventType is not correct.\nIt must have at least 8 digits"
        print "The options file for "+DecayName+".dec file can't be generated"
        sys.exit()
 
    # Check Type
    if OptionsName[0] == '3':
        if OptionsName[1] == '0':
                # MinimumBias
                sample = "MinimumBias"
    elif int(OptionsName[0]) in (1, 2):
        if OptionsName[1] == '0':
                # Inclusive
                sample = "Inclusive"
        elif int(OptionsName[0]) == 1 and int(OptionsName[1]) in (1, 2, 3, 5):
                # SignalRepeatedHadronization
                sample = "SignalRepeatedHadronization"
        elif int(OptionsName[0]) == 2 and int(OptionsName[1]) in (1, 2, 3, 4):
                # SignalPlain
                sample = "SignalPlain"
        elif int(OptionsName[0]) == 1 and int(OptionsName[1]) == 4:
            # SignalForcedFragmentation
            sample = "SignalForcedFragmentation"
        else:
            sample = "otherTreatment"
    elif int(OptionsName[0]) == 4 and int(OptionsName[1]) in (0, 1, 2):
        sample = "Special"
    elif OptionsName[0] == '6':
        sample = "MinimumBias"
    else:
        sample = "otherTreatment"

    # Check Clean Event
    if clean == "true":
        if sample in ('SignalRepeatedHadronization', 'SignalPlain', 'SignalForcedFragmentation'):
            OptionsName = OptionsName[:-1]+'5'
            #checkClean = OptionsValue(decdir,"Clean:")
            #if checkClean != "Yes":
            #    writeCleanParam(decdir)
        else:
            clean = 'false'
            print "ERROR: You are trying to do Clean with a wrong file type.\nThe file must be from a Signal type.\n"
            sys.exit()
 


# Check if Production keyword is correct
    ProductionValue = OptionsValue(decdir,"Production")
    if ProductionValue is None:
        #print "No Production given: Using Pythia for "+DecayName+".dec file"
        ProductionValue = "Pythia"
    else:
        print "Production: Using %s for %s.dec file" % ( ProductionValue, DecayName )
 
    length = len(ProductionValue.strip().split(' ')) 
    if length > 1:
        engines = []
        for n in range(length):
            engines.append(ProductionValue.strip().split(' ')[n])
        ProductionValue = "Pythia"     
    
# get the first digit of the eventtype
    AB = OptionsName[0:2]
 
    HeaderOptions(optionsdir)
# Higgs files
    if AB == "40":
        str = "#include \"$DECFILESROOT/options/Higgs.opts\"\n"
        writeOptions(optionsdir,str)
 
# Check if exists Include keyword
    incl = OptionsValue(decdir,"ExtraOptions")
    if incl != None:
        if len(incl) == 1:
            print "WARNING: There is an ExtraOptions keyword with no value in "+decdir
	else:
            str = "#include \"$DECFILESROOT/options/"+string.strip(incl)+".opts\"\n"
            writeOptions(optionsdir,str)
 
# Write lines in the options file
    line = "Generation.EventType = "+OptionsName+";\n"
    writeOptions(optionsdir,line)

# Mandatory lines to write -------------------------------------------
 
    str = "Generation.SampleGenerationTool = \""+string.strip(sample)+"\";\n"
    writeOptions(optionsdir,str)

    #ProductionValue
    str = "Generation."+string.strip(sample)+".ProductionTool = \""+string.strip(ProductionValue)+"Production\";\n"
    writeOptions(optionsdir,str)

    str = "ToolSvc.EvtGenDecay.UserDecayFile = \"$DECFILESROOT/dkfiles/"+DecayName+".dec\";\n"
    writeOptions(optionsdir,str)
 
# Optional lines depending of existing keywords -----------------------------------------------
 
# Check if exists DecayEngine keyword
    DecayEngineValue = OptionsValue(decdir,"DecayEngine")
    if DecayEngineValue != None:
        if len(string.strip(DecayEngineValue)) == 0:
            print "WARNING: The Decay Keyword in "+decdir+" has no value\n"
        str = "Generation.DecayTool = \""+string.strip(DecayEngineValue)+"Decay\";\nGeneration."+string.strip(sample)+".DecayTool = \""+string.strip(DecayEngineValue)+"Decay\";\n"
        writeOptions(optionsdir,str)
 
# Check if exists cuts keyword
    CutsValue = OptionsValue(decdir,"Cuts")
    if CutsValue != None:
        if len(string.strip(CutsValue)) == 0:
            print "WARNING: The Cuts Keyword in "+decdir+" has no value\n"
        str = "Generation."+string.strip(sample)+".CutTool = \""+string.strip(CutsValue)+"\";\n"
        writeOptions(optionsdir,str)
 
# Check if exists FullEventCuts keyword
    FullEventCutsValue = OptionsValue(decdir,"FullEventCuts")
    if FullEventCutsValue != None:
        if len(string.strip(FullEventCutsValue)) == 0:
            print "WARNING: The FullEventCuts Keyword in "+decdir+" has no value\n"
        str = "Generation.FullGenEventCutTool = \""+string.strip(FullEventCutsValue)+"\";\n"
        writeOptions(optionsdir,str)
 
# Generation.SAMPLE.GENERATOR.InclusivePIDList
# if Inclusive
    if sample == 'Inclusive':
        if OptionsName[0] == '1':
                list = '521, -521, 511, -511, 531, -531, 541, -541, 5122, -5122, 5222, -5222, 5212, -5212, 5112, -5112, 5312, -5312, 5322, -5322, 5332, -5332, 5132, -5132, 5232, -5232'
        elif OptionsName[0] == '2':
                list = '421, -421, 411, -411, 431, -431, 4122, -4122, 443, 4112, -4112, 4212, -4212, 4222, -4222, 4312, -4312, 4322, -4322, 4332, -4332, 4132, -4132, 4232, -4232, 100443, 441, 10441, 20443, 445, 4214, -4214, 4224, -4224, 4314, -4314, 4324, -4324, 4334, -4334, 4412, -4412, 4414,-4414, 4422, -4422, 4424, -4424, 4432, -4432, 4434, -4434, 4444, -4444, 14122, -14122,  14124, -14124, 100441'
        str = "Generation.Inclusive.InclusivePIDList = {"+list+"};\n"
        writeOptions(optionsdir,str)
# if Type Signal
    else:
        listing = {'10':'521, -521, 511, -511, 531, -531, 541, -541, 5122, -5122, 5222, -5222, 5212, -5212, 5112, -5112, 5312, -5312, 5322, -5322, 5332, -5332, 5132, -5132, 5232, -5232','11':'511,-511','12':'521,-521','13':'531,-531','14':'541,-541','15':'5122,-5122','19':'521, -521, 511, -511, 531, -531, 541, -541, 5122, -5122, 5332, -5332, 5132, -5132, 5232, -5232','20':'421, -421, 411, -411, 431, -431, 4122, -4122, 443, 4112, -4112, 4212, -4212, 4222, -4222, 4312, -4312, 4322, -4322, 4332, -4332, 4132, -4132, 4232, -4232, 100443, 441, 10441, 20443, 445, 4214, -4214, 4224, -4224, 4314, -4314, 4324, -4324, 4334, -4334, 4412, -4412, 4414,-4414, 4422, -4422, 4424, -4424, 4432, -4432, 4434, -4434, 4444, -4444, 14122, -14122,  14124, -14124, 100441','21':'411,-411','22':'421,-421','23':'431,-431','24':'443','25':'4122,-4122'}
        if listing.has_key(AB):
            str = "Generation."+string.strip(sample)+".SignalPIDList = {"+listing[AB]+"};\n"
            writeOptions(optionsdir,str)
         
# write Clean lines   
    if clean == "true":
        str = "Generation."+sample+".Clean = true;\n"
        str = str + "GeneratorToG4.HepMCEventLocation = \"/Event/Gen/SignalDecayTree\";\n"
        writeOptions(optionsdir,str)

#  test if a Decay could have a clean event type
#    if clean == "false":
#        checkClean = OptionsValue(decdir,"Clean:")
#        if checkClean == "Yes":
#            commandline = command+" "+DecayName+" clean"
#            os.system(commandline)
 
# Check if exists ParticleTable keyword
    arg = OptionsValue(decdir,"ParticleTable:")
    if arg != None:
        if len(string.strip(arg)) == 0:
            print "WARNING: The Keyword ParticleTable has no value\n"
        str = "ParticlePropertySvc.ParticlePropertiesFile = \"$PARAMFILESROOT/data/ParticleTable,"+string.strip(arg)+".txt\";\n"
        writeOptions(optionsdir,str)

    writeBkkTable(OptionsName,AsciiName,OptionsNick,clean)
    writeSQLTable(OptionsName,AsciiName,OptionsNick,clean)

 
#
#  loop in the DKFILES directory to generate the options file
#
def run_loop():
    files = os.listdir(os.environ["DECFILESROOT"]+"/dkfiles/")
    for f in files:
        res = re.search('.dec',f)
        if res is not None:
            if len(f.split('.dec')[1]) == 0:  
                basefile = f.split('.')[0]
                commandline = command+" "+basefile
                os.system(commandline)
 
#
#  create the options file
#
#
# give the usage of the command
#
def usage():
    print "This command should be used with the name of the decay file\n"
    print "create_options.py DECAY_NAME\n\n"
    return 0
 
#
#  Main
#
 
# test number of argument
#
global optionsdirroot

loop = "false"
clean = "false"
command = sys.argv[0]
# It is defined because it may be change in the future
optionsdirroot = os.environ["DECFILESROOT"]+"/options/"
 
if len(sys.argv) > 3:
    usage()
    sys.exit()
else:
    if len(sys.argv) == 1:
        loop = "true"
    elif len(sys.argv) == 2:
        DecayName = sys.argv[1]
    elif len(sys.argv) == 3:
        DecayName = sys.argv[1]
        if sys.argv[2].lower() == "clean":
            clean = "true"
        else:
            print "Option "+sys.argv[2]+" unknown\n"
            sys.exit(2)
    else:
        usage()
        sys.exit()
         
if loop == "true":
    run_loop()
    sys.exit(0)
else:
    run_create(clean)
