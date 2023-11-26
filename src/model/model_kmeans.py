from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from datetime import datetime
import pandas as pd
pd.set_option('display.max_columns', None)


class Clustering:

    def __init__(self, data):

        self.df = pd.DataFrame(data)
        self.preprocessor = None
        self.pca = None
        self.kmeans = None


    def process_data(self):
        # Preprocessing
        print(self.df)
        self.df["dob"] = self.df.apply(lambda row: self.transform_dob_to_age(row["dateOfBirth"]), axis=1)

        features = [
                'iqScore', 'personalityScore', 'age', 'gender', 'dob', 'experience', 
                'styles'
            ]
        X = self.df[features]

        # Encode categorical data and normalize
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), ['iqScore', 'dob']),
                ('cat', OneHotEncoder(), [
                    'personalityScore', 'age', 'gender', 'experience', 'styles'
                ])
            ])
        X_processed = preprocessor.fit_transform(X)

        # Dimensionality Reduction (optional)
        # pca = PCA(n_components=2)
        # X_pca = pca.fit_transform(X_processed)

        # Model Training
        kmeans = KMeans(n_clusters= 2 if len(self.df) > 6 else 3 if len(self.df) > 9 else 1 )  # example: 3 clusters
        # kmeans.fit(X_pca)
        kmeans.fit(X_processed)

        # Assign students to clusters
        self.df['cluster'] = kmeans.labels_
        result = self.df[['user_id', 'cluster']]
        return result

    def predict_cluster(self, new_data):
        # Convert new data to DataFrame for consistent preprocessing
        new_data_df = pd.DataFrame(new_data)

        # Process new data
        new_data_processed = self.preprocessor.transform(new_data_df)
        new_data_pca = self.pca.transform(new_data_processed)

        # Predict cluster
        cluster = self.kmeans.predict(new_data_pca)
        return cluster[0]
    
    @staticmethod
    def transform_dob_to_age(dob):
        """
        Calculate the age of a person given their birth date in 'YYYY-MM-DD' format.

        :param birth_date_str: String representing the birth date in 'YYYY-MM-DD' format.
        :return: Integer representing the age.
        """
        birth_date = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        return age