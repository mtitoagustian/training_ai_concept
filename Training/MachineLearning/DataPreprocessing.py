# Import library
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris

# Load dataset
data = load_iris()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

# Memisahkan fitur dan label
X = df.drop('target', axis=1)
y = df['target']

# Normalisasi data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Pembagian data (Train-Test Split)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

print(f"Train set shape: {X_train.shape}, Test set shape: {X_test.shape}")
