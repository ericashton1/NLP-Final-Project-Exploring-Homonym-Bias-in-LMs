import pandas as pd

def main():

    #print("hello")
    df = pd.read_csv("results/homonym_minimal_pairs_byword_adjusted.tsv", sep="\t")
    
    df_target = df[df["ROI"] == df["wordpos"]].copy()
    
    results = []
    for pid, group in df_target.groupby("pairid"):
        if group["comparison"].nunique() == 2:  # need both conditions
            conds = group.set_index("comparison")["adjusted_surp"]
            if all(c in conds for c in ["expected", "unexpected"]):
                diff = conds["expected"] - conds["unexpected"]
                results.append(diff)
    

    avg_diff = sum(results) / len(results)
    avg_abs_diff = sum(abs(d) for d in results) / len(results)
    
    print(results)
    print(f"Average (signed) probability difference: {avg_diff:.6f}")
    print(f"Average absolute probability difference: {avg_abs_diff:.6f}")

if __name__ == "__main__":
    main()