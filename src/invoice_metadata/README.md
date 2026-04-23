###Metadata Service (gRPC Server)###

Dieser Dienst ist der zentrale Ankerpunkt für die Datenintegrität des Systems. Er stellt einen gRPC-Endpunkt bereit, der strukturierte Rechnungsdaten empfängt, validiert und dauerhaft in einer relationalen Datenbank speichert.








Robustheit: Daten bleiben auch nach einem Neustart des Containers oder des Servers erhalten.

Status-Management: Der Server setzt den Initialstatus (OFFEN), welcher später vom Payment-Worker aktualisiert wird.







##Projektstruktur & Dateien##

invoice.proto: Die Schnittstellendefinition (IDL). Sie erzwingt die Struktur der Daten (Nummer, Betrag, Währung etc.).

server.py: Kernlogik des Servers inklusive der SQL-Befehle zur Datenbank-Kommunikation.

invoice_pb2.py / invoice_pb2_grpc.py: Die aus der Proto-Datei generierten Python-Klassen.









##Funktionsweise##

Wenn der Client Daten an den Server sendet, durchlaufen diese folgende Kette:

Connection-Init: Beim Start verbindet sich der Server via psycopg2 mit der PostgreSQL-Instanz (localhost:5432).

Validierung: gRPC prüft die Typsicherheit der eingehenden Nachricht (Protobuf-Standard).

SQL-Persistenz: Der Server führt ein INSERT INTO invoices aus. Dabei werden die Daten aus dem gRPC-Request in SQL-Datentypen übersetzt.

Logging: Erfolgreiche Datenbank-Transaktionen werden im Terminal bestätigt.

Antwort: Nach erfolgreichem Datenbank-Commit sendet der Server erfolg=True an den Client zurück.









###Technische Details##

Port: 50051 (gRPC)

Datenbank: PostgreSQL 15+ (läuft im Docker-Container postgres_db)

Datenbank-Treiber: psycopg2-binary

Tabellen-Schema:

rechnungs_nummer (Primary Key)

lieferant, betrag, waehrung, datum

status (Default: OFFEN)







##Starten des Servers##
Stellen Sie sicher, dass der Docker-Stack gestartet ist, bevor Sie den Server ausführen.