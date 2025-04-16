# career_matcher.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
import joblib

class CareerMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=3000)
        self.kmeans = KMeans(n_clusters=5, random_state=42)
        self.classifier = SVC(kernel='linear', probability=True)

    def fit(self, resumes, labels):
        """
        Melatih model clustering dan klasifikasi.
        resumes: list teks CV (preprocessed)
        labels: label pekerjaan (misalnya: 'Data Analyst', 'DevOps Engineer')
        """
        X = self.vectorizer.fit_transform(resumes)
        self.kmeans.fit(X)
        self.classifier.fit(X, labels)

        # Simpan model
        joblib.dump(self.vectorizer, 'model/tfidf_vectorizer.pkl')
        joblib.dump(self.kmeans, 'model/kmeans_model.pkl')
        joblib.dump(self.classifier, 'model/svm_classifier.pkl')

    def predict_cluster(self, new_resume):
        """
        Prediksi cluster pekerjaan dari CV.
        """
        X_new = self.vectorizer.transform([new_resume])
        cluster = self.kmeans.predict(X_new)
        return int(cluster[0])

    def predict_position(self, new_resume):
        """
        Prediksi posisi kerja terbaik.
        """
        X_new = self.vectorizer.transform([new_resume])
        prediction = self.classifier.predict(X_new)
        return prediction[0]

    def top_matches(self, new_resume, job_descriptions, top_n=3):
        """
        Rekomendasi pekerjaan terdekat berdasarkan cosine similarity.
        """
        job_vectors = self.vectorizer.transform(job_descriptions)
        resume_vector = self.vectorizer.transform([new_resume])
        similarities = cosine_similarity(resume_vector, job_vectors)[0]
        top_indices = similarities.argsort()[-top_n:][::-1]
        return top_indices, [similarities[i] for i in top_indices]
