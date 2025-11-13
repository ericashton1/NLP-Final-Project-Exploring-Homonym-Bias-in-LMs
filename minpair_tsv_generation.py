import pandas as pd

data = {'sentid': [], 'pairid': [], 'sentence': [], 'roi': []}
numset = ['0,', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def main():
    
    with open('data/data.txt', 'r') as file:
        lines = file.readlines()
        sentid = 0
        pairid = 0
        homonym = ''
        roi = 0
        for line in lines:
            words = line.strip().split()
            if line == '':
                continue
            # print("words", words)
            # print("0th ind: ", words[0])
            # print("0th ind 0th ind: ", words[0][0])
            #print(len(words))
            #signals new homonym
            if len(words) > 0 and words[0][0] in numset:
                homonym = words[1]
            #ignore line that tells you meaning
            elif len(words) > 0 and words[0] == 'Meaning':
                continue
            else:
                #get roi for minpair set
                if ( pairid == 0):
                    for i in range(len(words)):
                        if words[i] == homonym:
                            roiFound = True
                            roi = i
                            break
                sentid += 1
                pairid += 1
                data['sentid'].append(sentid)
                data['pairid'].append(sentid)
                data['sentence'].append(line)
                data['roi'].append(roi)
                if (pairid == 3):
                    pairid = 0
    
                
    
    
            
    
    dataframe = pd.DataFrame(data)
    dataframe.to_csv('data/minpair_data.tsv', sep = '\t')

if __name__ == "__main__":
    main()