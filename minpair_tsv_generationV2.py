import pandas as pd
import re

def parse_data_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    entries = re.split(r'\n(?=\d+\.\s+\w+:)', content)
    #print(entries)
    clean_entries = []
    for entry in entries:
        stripped_entry = entry.strip()
        if stripped_entry:
            clean_entries.append(stripped_entry)
    
    homonyms_data = []
    
    for entry in clean_entries:
        homonym_dict = parse_homonym_entry(entry)
        if homonym_dict:
            homonyms_data.append(homonym_dict)
    
    return homonyms_data

def parse_homonym_entry(entry):
    lines = entry.strip().split('\n')
    
    header_match = re.match(
        r'(\d+)\.\s+(\w+):\s*(\d+)\s+\(\[(.+?)\]\s+(?:vs|and)\s+\[(.+?)\]\)', lines[0])
    #print(header_match)
    if not header_match:
        print(f"Warning: Could not parse header: {lines[0]}")
        return None
    
    number = int(header_match.group(1))
    homonym = header_match.group(2).lower()
    homonym_freq = int(header_match.group(3))
    meaning1_syns_raw = header_match.group(4)
    meaning2_syns_raw = header_match.group(5)
    
    meaning1_synonyms, meaning1_freqs = extract_synonyms(meaning1_syns_raw)
    meaning2_synonyms, meaning2_freqs = extract_synonyms(meaning2_syns_raw)
    
    full_text = '\n'.join(lines)
    meaning1_match = re.search(r'Meaning 1:\s*(.+?)\s*\(', full_text)
    meaning2_match = re.search(r'Meaning 2:\s*(.+?)\s*\(', full_text)
    
    if meaning1_match:
        meaning1_name = meaning1_match.group(1).strip()
    else:
        meaning1_name = "meaning1"
    
    if meaning2_match:
        meaning2_name = meaning2_match.group(1).strip()
    else:
        meaning2_name = "meaning2"
    
    content = '\n'.join(lines[1:])
    meanings_split = re.split(r'Meaning 2:', content)
    
    if len(meanings_split) < 2:
        print(f"Warning: Could not find both meanings for {homonym}")
        return None
    
    meaning1_content = meanings_split[0].replace('Meaning 1:', '').strip()
    meaning2_content = meanings_split[1].strip()
    
    meaning1_sentences = extract_sentences_with_target(meaning1_content, homonym)
    meaning2_sentences = extract_sentences_with_target(meaning2_content, homonym)
    
    roi_indices = {}
    all_sentences = meaning1_sentences + meaning2_sentences
    for sent in all_sentences:
        roi_indices[sent] = find_word_index(sent, homonym)
    
    return {
        'number': number,
        'homonym': homonym,
        'homonym_freq': homonym_freq,
        'meaning1_name': meaning1_name,
        'meaning1_synonyms': meaning1_synonyms,
        'meaning1_synonyms_freq': meaning1_freqs,
        'meaning1_sentences': meaning1_sentences,
        'meaning2_name': meaning2_name,
        'meaning2_synonyms': meaning2_synonyms,
        'meaning2_synonyms_freq': meaning2_freqs,
        'meaning2_sentences': meaning2_sentences,
        'roi_indices': roi_indices
    }

def extract_synonyms(synonym_string):
    pairs = re.findall(r'(\w+):\s*(\d+)', synonym_string)
    
    synonyms = []
    frequencies = []
    
    for word, freq in pairs:
        synonyms.append(word)
        frequencies.append(int(freq))
    
    return synonyms, frequencies

def extract_sentences_with_target(text, target_word):
    lines = text.split('\n')
    sentences = []
    
    for line in lines:
        stripped = line.strip()
        if stripped:
            sentences.append(stripped)
    
    target_sentences = []
    for sent in sentences:
        cleaned_sent = sent.replace('.', '').replace(',', '').lower()
        words = cleaned_sent.split()
        if target_word in words:
            target_sentences.append(sent)
    
    return target_sentences

def find_word_index(sentence, target_word):
    words = sentence.split()
    
    for i, word in enumerate(words):
        clean_word = word.strip('.,!?;:').lower()
        if clean_word == target_word.lower():
            return i
    
    error_msg = f"Could not find '{target_word}' in sentence: {sentence}"
    raise ValueError(error_msg)

def generate_pair_rows(word1, word2, base_sentences, roi_indices, condition, sentid_start, pairid_start):
    all_rows = []
    sentid = sentid_start
    pairid = pairid_start
    
    for sentence in base_sentences:
        roi_index = roi_indices[sentence]
        words = sentence.split()
        
        expected_row = {
            "sentid": sentid,
            "pairid": pairid,
            "condition": condition,
            "comparison": "expected",
            "sentence": sentence,
            "ROI": roi_index,
        }
        all_rows.append(expected_row)
        sentid += 1
        
        synonym_words = words.copy()
        synonym_words[roi_index] = word2
        synonym_sentence = " ".join(synonym_words)
        
        unexpected_row = {
            "sentid": sentid,
            "pairid": pairid,
            "condition": condition,
            "comparison": "unexpected",
            "sentence": synonym_sentence,
            "ROI": roi_index,
        }
        all_rows.append(unexpected_row)
        sentid += 1
        pairid += 1
    
    return all_rows, sentid

