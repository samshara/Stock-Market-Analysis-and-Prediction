import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif

def select_kbest_clf(data_frame, target, k=4):
    """
    Selecting K-Best features for classification
    :param data_frame: A pandas dataFrame with the training data
    :param target: target variable name in DataFrame
    :param k: desired number of features from the data
    :returns feature_scores: scores for each feature in the data as 
    pandas DataFrame
    """
    feat_selector = SelectKBest(f_classif, k=k)
    _ = feat_selector.fit(data_frame.drop(target, axis=1), data_frame[target])
    
    feat_scores = pd.DataFrame()
    feat_scores["F Score"] = feat_selector.scores_
    feat_scores["P Value"] = feat_selector.pvalues_
    feat_scores["Support"] = feat_selector.get_support()
    feat_scores["Attribute"] = data_frame.drop(target, axis=1).columns
    
    return feat_scores

df = pd.read_csv("NABIL.csv")
df.drop(df.columns[[0,1,9,13]], axis=1, inplace=True)
df.drop(df.index[:19],inplace=True)

kbest_feat = select_kbest_clf(df, 'Updown', k=4)
kbest_feat = kbest_feat.sort(["F Score", "P Value"], ascending=[False, False])
print("\nFeature scores using classification method \n")
print(kbest_feat)

