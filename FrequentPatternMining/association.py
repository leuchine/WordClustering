from pymining import itemmining, assocrules, perftesting

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
print("OMG2")
relim_input = itemmining.get_relim_input(symptoms)
item_sets = itemmining.relim(relim_input, min_support=18000)
print("OMG")
rules = assocrules.mine_assoc_rules(item_sets, min_support=18000, min_confidence=0.8)
fw=open("result.txt",'w')
for i in rules:
	fw.write(",".join(list(i[0]))+"->"+",".join(list(i[1]))+"||"+str(i[2])+"||"+str(i[3])+"\n")

