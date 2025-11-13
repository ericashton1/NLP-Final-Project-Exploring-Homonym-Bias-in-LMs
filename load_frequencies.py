import pandas as pd
import string
import numpy as np
from sklearn.linear_model import LinearRegression

data = {'sentid': [], 'pairid': [], 'sentence': [], 'roi': []}
numset = ['0,', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def main():
    freq_dict ={}
    freq_df = pd.read_csv('freqs_coca.tsv', sep='\t')
    words_list = freq_df['word'].tolist()
    count_list = freq_df['count'].tolist()
    for i in range(len(words_list)):
        freq_dict[words_list[i]] = count_list[i]
    #print(freq_dict)
    evaluate_df = pd.read_csv('results/homonym_minimal_pairs_byword.tsv', sep='\t')
    eval_words = evaluate_df['word_mod'].tolist()
    eval_freqs = []
    #count was used to check how many unfound words there were. Only 4 so we can ignore
    #count = 0
    for word in eval_words:
        #https://www.geeksforgeeks.org/python/string-punctuation-in-python/ used this source for cleaning strings
        word = word.lower().strip().translate(str.maketrans('', '', string.punctuation))
        if word in freq_dict:
            eval_freqs.append(freq_dict[word])
        else:
            #count += 1
            eval_freqs.append(0)
    #print(count)
    evaluate_df['freqs'] = eval_freqs
    evaluate_df.to_csv('results/homonym_minimal_pairs_byword.tsv', sep='\t', index = False)


    
    
    #https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html used this source for linear regression
    freqs = np.array(evaluate_df['freqs']).reshape((-1,1))
    probs = np.array(evaluate_df['prob']).reshape((-1,1))
    regression = LinearRegression()
    reg = regression.fit(freqs, probs)
    a = regression.intercept_
    b = regression.coef_[0]
    adjusted_probs = []
    for i in range(len(evaluate_df['freqs'])):
        freq = evaluate_df['freqs'][i]
        prob = evaluate_df['prob'][i]
        expected_prob = a + b * freq
        adjusted_prob = prob - expected_prob
        adjusted_probs.append(adjusted_prob)
    evaluate_df['adjusted_probs'] = adjusted_probs
    evaluate_df.to_csv('results/homonym_minimal_pairs_byword.tsv', sep='\t', index = False)

if __name__ == "__main__":
    main()