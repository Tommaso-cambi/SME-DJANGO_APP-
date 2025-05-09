# SME Manager - Sistema di Gestione per Piccole e Medie Imprese

## Descrizione
SME Manager è un'applicazione web Django progettata per aiutare le piccole e medie imprese nella gestione quotidiana delle loro operazioni. Il sistema include moduli per la gestione di dipendenti, ordini e finanze, offrendo una soluzione integrata per le esigenze aziendali.

## Requisiti di Sistema
- Python 3.8 o superiore
- pip (gestore pacchetti Python)
- Git

## Installazione e Configurazione

### 1. Clonare il Repository
```bash
git clone https://github.com/your-username/SME-DJANGO_APP-.git
cd SME-DJANGO_APP-/django-app
```

### 2. Creare e Attivare l'Ambiente Virtuale
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installare le Dipendenze
```bash
pip install -r requirements.txt
```

### 4. Configurare il Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Creare un Superuser
```bash
python manage.py createsuperuser
```

### 6. Avviare il Server di Sviluppo
```bash
python manage.py runserver
```

L'applicazione sarà disponibile all'indirizzo: http://127.0.0.1:8000/

## Struttura del Progetto
- `sme_manager/`: Configurazione principale del progetto Django
- `employees/`: Gestione dipendenti
- `orders/`: Gestione ordini
- `finances/`: Gestione finanziaria
- `templates/`: Template HTML
- `static/`: File statici (CSS, JS, immagini)

## Funzionalità Principali
- Gestione dipendenti (anagrafica, contratti, permessi)
- Gestione ordini (creazione, tracciamento, fatturazione)
- Gestione finanziaria (entrate, uscite, report)
- Dashboard amministrativa
- Sistema di autenticazione e autorizzazione

## Dipendenze Principali
- Django 5.1.7
- Pillow 10.1.0 (gestione immagini)
- python-dotenv (gestione variabili d'ambiente)
- django-crispy-forms (form avanzati)
- crispy-bootstrap5 (template Bootstrap 5)

## Funzionalità Future
- Integrazione con sistemi di pagamento online
-  Reportistica avanzata e grafici
-  Sistema di notifiche email
-  App mobile companion
-  Integrazione con software contabili
-  Sistema di backup automatico
  
    

## Riferimenti Utili
- [Documentazione Django](https://docs.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/getting-started/introduction/)
- [Python Virtual Environment](https://docs.python.org/3/library/venv.html)

