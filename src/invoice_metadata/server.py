import grpc
from concurrent import futures
import psycopg2
from psycopg2 import sql
from . import invoice_pb2
from . import invoice_pb2_grpc

class RechnungService(invoice_pb2_grpc.RechnungServiceServicer):
    def __init__(self):
        # Verbindung zur Postgres-DB herstellen
        self.conn = psycopg2.connect(
            host="localhost",
            database="invoice_db",
            user="admin",
            password="secretpassword"
        )
        self._create_table()

    def _create_table(self):
        """Erstellt die Tabelle, falls sie noch nicht existiert."""
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS invoices (
                    rechnungs_nummer VARCHAR(50) PRIMARY KEY,
                    lieferant VARCHAR(100),
                    betrag DOUBLE PRECISION,
                    waehrung VARCHAR(10),
                    datum DATE,
                    status VARCHAR(20)
                );
            """)
            self.conn.commit()

    def SpeichereMetadaten(self, request, context):
        status_name = invoice_pb2.RechnungsStatus.Name(request.status)
        
        try:
            with self.conn.cursor() as cur:
                # Daten in Postgres speichern (UPSERT: Einfügen oder bei Konflikt aktualisieren)
                cur.execute("""
                    INSERT INTO invoices (rechnungs_nummer, lieferant, betrag, waehrung, datum, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (rechnungs_nummer) DO UPDATE 
                    SET status = EXCLUDED.status;
                """, (
                    request.rechnungs_nummer, 
                    request.lieferant, 
                    request.betrag, 
                    request.waehrung, 
                    request.datum, 
                    status_name
                ))
                self.conn.commit()

            print(f"\n[DB] Rechnung {request.rechnungs_nummer} erfolgreich gespeichert.")
            return invoice_pb2.RechnungResponse(erfolg=True, nachricht="In DB gespeichert")
        
        except Exception as e:
            print(f"[Fehler] DB-Speicherung fehlgeschlagen: {e}")
            return invoice_pb2.RechnungResponse(erfolg=False, nachricht=str(e))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    invoice_pb2_grpc.add_RechnungServiceServicer_to_server(RechnungService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC Server mit Postgres-Anbindung läuft...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()