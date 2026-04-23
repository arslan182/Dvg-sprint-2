import pika
import json
import psycopg2

def update_invoice_status(rechnungs_nummer):
    """Verbindet sich mit der DB und setzt den Status auf BEZAHLT."""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="invoice_db",
            user="admin",
            password="secretpassword"
        )
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE invoices SET status = 'BEZAHLT' WHERE rechnungs_nummer = %s",
                (rechnungs_nummer,)
            )
            conn.commit()
        conn.close()
        print(f"   [DB-Update] Status für {rechnungs_nummer} auf 'BEZAHLT' gesetzt.")
    except Exception as e:
        print(f"   [DB-Fehler] Konnte Status nicht aktualisieren: {e}")

def callback(ch, method, properties, body):
    data = json.loads(body)
    r_nr = data.get("rechnungsnummer")
    
    print(f" [x] Empfangen: Rechnung {r_nr}")
    
    # JETZT NEU: Status in der Datenbank ändern
    update_invoice_status(r_nr)
    
    # Bestätigung an RabbitMQ (Nachricht wird aus der Queue gelöscht)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost',
        credentials=pika.PlainCredentials('user', 'password')
    ))
    channel = connection.channel()
    channel.queue_declare(queue='zahlungs_auftraege', durable=True)

    channel.basic_consume(queue='zahlungs_auftraege', on_message_callback=callback)

    print(' [*] Payment-Worker wartet auf Nachrichten. Drücke STRG+C zum Beenden.')
    channel.start_consuming()

if __name__ == "__main__":
    start_worker()