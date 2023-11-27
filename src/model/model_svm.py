import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from datetime import datetime


class SVMModel:
    def __init__(self):

        pass

    # Functions to process the data
    def process_personality_score(self, string):
        if type(string)!=str:
            return len(personalityScore)
        personalityScore = ['agreeableness', 'conscientiousness', 'extraversion', 'neuroticism', 'openness']
        try:
            index = personalityScore.index(string.lower())
            return index
        except ValueError:
            return len(personalityScore)

    def process_experience(self, string):
        if type(string)!=str:
            return len(experience)
        experience = ['beginner', 'intermediate', 'advanced']
        try:
            index = experience.index(string.lower())
            return index
        except ValueError:
            return len(experience)

    def process_styles(self, string):
        styles = ['visual', 'auditory', 'kinesthetic']
        if type(string)!=str:
            return len(styles)
        try:
            index = styles.index(string.lower())
            return index
        except ValueError:
            return len(styles)

    def process_gender(self, string):
        if type(string)!=str:
            return len(gender)
        gender = ['male', 'female']
        try:
            index = gender.index(string.lower())
            return index
        except ValueError:
            return len(gender)

    def transform_dob_to_age(self, dob):
        birth_year = datetime.strptime(dob, "%Y-%m-%d").year
        current_year = datetime.now().year
        return current_year - birth_year

    def process_dataframe(self, df):
        df["styles"] = df.apply(lambda row: self.process_styles(row["styles"]), axis=1)
        df["experience"] = df.apply(lambda row: self.process_experience(row["experience"]), axis=1)
        df["personalityScore"] = df.apply(lambda row: self.process_personality_score(row["personalityScore"]), axis=1)
        df["gender"] = df.apply(lambda row: self.process_gender(row["gender"]), axis=1)
        df["dob"] = df.apply(lambda row: self.transform_dob_to_age(row["dateOfBirth"]), axis=1)
        
        features = ['iqScore', 'styles', 'experience', 'personalityScore', 'gender', 'dob']
        X = df[features]
        return X

    def process_target(self, string, target_list):
        try:
            index = target_list.index(string.lower())
            return index
        except ValueError:
            return len(target_list)

    def train_model_response(self, data, new_user):
        # Converting data to DataFrame
        df = pd.DataFrame(data)
        
        # Processing the DataFrame
        df_processed = self.process_dataframe(df)
        target_list = list(df['groupId'].unique())
        # If length of groupId is 1 return
        print("USER TARGET GROUPS", target_list)
        if len(target_list)<2:
            # Add user to existing group
            return target_list[0]
        
        df["groupId"] = df.apply(lambda row: self.process_target(row["groupId"],target_list), axis=1)
        

        # Target and features
        y = df['groupId']
        X = df_processed

        # Creating and training the SVM model
        svm_model = SVC()
        svm_model.fit(X, y)

        df_new = pd.DataFrame(new_user)

        # Processing the DataFrame
        df_processed_new = process_dataframe(df_new)

        # predict group for new user
        group_label = svm_model.predict(df_processed_new)[0]
        predicted_label = target_list[group_label]

        return predicted_label
        