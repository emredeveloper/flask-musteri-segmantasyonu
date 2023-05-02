from flask import Flask, render_template, request
import pandas as pd
from sklearn.cluster import KMeans

app = Flask(__name__)


# Ana sayfa
@app.route('/')
def home():
    return render_template('index.html')


# Form gönderildiğinde çalışacak olan fonksiyon
@app.route('/result', methods=['POST'])
def result():
    # Form gönderildiğinde çalışacak olan fonksiyon

    # Form verilerini al
    age = int(request.form['age'].lower())
    gender = str(request.form['gender'])

    kids = int(request.form['number_of_kids'])

    # Veri setini yükle
    df = pd.read_csv('customers.csv')
    df['gender'] = df['gender'].replace({'MALE': 0, 'FEMALE': 1})


    # Modeli oluştur
    x = df.iloc[:, [1, 2, 3]].values
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(x)

    # Yeni müşteriyi modele ekle
    new_customer = [[age, gender, kids]]
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
