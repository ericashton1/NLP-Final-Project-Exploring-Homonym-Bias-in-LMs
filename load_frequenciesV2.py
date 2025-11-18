import pandas as pd
import string
import numpy as np
#from statsmodels.nonparametric.smoothers_lowess import lowess
from pygam import LinearGAM, s

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
    # count was used to check how many unfound words there were. Only 4 so we can ignore
    # count = 0

    for word in eval_words:
        # https://www.geeksforgeeks.org/python/string-punctuation-in-python/
        word = word.lower().strip().translate(str.maketrans('', '', string.punctuation))
        if word in freq_dict:
            eval_freqs.append(freq_dict[word])
        else:
            # count += 1
            eval_freqs.append(0)
    # print(count)

    evaluate_df['freqs'] = eval_freqs

    # MODIFICATION: Add log frequency to avoid regression domination by high-frequency words 
    evaluate_df['log_freq'] = np.log1p(evaluate_df['freqs'])

    evaluate_df.to_csv('results/homonym_minimal_pairs_byword_adjusted.tsv',
                       sep='\t', index=False)

    # MODIFICATION: Use surprisal instead of raw probabilities
    # GPT-like probabilities are highly nonlinear; surprisal linearizes them
    surprisal = np.array(evaluate_df['surp']).reshape((-1, 1))
    log_freqs = np.array(evaluate_df['log_freq']).reshape((-1, 1))



# Fit GAM
    X = evaluate_df['log_freq'].values.reshape(-1, 1)
    y = evaluate_df['surp'].values

    gam = LinearGAM(s(0)).fit(X, y)

# Expected surprisal from GAM smooth
    expected = gam.predict(X)

    evaluate_df['expected_surp_gam'] = expected

    evaluate_df['adjusted_surp'] = (
        evaluate_df['surp'] - evaluate_df['expected_surp_gam']
    )

    evaluate_df['adjusted_prob'] = np.exp(-evaluate_df['adjusted_surp'])


    evaluate_df.to_csv('results/homonym_minimal_pairs_byword_adjusted_GAM.tsv',
                       sep='\t', index=False)

if __name__ == "__main__":
    main()
