#  Tour de App - [TuATam]

## Fáze 0: Příprava prostředí

Tento repozitář obsahuje základní strukturu projektu pro soutěž Tour de App.

###  Tým

* **Tým Leader:** [Tomáš Nguyen]
* **Člen 2:** [David Žáček]

###  Technologie

* **Backend:** Python (Flask)
* **Deployment:** Docker
* **Verzování:** Git/GitHub

### Spuštění lokálně s Dockerem

Pro ověření funkčnosti kontejneru před nasazením na Tour de Cloud použijte tyto příkazy:

1.  **Sestavení Image:**
    ```bash
    docker build -t tda-app .
    ```
2.  **Spuštění Kontejneru:**
    ```bash
    docker run -d -p 5000:5000 tda-app
    ```
    Aplikace by měla být dostupná na **http://localhost:5000/**.
