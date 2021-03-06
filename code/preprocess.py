import sys

train_set_label='../data/raw/train/chemdner_cemp_gold_standard_train.tsv'
train_set_text='../data/raw/train/chemdner_patents_train_text.txt'
dev_set_label='../data/raw/dev/chemdner_cemp_gold_standard_development_v03.tsv'
dev_set_text='../data/raw/dev/chemdner_patents_development_text.txt'
test_set_text='../data/raw/test/test.set'
new_train_file='../data/preprocessed/train.tsv'
new_dev_file='../data/preprocessed/dev.tsv'
new_test_file='../data/preprocessed/test.tsv'

def read_sentence(sent):
	tokens=[]
	i=0
	start=-1
	size=0
	while i<len(sent):
		if sent[i]!=' ':
			if size==0:
				start=i
			size=size+1
		else:
			if size!=0:
				tokens.append(sent[start:start+size]+'$$$'+str(start)+'$$$'+str(start+size))
				size=0
		i=i+1
	if size!=0:
		tokens.append(sent[start:start+size]+'$$$'+str(start)+'$$$'+str(start+size))
	return tokens

count=0
def is_part_of_label(token,labels):
	global count
	tokenContent=token.strip().split('$$$')
	tokStart=int(tokenContent[1])
	tokEnd=int(tokenContent[2])
	if labels!=None:
		for label in labels:
			labelContent=label.strip().split('\t')
			labStart=int(labelContent[2])
			labEnd=int(labelContent[3])
			if max(tokStart,labStart)<=min(tokEnd,labEnd):
				count=count+1
				return '$$$I'
	return '$$$O'

def get_annotated_tokens(sent,labels):
	tokens=read_sentence(sent)
	result=''
	cmCount=0
	for token in tokens:
		label=is_part_of_label(token,labels)
		if label=='$$$I':
			cmCount=cmCount+1
		result+=token+label+'\t'
	return result.strip(),cmCount

def get_tokens(sent):
	tokens=read_sentence(sent)
	result=''
	for token in tokens:
		result+=token+'\t'
	return result.strip()

def get_map_entry(map,i):
	if i in map:
		return map[i]
	return None

def process1(label_file,text_file,dest_file):
	#Read the label file
	tit_label_map={}
	abs_label_map={}	
	with open(label_file,"r") as ins:
		for line in ins:
			content=line.strip().split('\t')
			if content[1]=='T':
				if content[0] not in tit_label_map:
					tit_label_map[content[0]]=[]
				tit_label_map[content[0]].append(line.strip())
			if content[1]=='A':
				if content[0] not in abs_label_map:
					abs_label_map[content[0]]=[]
				abs_label_map[content[0]].append(line.strip())	
	#Write the out file
	res_file=open(dest_file,'w')
	with open(text_file,"r") as ins:
		for line in ins:
			content=line.strip().split('\t')
			pId=content[0]
			title=content[1]
			abstract=content[2]
			res_file.write(pId+'\n')			
			text,cmCount=get_annotated_tokens(title,get_map_entry(tit_label_map,pId))
			res_file.write(text+'\n')
			text,cmCount=get_annotated_tokens(abstract,get_map_entry(abs_label_map,pId))
			res_file.write(text+'\n')
	res_file.close()

def process2(text_file,dest_file):
	#Write the out file
	res_file=open(dest_file,'w')
	with open(text_file,"r") as ins:
		for line in ins:
			content=line.strip().split('\t')
			pId=content[0]
			title=content[1]
			abstract=content[2]
			res_file.write(pId+'\n')
			res_file.write(get_tokens(title)+'\n')
			res_file.write(get_tokens(abstract)+'\n')
	res_file.close()

process1(train_set_label,train_set_text,new_train_file)
process1(dev_set_label,dev_set_text,new_dev_file)
process2(test_set_text,new_test_file)