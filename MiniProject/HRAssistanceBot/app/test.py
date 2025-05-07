import pandas as pd

# Cek apakah data dapat dibaca dengan benar
df = pd.read_csv("data/faq.csv")
print(df.head())  # Tampilkan beberapa baris data
