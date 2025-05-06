# SME Manager

Un'applicazione Django per la gestione delle piccole e medie imprese.

## Funzionalità

L'applicazione include i seguenti moduli:

1. **Gestione Dipendenti**
   - Anagrafica dipendenti
   - Gestione dipartimenti e posizioni
   - Rilevazione presenze
   - Gestione ferie e permessi

2. **Gestione Finanziaria**
   - Registrazione entrate e uscite
   - Gestione conti e categorie
   - Pianificazione budget

3. **Gestione Ordini**
   - Ordini clienti
   - Ordini fornitori
   - Gestione prodotti e inventario
   - Anagrafica clienti e fornitori

## Requisiti

- Python 3.8+
- Django 5.1+

## Installazione

2. Installa le dipendenze:
   ```
   pip install -r requirements.txt
   ```

3. Esegui le migrazioni del database:
   ```
   python manage.py migrate
   ```

4. Crea un superuser:
   ```
   python manage.py createsuperuser
   ```

5. Avvia il server di sviluppo:
   ```
   python manage.py runserver
   ```

6. Accedi all'applicazione nel browser all'indirizzo http://127.0.0.1:8000/

## Struttura del Progetto

- `employees`: Gestione dipendenti, dipartimenti e presenze
- `finances`: Gestione entrate/uscite e conti
- `orders`: Gestione ordini, prodotti, clienti e fornitori

## Licenza

MIT
