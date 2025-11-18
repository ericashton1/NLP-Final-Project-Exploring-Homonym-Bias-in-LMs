import pandas as pd
import string
import numpy as np


def main():
    evaluate_df = pd.read_csv('results/homonym_minimal_pairs_byword_adjusted.tsv', sep='\t')
    homonym_total_adjusted_prob = 0
    nonhomonym_total_adjusted_prob = 0
    total_sentence_count = 0
    count_homonym_more_expected = 0
    most_recent_prob = 0
    num_homonym_sentences = 0
    num_nonhomonym_sentences = 0
    avg_prob_diff = 0
    for i in range(len(evaluate_df['word_mod'])):
        #print(evaluate_df['wordpos'][i] == evaluate_df['ROI'][i])
        if(evaluate_df['wordpos'][i] == evaluate_df['ROI'][i]):
            #print(evaluate_df['comparison'][i])
            if (evaluate_df['comparison'][i] == 'unexpected'):
                #print("INSIDE IF STATEMENT")
                homonym_total_adjusted_prob += evaluate_df['adjusted_prob'][i]
                num_nonhomonym_sentences += 1
                most_recent_prob = evaluate_df['adjusted_prob'][i]
                total_sentence_count += 1
            else:
                nonhomonym_total_adjusted_prob += evaluate_df['adjusted_prob'][i]
                num_homonym_sentences += 1
                if (evaluate_df['adjusted_prob'][i] < most_recent_prob):
                    count_homonym_more_expected += 1
                most_recent_prob = evaluate_df['adjusted_prob'][i]
                total_sentence_count += 1
    #print(homonym_total_adjusted_prob)
    print("Homonym average adjusted prob: ", homonym_total_adjusted_prob / num_homonym_sentences)
    print("Non-homonym average adjusted prob: ", nonhomonym_total_adjusted_prob / num_nonhomonym_sentences)
    print("Count homonym more expected: ", count_homonym_more_expected)
    print("Total sentences: ", total_sentence_count)
   
        



if __name__ == "__main__":
    main()