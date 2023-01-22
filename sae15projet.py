import csv
import webbrowser
import matplotlib.pyplot as plt
import numpy as np



#Ici, nous allons ouvrir et lire notre fichier non traité que nous allons traiter et dont nous allons extraire les données importantes.
fichier=open("DumpFile.txt", "r")

#création des listes = créer des listes pour remplir chacune d'elle avec les données convenables dans le tcmpdump
ipsr=[]
ipde=[]
longueur=[]
flag=[]
seq=[]
heure=[]

      # créer des compteurs
#compteur du nombre de flag [P] = counter for flag [P] number
flagcounterP=0
#compteur du nombre de flag [S] = counter for flag [S] number
flagcounterS=0
#compteur du nombre de flag [.] = counter for flag [.] number
flagcounter=0
#compteur des trames échangés = counter for number of frames  exchanged on network
framecounter=0
#compteur request = counter for the number of requests
requestcounter=0
#compteur reply = counter for number of replies
replycounter=0
#compteur sequence = sequences counter
seqcounter=0
#compteur acknowledgement = acknowledgments counter
ackcounter=0
#compteur window = windows counter
wincounter=0

for ligne in fichier:
    # faire un split avec un espace comme délimiteur
    split=ligne.split(" ")
    #supprimer les blocs hexadécimaux et ne garder que les lignes qui contiennent l'information
    if "IP" in ligne :
    #remplir la liste des drapeaux    
        framecounter+=1
        if "[P.]" in ligne :
            flag.append("[P.]")
            flagcounterP+=1
        if "[.]" in ligne :
            flag.append("[.]")
            flagcounter+=1
        if "[S]" in ligne :
            flag.append("[S]")
            flagcounterS+=1
        #remplir la liste seq     
        if "seq" in ligne :
            seqcounter+=1
            seq.append(split[8])
        #fenêtres de comptage   
        if "win" in ligne :
            wincounter+=1
        #comptage des acces   
        if "ack" in ligne:
            ackcounter+=1
            
        #remplir la liste des sources IP(ipsr)  
        ipsr.append(split[2])  
        #filling the IP destination(ipde) list
        ipde.append(split[4])
        #filling the hour (heure) list
        heure.append(split[0])
        #filling the lenght (longueur) list
        if "length" in ligne:
            split = ligne.split(" ")
            if "HTTP" in ligne :
                longueur.append(split[-2])
            else: 
                longueur.append(split[-1]) 
        #to detect request and reply via ICMP protocol        
        if "ICMP" in ligne:
            if "request" in ligne:
                requestcounter+=1
            if "reply" in ligne:
                replycounter+=1
'''ipsource2 = []
ipdesti2 = []   
ipdestifinale=[]             
                
for i in ipsr:
    if not "." in i:
        ipsource2.append(i)
    elif "ssh" in i or len(i) > 15 or "B" in i:
        ports = i.split(".")
        del ports[-1]
        delim = "."
        delim = delim.join(ports)
        ipsource2.append(delim)
    else:
        ipsource2.append(i)
for j in ipde:
    if not "." in j:
        ipdesti2.append(j)
    elif "ssh" in j or len(j) > 15 or "B" in j:
        ports = j.split(".")
        del ports[-1]
        delim = "."
        delim = delim.join(ports)
        ipdesti2.append(delim)
    else:
        ipdesti2.append(j)

for l in ipdesti2:
    if not ":" in l:
        ipdestifinale.append(l)
    else:
        deuxp = l.split(":")
        ipdestifinale.append(deuxp[0])   '''

             
globalflagcounter=flagcounter+flagcounterP+flagcounterS

P=flagcounterP/globalflagcounter
S=flagcounterS/globalflagcounter
A=flagcounter/globalflagcounter 

globalreqrepcounter=replycounter+requestcounter
req=requestcounter/globalreqrepcounter
rep=replycounter/globalreqrepcounter
          
