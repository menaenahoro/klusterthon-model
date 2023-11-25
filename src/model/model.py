from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
import pandas as pd

class Clustering:

    def __init__(self, df):
        self.df = df
        self.preprocessor = None
        self.pca = None
        self.kmeans = None


    def process_data():
        # Preprocessing
        features = ['IQ', 'personality', 'education', 'age', 'gender']
        X = df[features]

        # Encode categorical data and normalize
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), ['IQ', 'age']),
                ('cat', OneHotEncoder(), ['personality', 'education', 'gender'])
            ])
        X_processed = preprocessor.fit_transform(X)

        # Dimensionality Reduction (optional)
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_processed)

        # Model Training
        kmeans = KMeans(n_clusters=3)  # example: 3 clusters
        kmeans.fit(X_pca)

        # Assign students to clusters
        df['cluster'] = kmeans.labels_

    def predict_cluster(self, new_data):
        # Convert new data to DataFrame for consistent preprocessing
        new_data_df = pd.DataFrame([new_data], columns=['IQ', 'Personality', 'Education', 'Age', 'Gender'])

        # Process new data
        new_data_processed = self.preprocessor.transform(new_data_df)
        new_data_pca = self.pca.transform(new_data_processed)

        # Predict cluster
        cluster = self.kmeans.predict(new_data_pca)
        return cluster[0]
