# DSZI_Survival - Sieć Neuronowa
### Autor: Jonathan Spaczyński

## Cel zastosowania w projekcie
W projekcie DSZI_Survival sieć neuronowa użyta jest do podejmowania decyzji przez agenta.
Decyzja polega na rozpoznawaniu zdjęć owoców (jabłka i gruszki). W przypadku nie rozpoznania owocu przez
agenta, dochodzi do zatrucia i agent umiera/przegrywa.

## Przygotowanie danych

* **Krok 1** Przechowywane zdjęcia owoców muszą przejść przez proces zamiany zdjęcia (.jpg) na dane, które
mogą być wykorzystane przez sieć neuronową.

```python
CATEGORIES = ["Apple", "Pear"]
IMG_SIZE = 64

training_data = []


def create_training_data():
    for category in CATEGORIES:
        path = os.path.join(DATADIR, category)
        class_num = CATEGORIES.index(category)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                training_data.append([new_array, class_num])
            except Exception as e:
                pass
```
zdjęcia są przechowywane w tablicy training_data wraz z klasyfikacją (class_num) odpowiadającą jakim typem owocu jest zdjęcie

* **Krok 2** Bardzo ważnym krokiem jest pomieszanie danych. W przeciwnym wypadku nasz model po ciągłym otrzymywanie danych
reprezentujących tylko jedną kategorię owoców mógłby się wyuczyć, aby tylko zgadywać tą kategorię.
```python
random.shuffle(training_data)
```
* **Krok 3** Ostatnim krokiem jest zaktualizowanie danych w taki sposób żeby były z przedziału
od 0 d 255 (reprezentacja koloru danego pixela)
```python
X = X / 255.0
```
## Kilka słów na temat danych
* **Ilość Danych** Do trenowania modelu wykorzystałem 8568 zdjęć gruszek i jabłek 
z czego mniej więcej połowa danych była jednym z typów ww. owoców, a druga połowa
reprezentowała pozostałą kategorią
* **Dane wykorzystane do obliczenia skutecznośći** stanowiły małą i oddzielną część danych wykorzystanych do trenowania.
## Model
* **Dane wejściowe:** Dane o kształcie 64x64 reprezentujące pixele w zdjęciach owoców 
* **Warstwa ukryta:** Składająca się z 128 "neuronów" wykorzystującą sigmoid jako funkcję aktywacyjną 
* **Warstwa wyjściowa:** Składająca się z 2 "neuronów" reprezentujących gruszkę i jabłko
* **Stała ucząca:** 0.001

```python
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(64, 64)),
    tf.keras.layers.Dense(128, activation=tf.nn.sigmoid),
    tf.keras.layers.Dense(2, activation=tf.nn.sigmoid)
    ])

model.compile(tf.keras.optimizers.Adam(lr=0.001),
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
```
## Osiągniecia modelu
* **Trafność:** 86.4%
* **Strata:** 0.312

