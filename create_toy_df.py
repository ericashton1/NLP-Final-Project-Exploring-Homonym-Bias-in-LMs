import pandas as pd

def generate_homonymic_df(sentences: dict):
    '''Generate pairs comparing original vs homonymic'''
    all_rows = []
    sentid = 1
    pairid = 1
    
    for original_sentence, (monosemic, homonymic, roi_index) in sentences.items():
        words = original_sentence.split()
        original_word = words[roi_index]
        
        # Original (expected)
        all_rows.append({
            "sentid": sentid,
            "pairid": pairid,
            "comparison": "expected",
            "sentence": original_sentence,
            "ROI": roi_index,
        })
        sentid += 1
        
        # Homonymic (unexpected)
        homonymic_words = words.copy()
        homonymic_words[roi_index] = homonymic
        all_rows.append({
            "sentid": sentid,
            "pairid": pairid,
            "comparison": "unexpected",
            "sentence": " ".join(homonymic_words),
            "ROI": roi_index,
        })
        sentid += 1
        pairid += 1
    
    df = pd.DataFrame(all_rows)
    df['comparison'] = df['comparison'].astype(str).str.strip()
    df['ROI'] = df['ROI'].astype(int)
    df['sentid'] = df['sentid'].astype(int)
    df['pairid'] = df['pairid'].astype(int)
    
    return df

def generate_monosemic_df(sentences: dict):
    '''Generate pairs comparing original vs monosemic'''
    all_rows = []
    sentid = 1
    pairid = 1
    
    for original_sentence, (monosemic, homonymic, roi_index) in sentences.items():
        words = original_sentence.split()
        original_word = words[roi_index]
        
        # Original (expected)
        all_rows.append({
            "sentid": sentid,
            "pairid": pairid,
            "comparison": "expected",
            "sentence": original_sentence,
            "ROI": roi_index,
        })
        sentid += 1
        
        # Monosemic (unexpected)
        monosemic_words = words.copy()
        monosemic_words[roi_index] = monosemic
        all_rows.append({
            "sentid": sentid,
            "pairid": pairid,
            "comparison": "unexpected",
            "sentence": " ".join(monosemic_words),
            "ROI": roi_index,
        })
        sentid += 1
        pairid += 1
    
    df = pd.DataFrame(all_rows)
    df['comparison'] = df['comparison'].astype(str).str.strip()
    df['ROI'] = df['ROI'].astype(int)
    df['sentid'] = df['sentid'].astype(int)
    df['pairid'] = df['pairid'].astype(int)
    
    return df

def main():
    # Dictionary structure: sentence: [monosemic_synonym, homonymic_synonym, word_index]
    sentences = {
        "The family decided to donate money to the local food bank.": ["contribute", "present", 4],  
    
        "She needs to purchase new equipment for the laboratory.": ["acquire", "secure", 3], 
    
        "The company plans to eliminate unnecessary expenses from the budget.": ["remove", "cut", 4],  
    
        "The workers will fabricate metal parts for the new machinery.": ["manufacture", "forge", 3],  
    
        "Students should inquire about scholarship opportunities before applying.": ["ask", "question", 2],  
    
        "Please notify the supervisor immediately if problems arise.": ["inform", "alert", 1], 
    
        "The rules prohibit smoking inside the building at all times.": ["forbid", "bar", 2],  
    
        "The museum will retain all original documents in the archive.": ["keep", "hold", 3],  
    
        "The manager decided to terminate the contract with the vendor.": ["end", "close", 4],  
    
        "Scientists must verify their results through repeated testing.": ["confirm", "check", 2]  
    }
    
    # Generate two separate dataframes
    df_homonymic = generate_homonymic_df(sentences)
    df_monosemic = generate_monosemic_df(sentences)
    
    # Save to separate files
    df_homonymic.to_csv("data/min_pair_homo_toy.tsv", sep='\t', index=False)
    df_monosemic.to_csv("data/minimal_pair_mono_toy.tsv", sep='\t', index=False)
    
    return df_homonymic, df_monosemic

if __name__ == "__main__":
    df_hom, df_mono = main()