#transformer tous les compteurs en listes pour les visualiser sur le fichier csv 
flagcounter=[flagcounter]
flagcounterP=[flagcounterP]
flagcounterS=[flagcounterS]
framecounter=[framecounter]
requestcounter=[requestcounter]
replycounter=[replycounter]
seqcounter=[seqcounter]
ackcounter=[ackcounter]
wincounter=[wincounter]



# create python graphic with matplotlib library 
  #circular graphic for flags
  
'''Flag [.] : Il s'agit d'un drapeau générique qui peut être utilisé pour indiquer un paquet de données qui n'est pas spécifique à un protocole ou une application particulière.

Flag [P] : Il s'agit d'un drapeau qui indique que le paquet de données est un paquet protocole.

Flag [S] : Il s'agit d'un drapeau qui indique que le paquet de données est un paquet de service.'''


name = ['Flag [.]', 'Flag [P]', 'Flag [S]']
data = [A,P,S]

explode=(0, 0, 0)
plt.pie(data, explode=explode, labels=name, autopct='%1.1f%%', startangle=90, shadow=True)
plt.axis('equal')
plt.savefig("graphe1.png")
plt.show()
  #circular graphic for request and reply 
name2 = ['Request' , 'Reply']
data2 = [req,rep]  
explode=(0,0)
plt.pie(data2,explode=explode,labels=name2, autopct='%1.1f%%',startangle=90, shadow=True)
plt.savefig("C:graphe2.png")
plt.show()


#contenu de la page web = web page content 
htmlcontenu='''
<html>
   <head>
      <meta charset="utf-8">
      <title> Traitement des données </title>
      <style>
      body{
          background-color:#3498DB;
          }
      </style>
   </head>
   
   <body>
       <center><h2>Projet SAE15</h2></center>
       <center><p>Sur cette page web on va vous presenter les infomations et donnees petinentes qu'on a trouve dans le fichier a traiter(DumpFili.txt) </p></center>
       <center><h3> Nombre total des trames échangés</h3> %s</center>
       <br>
       <center><h3> Drapeaux (Flags)<h3></center>
       <center>Nombre de flags [P] (PUSH) = %s
       <br>Nombre de flags [S] (SYN) = %s  
       <br>Nombre de flag [.] (ACK) = %s
       <br>
       <br>
       <img src="graphe1.png">
       <h3> Nombre des requests et replys </h3>
       Request = %s 
       <br>
       Reply = %s
       <br>
       <br>
       <img src="graphe2.png">
       <h3>Statistiques entre seq et win et ack </h3>
       Nombre de seq = %s
           <br>
       Nombre de win = %s
           <br>
       Nombre de ack = %s
       
      
   </body>

</html>
'''%(framecounter,flagcounterP,flagcounterS,flagcounter,requestcounter,replycounter,seqcounter,wincounter,ackcounter)

#ouverture d'un fichier csv = open a csv file for data extracted from txt file untreated 
with open('données.csv', 'w', newline='') as fichiercsv:
    writer = csv.writer(fichiercsv)
    writer.writerow(['Heure','IP source','IP destination','Flag','Seq','Length'])
    writer.writerows(zip(heure,ipsr,ipde,flag,seq,longueur))
    fichiercsv.close()
    
#ouverture d'un fichier csv    = open a csv file for different stats
with open('Stats.csv', 'w', newline='') as fichier2:
    writer = csv.writer(fichier2)
    writer.writerow(['Flag[P] (PUSH)','Flag[S] (SYN)','Flag[.] (ACK)','Nombre total de trames',"nombre de request","nombre de reply","nombre de sequence","nombre de acknowledg","nombre de window"])
    writer.writerows(zip(flagcounterP,flagcounterS,flagcounter,framecounter,requestcounter,replycounter,seqcounter,ackcounter,wincounter))
    fichier2.close()
    
#partie page  web = open a web page with important information and statistics
with open("data.html","w") as html:
    html.write(htmlcontenu)
    print("page web créée avec succès")

       
fichier.close()

