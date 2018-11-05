import os

stool = ['SRS024075','SRS024388','SRS011239']
tongue = ['SRS075404','SRS043663','SRS062761']

for id in stool:
    os.system("wget ftp://public-ftp.ihmpdcc.org/Illumina/stool/"+str(id)+".tar.bz2")
    os.system("ls")
    os.system("tar xf "+str(id)+".tar.bz2")
    os.system("rm "+str(id)+".tar.bz2")
    os.system("cd "+str(id)+" && ls")
    os.system("rm "+str(id)+"/"+str(id)+"*single*")
    os.system("cd "+str(id)+" && ls")
    os.system("cat "+str(id)+"/"+str(id)+"*.fastq > "+str(id)+"/"+str(id)+".fastq")
    os.system("cd "+str(id)+" && ls")
    os.system("rm "+str(id)+"/"+str(id)+"*novo*")
    os.system("cd "+str(id)+" && ls")

for id in tongue:
    os.system("wget ftp://public-ftp.ihmpdcc.org/Illumina/tongue_dorsum/"+str(id)+".tar.bz2")
    os.system("ls")
    os.system("tar xf "+str(id)+".tar.bz2")
    os.system("rm "+str(id)+".tar.bz2")
    os.system("cd "+str(id)+" && ls")
    os.system("rm "+str(id)+"/"+str(id)+"*single*")
    os.system("cd "+str(id)+" && ls")
    os.system("cat "+str(id)+"/"+str(id)+"*.fastq > "+str(id)+"/"+str(id)+".fastq")
    os.system("cd "+str(id)+" && ls")
    os.system("rm "+str(id)+"/"+str(id)+"*novo*")
    os.system("cd "+str(id)+" && ls")

# ftp://public-ftp.ihmpdcc.org/Illumina/stool/SRS024075.tar.bz2
# ftp://public-ftp.ihmpdcc.org/Illumina/stool/SRS024388.tar.bz2
# ftp://public-ftp.ihmpdcc.org/Illumina/stool/SRS011239.tar.bz2
# ftp://public-ftp.ihmpdcc.org/Illumina/tongue_dorsum/SRS075404.tar.bz2
# ftp://public-ftp.ihmpdcc.org/Illumina/tongue_dorsum/SRS043663.tar.bz2
# ftp://public-ftp.ihmpdcc.org/Illumina/tongue_dorsum/SRS062761.tar.bz2
