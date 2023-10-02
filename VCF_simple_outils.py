import os, sys

if  os.path.isdir(sys.argv[1]) == 1 :
  print("Le fichier ne doit pas etre un dossier !")
  exit()
  
temp = sys.argv[1]
file_name = temp.split("/")[-1] # Split file_name from the path
chaine = file_name.split(".")[-1] #Split extension from file_name

if chaine != str("VCF") and chaine != str("vcf")  :   #Check if the file has a SAM extension
  print("Veuillez entrer un fichier avec le format adapté (.vcf)")
  exit()
if os.path.getsize(file_name) == 0  :  #Check if the file is not empty
  print("Le fichier est vide ! sélectionnez un fichier VCF adapté")
  exit()
else :
    print("Fichier ouvert")
    fichier_vcf = open(file_name, "r")   #Open and read file
  
#### Read columns and stock each line, then save all in a dictionnary{}
reads = fichier_vcf.readlines()
list_keys=['CHROM','POS','ID','REF','ALT','QUAL','FILTER','INFO','FORMAT','SAMPLE1','SAMPLE2','SAMPLE3']
ID_seq={}
# ClesID_seq =ID_seq.keys()
# cpt=0
i=0

# Filtering the data based on the quality, the default quality is set to 20 with an option given to the user to change it.
# Qual = 20
# Rep = input("Le seuil de qualité suffisant est défini à 20; voulez-vous le modifier ? Oui/Non"+"\t")
# if Rep != "Oui" and Rep != "Non" :
#   print("Veuillez choisir une réponse valide")
# elif Rep == "Oui" :
#   Qual = input("Entrez la valeur de qualité souhaitée")

# Filtering the data based on the Allel Frequency, the default quality is NULL with an option given to the user to change it.
# Rep = input("Aucun seuil de frequence allelique n'est défini; voulez-vous en ajouter un ? Oui/Non"+"\t")
# if Rep != "Oui" and Rep != "Non" :
#   print("Veuillez choisir une réponse valide")
# elif Rep == "Oui" :
#   seuilAF = input("Entrez la valeur de qualité souhaitée")

list_nv=['nv_SV46-C3216', 'nv_SV33-50121', 'nv_SV35-CAB47', 'nv_SV47-0B2B4', 'nv_SV86-8705F', 'nv_SV443-06D8E', 'nv_SV508-ED32D', 'nv_SV614-69E99']

# Reading of the lines
with open ("reads_vcf.txt", "a+") as reads_vcf, open ("reads_filtered_outils_vcf2.txt", "a+") as reads_filtered_vcf:   # Detected Reads are written in reads_vcf.txt with ID in first column as main key 
  for line in reads :     
    
    tmp=line.split('\t')
    if len(tmp)==12 and (tmp[0]!='#CHROM'):  
        outil=((tmp[2]).split('.'))[0]
        # print(outil)
        i=i+1
        ID_seq[outil]={}
        for n in range (len(list_keys)):      # Dico set up when no ID
           ID_seq[outil][list_keys[n]]=tmp[n]
           
        if (outil=='Sniffles2') :
            info=ID_seq['Sniffles2']['INFO']
            infoSplt=info.split(';')
            AF=float((infoSplt[1]).split('=')[1])
            SUP=str((infoSplt[10]).split('=')[1])
            SVLen=str((infoSplt[11]).split('=')[1])
            Cov=(infoSplt[3]).split('=')[1]  
            # if(str((infoSplt[12]).split('=')[1]) == NULL):
            #     SVType ='.'
            # else:
            #     SVType=str((infoSplt[12]).split('=')[1])
        if (outil=='svim'):
            info=ID_seq['svim']['INFO']
            infoSplt=info.split(';')
            AF='.'
            SUP=str((infoSplt[5]).split('=')[1])
            SVLen='.'
            Cov='.'
            # if (str((infoSplt[6]).split('=')[1]) == NULL):
            #     SVType=str((infoSplt[6]).split('=')[1])
            # else:
            #     SVType ='.'
        if (outil in list_nv):
            info=ID_seq[outil]['INFO']           # Extract data from 'INFO'
            infoSplt=info.split(';')
            AF=float((infoSplt[1]).split('=')[1])
            # SUP=int((infoSplt[10]).split('=')[1])
            SUP='.'
            END=int((infoSplt[2]).split('=')[1])  # POS - END pour avoir SVLen
            # SVType=str((infoSplt[7]).split('=')[1])
            Cov='.'
            SVLen = END - int(ID_seq[outil]['POS'])
    else:
        continue
    ID_seq[outil]['INFO']={'SVLen':SVLen,'AF':AF,'Cov':Cov,'SUP':SUP}
    # reads_filtered_vcf.write(str(ID_seq[outil]['CHROM']+"\t"+ID_seq[outil]['POS'])+"\t"+str(ID_seq[outil]['INFO']['SVLen'])+"\t"+str(ID_seq[outil]['INFO']['AF'])+"\t"+str(ID_seq[outil]['INFO']['Cov'])+"\n")  
    reads_filtered_vcf.write(str(outil)+"\t"+str(ID_seq[outil]['CHROM']+"\t"+ID_seq[outil]['POS'])+"\t"+"\t"+str(ID_seq[outil]['INFO']['SVLen'])+"\t"+str(ID_seq[outil]['INFO']['AF'])+"\t"+str(ID_seq[outil]['INFO']['Cov'])+"\n")
# print(ID_seq['Sniffles2'].keys())
# print(ID_seq['svim']['INFO'])
# print(ID_seq['svim'])






#  ID_seq[outil][list_keys[n]]=tmp[n]
#             # if (outil=='svim') :
#             #     info=ID_seq[outil]['INFO']           # Extract data from 'INFO'
#             #     infoSplt=info.split(';')
#             #     AF='.'
#             #     SUP=int((infoSplt[6]).split('=')[1])
#             #     SVLen='.'
#             #     SVType=str((infoSplt[6]).split('=')[1])
#             #     Cov='.'

#             if (outil=='Sniffles2'):
#                 # info=ID_seq[outil]['INFO']           # Extract data from 'INFO'
#                 # infoSplt=info.split(';')
#                 AF=float((infoSplt[1]).split('=')[1])
#                 SUP=int((infoSplt[10]).split('=')[1])
#                 SVLen=int((infoSplt[11]).split('=')[1])
#                 SVType=str((infoSplt[12]).split('=')[1])
#                 Cov=(infoSplt[3]).split('=')[1]  

#             # if (outil in list_nv):
#             #     continue
#                 # info=ID_seq[outil]['INFO']           # Extract data from 'INFO'
#                 # infoSplt=info.split(';')
#                 # AF=float((infoSplt[1]).split('=')[1])
#                 # SUP=int((infoSplt[10]).split('=')[1])
#                 # END=int((infoSplt[2]).split('=')[1])  # POS - END pour avoir SVLen
#                 # SVType=str((infoSplt[7]).split('=')[1])
#                 # Cov='.'
#                 # ID_seq[tmp[2]]['INFO']={'SVType':SVType,'SVLen':(END-ID_seq[outil]['POS']),'AF':AF}