def process_all_homonyms(data_filepath, output_dir="."):
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    print("Parsing data file...")
    homonyms_data = parse_data_file(data_filepath)
    print(f"Found {len(homonyms_data)} homonyms\n")
    
    all_rows = []
    sentid_counter = 1
    pairid_counter = 1
    
    for homonym_data in homonyms_data:
        homonym = homonym_data['homonym']
        homonym_freq = homonym_data['homonym_freq']
        
        print(f"\nProcessing: {homonym} (freq: {homonym_freq})")
        
        meaning1_name = homonym_data['meaning1_name']
        meaning1_sentences_count = len(homonym_data['meaning1_sentences'])
        meaning1_synonyms = homonym_data['meaning1_synonyms']
        
        print(f"Meaning 1 ({meaning1_name}): {meaning1_sentences_count} sentences")
        print(f"Synonyms: {meaning1_synonyms}")
        
        meaning2_name = homonym_data['meaning2_name']
        meaning2_sentences_count = len(homonym_data['meaning2_sentences'])
        meaning2_synonyms = homonym_data['meaning2_synonyms']
        
        print(f"Meaning 2 ({meaning2_name}): {meaning2_sentences_count} sentences")
        print(f"Synonyms: {meaning2_synonyms}")
        
        try:
            if len(homonym_data['meaning1_synonyms']) >= 1:
                synonym1 = homonym_data['meaning1_synonyms'][0]
                condition = f"{homonym}_meaning1_syn1"
                
                rows, sentid_counter = generate_pair_rows(
                    homonym,
                    synonym1,
                    homonym_data['meaning1_sentences'],
                    homonym_data['roi_indices'],
                    condition,
                    sentid_counter,
                    pairid_counter
                )
                all_rows.extend(rows)
                num_pairs = len(rows) // 2
                pairid_counter += num_pairs
            
            if len(homonym_data['meaning1_synonyms']) >= 2:
                synonym2 = homonym_data['meaning1_synonyms'][1]
                condition = f"{homonym}_meaning1_syn2"
                
                rows, sentid_counter = generate_pair_rows(
                    homonym,
                    synonym2,
                    homonym_data['meaning1_sentences'],
                    homonym_data['roi_indices'],
                    condition,
                    sentid_counter,
                    pairid_counter
                )
                all_rows.extend(rows)
                num_pairs = len(rows) // 2
                pairid_counter += num_pairs
            
            if len(homonym_data['meaning2_synonyms']) >= 1:
                synonym1 = homonym_data['meaning2_synonyms'][0]
                condition = f"{homonym}_meaning2_syn1"
                
                rows, sentid_counter = generate_pair_rows(
                    homonym,
                    synonym1,
                    homonym_data['meaning2_sentences'],
                    homonym_data['roi_indices'],
                    condition,
                    sentid_counter,
                    pairid_counter
                )
                all_rows.extend(rows)
                num_pairs = len(rows) // 2
                pairid_counter += num_pairs
            
            if len(homonym_data['meaning2_synonyms']) >= 2:
                synonym2 = homonym_data['meaning2_synonyms'][1]
                condition = f"{homonym}_meaning2_syn2"
                
                rows, sentid_counter = generate_pair_rows(
                    homonym,
                    synonym2,
                    homonym_data['meaning2_sentences'],
                    homonym_data['roi_indices'],
                    condition,
                    sentid_counter,
                    pairid_counter
                )
                all_rows.extend(rows)
                num_pairs = len(rows) // 2
                pairid_counter += num_pairs
                
        except Exception as e:
            print(f"  ERROR processing {homonym_data['homonym']}: {e}")
    
    print(f"\n{'='*60}")
    print("Saving TSV file...")
    
    if all_rows:
        df = pd.DataFrame(all_rows)
        df['comparison'] = df['comparison'].astype(str).str.strip()
        df['condition'] = df['condition'].astype(str).str.strip()
        df['ROI'] = df['ROI'].astype(int)
        df['sentid'] = df['sentid'].astype(int)
        df['pairid'] = df['pairid'].astype(int)
        
        filepath = f"{output_dir}/homonym_minimal_pairs.tsv"
        df.to_csv(filepath, sep='\t', index=False)
        
        total_rows = len(df)
        total_pairs = len(df) // 2
        
        print(f"  {filepath}: {total_rows} rows, {total_pairs} pairs")
    
    print(f"{'='*60}")
    return df

def main():
    data_filepath = "data/data.txt"
    output_dir = "minimal_pairs_tsvs"
    
    df = process_all_homonyms(data_filepath, output_dir)


if __name__ == "__main__":
    main()