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
list_keys=['CHROM','POS','ID','REF','ALT','QUAL','FILTER','INFO','FORMAT','SAMPLE']
ID_seq={}
ClesID_seq =ID_seq.keys()
cpt=0
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

# Reading of the lines
with open ("reads_vcf.txt", "a+") as reads_vcf, open ("reads_filtered_outils_vcf.txt", "a+") as reads_filtered_vcf:   # Detected Reads are written in reads_vcf.txt with ID in first column as main key 
  for line in reads :     
    tmp=line.split('\t')
    if len(tmp)==12 and (tmp[0]!='#CHROM'):   # Not taking account of the name parameters line
      ID_seq[tmp[2]]={}
      if tmp[2]=='.':                         # Take the ID as main key
        i=i+1
        ID_seq[tmp[2]]={str(i):{}}
        for n in range (len(list_keys)):      # Dico set up when no ID
          ID_seq[tmp[2]][str(i)][list_keys[n]]=tmp[n]
        del ID_seq[tmp[2]][str(i)]['ID']
        info=ID_seq[tmp[2]]['INFO']
        infoSplt=info.split(';')
        SVType=int((infoSplt[1]).split('=')[1])
        print (SVType)            
        SVLen=int((infoSplt[10]).split('=')[1])
        AF=float((infoSplt[1]).split('=')[1])
        # DP=float((infoSplt[4]).split('=')[1])
        # Cov=(((infoSplt[5]).split('=')[1]).split(','))[2]
        
        ID_seq[tmp[2]]['INFO']={'SVType':SVType,'SVLen':SVLen,'AF':AF}      # <DEL> has 10 subkeys instead of 11 like the others, INFO dico is set up 

        if (ID_seq[tmp[2]]['QUAL'])=='.' or float(ID_seq[tmp[2]]['QUAL'])<float(Qual) or float(ID_seq[tmp[2]]['INFO']['DP'])<float(0): # Remove Reads under the Qual filter or without Qual information
          # print(tmp[2]+" Filtré: "+ID_seq[tmp[2]][str(i)]['QUAL'])
          continue
        else:
          reads_vcf.write(str(tmp[2]+"\t"+ID_seq[tmp[2]][str(i)]['CHROM']+"\t"+ID_seq[tmp[2]][str(i)]['POS']+"\t"+ID_seq[tmp[2]][str(i)]['REF']+"\t"+ID_seq[tmp[2]][str(i)]['ALT']+"\t"+ID_seq[tmp[2]][str(i)]['QUAL']+"\t"+ID_seq[tmp[2]][str(i)]['FILTER']+"\t"+ID_seq[tmp[2]][str(i)]['INFO']+"\t"+ID_seq[tmp[2]][str(i)]['FORMAT']+"\t"+ID_seq[tmp[2]][str(i)]['SAMPLE']+"\t"+ID_seq[tmp[2]][str(i)]['S2']+"\t"+ID_seq[tmp[2]][str(i)]['S3']+"\n"))
    
      else:                                   # Dico set up when an ID is met for the first time
        for n in range (len(list_keys)):
          ID_seq[tmp[2]][list_keys[n]]=tmp[n]
        del ID_seq[tmp[2]]['ID']              # Remove the ID dupplicate among the secondaries keys
        # reads_vcf.write(str(tmp[2]+"\t"+ID_seq[tmp[2]]['CHROM']+"\t"+ID_seq[tmp[2]]['POS']+"\t"+ID_seq[tmp[2]]['INFO']['SVType']+"\t"+ID_seq[tmp[2]]['INFO']['SVLen']+"\n"))
        
        if(ID_seq[tmp[2]]['ALT']=='<DEL>'):
          info=ID_seq[tmp[2]]['INFO']           # Extract data from 'INFO'
          infoSplt=info.split(';')
          # AF=float((infoSplt[1]).split('=')[1]) 
          # SUP=int((infoSplt[10]).split('=')[1])
          # SVLen=int((infoSplt[11]).split('=')[1])
          # SVType=str((infoSplt[12]).split('=')[1])
          # Cov=(infoSplt[3]).split('=')[1]
        else:
          info=ID_seq[tmp[2]]['INFO']           # Extract data from 'INFO'
          infoSplt=info.split(';')
          # AF=float((infoSplt[1]).split('=')[1])
          # SUP=int((infoSplt[10]).split('=')[1])
          # SVLen=int((infoSplt[12]).split('=')[1])
          # SVType=str((infoSplt[13]).split('=')[1])
          # Cov=(infoSplt[3]).split('=')[1]

        # ID_seq[tmp[2]]['INFO']={'SVType':SVType,'SVLen':SVLen,'AF':AF,'SUP':SUP,'Cov':Cov}

        # samp=ID_seq[tmp[2]]['SAMPLE']         # Extract data from 'SAMPLE'
        # sampSplt=((samp.split('\n'))[0]).split(':')
        # ID_seq[tmp[2]]['SAMPLE']={'DR':sampSplt[2],'DV':sampSplt[3]}

        # reads_filtered_vcf.write(str(ID_seq[tmp[2]]['CHROM']+"\t"+ID_seq[tmp[2]]['POS'])+"\t"+str(ID_seq[tmp[2]]['INFO']['SVType'])+"\t"+str(ID_seq[tmp[2]]['INFO']['SVLen'])+"\t"+str(ID_seq[tmp[2]]['INFO']['AF'])+"\t"+str(ID_seq[tmp[2]]['INFO']['Cov'])+"\n")
        # print("Les fichiers de sortie ont été crees")
# print(info)
# print(infoSplt)
# print('AF: ',AF)
# print('SUP: ',SUP)
# print('SVLEN: ',SVLen)
# print('SVType',SVType)
# # print('idseq: ',ID_seq['Sniffles2.DEL.F1S0'])
# print(infoSplt)
# print(ID_seq.keys())
