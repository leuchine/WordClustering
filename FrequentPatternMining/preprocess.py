f=open('symptom.csv')
first=True
symptoms=[]
for i in f:
	if first==True:
		first=False
		continue
	symptom=i.split(',')[2].split(";;")
	newsymptom=[]
	for j in symptom:
		newsymptom+=[j.strip('"').lower()];
	setsymptom=set(newsymptom)
	dissymptom=list(setsymptom)
	symptoms+=[dissymptom]

fw=open('bracket.txt','w')
for i in symptoms:
	str=""
	for j in i:
		str+=j.lower()+","
	fw.write(str.strip(',')+"\n")
