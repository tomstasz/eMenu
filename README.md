# eMenu
API do zarządzania restauracyjnymi kartami dań.

## INSTALACJA I URUCHOMIENIE

Po sklonowaniu repozytorium na dysk projekt możemy uruchomić lokalnie na dwa sposoby: standardowo albo w kontenerach (jeśli mamy zainstalowanego Dockera).
Aby uruchomić standardowo najpierw należy założyć środowisko wirtualne i zainstalować niezbędne biblioteki. W katalogu projektu wykonujemy:
```sh
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```
Następnie uruchamiamy aplikację poleceniem:
```sh
python manage.py runserver
```
Z kolei aby uruchomić projekt w kontenerach, w katalogu z plikiem docker-compose.yml używamy komendy:
```sh
docker-compose up -d
```
## ENDPOINTY I PARAMETRY
Aby zobaczyć dokumentację wszystkich endpointów projektu wchodzimy na adres:
```sh
http://127.0.0.1:8000/swagger/
```
Dodatkowo, korzystając z urla listy kart menu możemy (używając parametrów GET) sortować listę według nazw lub liczby dań w karcie.

Aby posortować według nazw dodajemy parametr
```sh
nazwa=
```
Aby posortować według liczby dań dodajemy parametr:
```sh
dania=
```
Przykład:
```sh
http://127.0.0.1:8000/index/?nazwa=xxx
```
Jeśli chcemy wykonać testy aplikacji używamy komendy:
```sh
python manage.py test
```


