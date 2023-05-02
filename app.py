from flask import Flask, render_template, request
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Ana sayfa
@app.route('/')
def home():
    return render_template('index.html')

# Form gönderildiğinde çalışacak olan fonksiyon
@app.route('/result', methods=['POST'])
def result():
    # Form verilerini al
    age = int(request.form['age'].lower())
    gender = str(request.form['gender'])
    kids = int(request.form['number_of_kids'])

    # Veri setini yükle
    df = pd.read_csv('customers.csv')
    df['gender'] = df['gender'].replace({'MALE': 0, 'FEMALE': 1})

    # Verileri ölçeklendir
    scaler = StandardScaler()
    df['age'] = scaler.fit_transform(df[['age']])

    # Modeli oluştur
    x = df.iloc[:, [1, 2, 3]].values
    kmeans = KMeans(n_clusters=4, init='k-means++', max_iter=1000)
    kmeans.fit(x)

    # Yeni müşteriyi modele ekle
    new_customer = [[gender, age, kids]]
    new_customer[0][1] = scaler.transform([[new_customer[0][1]]])[0][0]
    new_customer_segment = kmeans.predict(new_customer)

    segment = new_customer_segment[0]

    # Yaşa göre sınıflandırma yap
    if age >= 18 and age <= 29:
        age_group = "Genç"
    elif age >= 30 and age <= 49:
        age_group = "Orta yaşlı"
    else:
        age_group = "Yaşlı"

    return render_template('result.html', segment=segment, age_group=age_group)


if __name__ == '__main__':
    app.run(debug=True)
