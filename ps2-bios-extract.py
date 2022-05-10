#PS2 rom unpacker
#Works well from scph10000 to all slim models
#Rename your dump to 'rom.bin'
#Run and follow instructions
#ALL for all modules or type a number for one module
#new directory will be created
#copy modules list with numbers from console

#How does it work:
# find the RESET module in ROMDIR and determine by offset
#end of the first and beginning of the second module
#read the second module, which is always a ROMDIR structure
#where are the dimensions of all other modules and their name
#Sizes are aligned on 16 bytes


#to-do: implement 16bytes padding in parseROMDIR function - ok
#to-do: make report file with numbers, names and offsets for packing modules back in to dump
#to-do: implement command line argument file opening and excetions
filename = 'rom.bin' ##type yours
import os
import sys


def romOPEN(romfile):
    print("Opening:" + romfile)
    romsize = os.path.getsize(romfile)
    #always 32Mbps
    rom = open(romfile, 'rb')
    return rom

def findROMDIRSIZE( file , romsize ):
    #ROMDIR is always behind RESET
    #ROMDIR size = size of the entire table + 16 null bytes
    i=0 #counter
    a=0 #first byte R
    b=[] #other ESET bytes
    d=[] #4 bytes where size is given in little-endian
    e=0 #File location after RESET e.g. 0x2705 for scph-10000
    f=0 # size value in big-endian
    g=0 #ROMDIR size
    h=0 #start ROMDIR (0x2700 for scph-10000)
    
    print("Searching for RESET module size")
    for i in range(0,romsize): # Pass through the file
        a = file.read(1)
        
        if (a[0]==0x52):  #R
            b=list(file.read(4))
            if (b[0:] ==[0x45,0x53,0x45,0x54]): #ESET
                e=file.tell() #0x2705 для scph-10000
                h=e-5
                print("Found at:" + hex(h))
             
                f=parseSIZE(file,(e-5+10+2)) 

                #print("Little-endian:"+d.hex())
                print("RESET size:" +hex (f))
                print("Reset module ends at:" + hex(e-6))

                f=parseSIZE(file,(h+0x10+2+10))

                print("ROMDIR size:" +hex (f))


                #Return the start of ROMDIR and its size
                return h,f
                break
        a=[]
        b=[]

def fixSIZE16 ( size ):
     #Remainder of the division. 16-a=how many bytes to add
    zza=size%16
    zzb=16-zza
    if zza==0:
        return size
    else:
        return size+zzb
    

def parseSIZE (file, offset):
    file.seek((offset)) #go to size bytes
    d=(file.read(4)) #read them
    f=int("0x"+ (d[::-1]).hex() ,16) #change byte order
    return f

def countMODULES (romdir_location):
    a = romdir_location
    b=(((a[1])//16)-1)
    return b

def parseROMDIR(file, romdir_location ):
    print('Modules:')
    #print('')
    i=0 #Counter
    a = romdir_location #To write less
    b=(((a[1])//16)-1) #Number of modules
    modules = [] # Modules
    c=''
    cc=''
    #Module name for loop
    d=0 #Module size for loop
    e=0 #absolute offset for loop
    temp=[]
    file.seek(a[0])
    for i in range (0,b):
        c=file.read(10)
        cc=c.decode('ascii')
        print(str(i)+'.'+(cc))
        file.seek(file.tell()+2)
        #if (i==0) or (i==1) or (i==2) or (i==3):  #scph-70000 derived
        # d=parseSIZE (file, file.tell()) #RESET size is always aligned
        #else:
        d=parseSIZE (file, file.tell())
            
        fd=fixSIZE16(d)
        modules.append([cc,e,fd,d])
        e=e+fd        
        
        
    return modules
        

def extractModule(romfile, modules, module_number ):
    
    
    romfile.seek(modules[module_number][1])
    print(str(module_number)+".Module:" + str(modules[module_number][0]) + " extracted")
    print("    Offset:"+hex(modules[module_number][1]))
    print("    Size 16byte padding:"+hex(modules[module_number][2]))
    print("    Size decimal:"+str(modules[module_number][2]))
    print("    Size as in ROMDIR:"+hex(modules[module_number][3]))

    module_out=romfile.read(modules[module_number][2])
    f = open(str(module_number), "wb")
    f.write(module_out)
    f.close()


###Not used:
#structROMDIR = {'name':10,'ext':2,'size':4}
#Format of records in ROMDIR

#filename = 'rom.bin'

size=os.path.getsize(filename)
romfile=romOPEN(filename)
romdir_location = findROMDIRSIZE(romfile, size)
z=parseROMDIR(romfile, romdir_location)
#print(z) romdir modules names, sizes and fixed offsets and sizes.
moddir='modules-'+filename
try: 
    os.mkdir(moddir)
except OSError as error: 
    exit     
os.chdir(moddir)
modules_count=countMODULES(romdir_location)
print('Total modules:'+str(modules_count)+' from:0 to:' + str(modules_count-1))
innum=input("Type module number or ALL to extract one or ALL modules:")
if innum=='ALL':
   for i in range(0,modules_count):
    extractModule (romfile, z, i)
else:
    extractModule(romfile, z, int(innum))
romfile.close()
input('Type anything to close')
