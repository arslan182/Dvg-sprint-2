##Client - Rechnungs-Orchestrator##

Dieser Dienst fungiert als zentraler Einstiegspunkt für die Verarbeitung von Eingangsrechnungen. Er koordiniert in Sprint 2 die Kommunikation zwischen der persistenten Speicherung (PostgreSQL via gRPC) und dem asynchronen Zahlungssystem (RabbitMQ).






##Aufgaben des Clients##

Datenerfassung: Definiert die Rechnungsdaten (Nummer, Lieferant, Betrag, Währung, Datum).

Synchrone Validierung & Persistenz (gRPC):

Sendet die Metadaten an den InvoiceMetadata-Service.

Dieser Schritt stellt sicher, dass die Rechnung fest in der PostgreSQL-Datenbank gespeichert wurde, bevor weitere Schritte unternommen werden.

Wartet auf die Bestätigung (success=True).

Asynchrone Prozess-Kopplung (RabbitMQ):

Nach erfolgreicher Speicherung triggert der Client den Workflow für das Zahlungssystem.

Der Auftrag wird als JSON-Nachricht in die Queue zahlungs_auftraege gepusht, damit der Payment-Worker diesen unabhängig verarbeiten kann.








##Funktionsweise im Code##

Der Client implementiert das Muster der Service-Orchestrierung:

Protokoll 1: gRPC (Port 50051): Nutzt invoice_pb2_grpc, um die Methode SpeichereMetadaten aufzurufen. Dies garantiert, dass die Datenstruktur exakt den Protobuf-Definitionen entspricht.

Protokoll 2: AMQP/RabbitMQ (Port 5672): Nutzt pika, um eine entkoppelte Nachricht zu senden. Der Client muss nicht wissen, wann oder wie die Zahlung ausgeführt wird – er übergibt lediglich die Verantwortung an den Broker.











##Ablaufschritte im Detail:##

gRPC-Channel öffnen: Aufbau der Verbindung zum Metadaten-Server (localhost:50051).

Daten-Objekt erstellen: Befüllen des RechnungRequest-Pakets (z. B. Nummer: 001, Betrag: 99.99 EUR).

Transaktions-Check: Der Client sendet das Paket. Nur wenn response.erfolg vom Server zurückkommt, wird der nächste Schritt eingeleitet.

RabbitMQ-Verbindung: Authentifizierung am Broker (Standard: user/password).

Queue-Sicherung: Deklaration der Queue zahlungs_auftraege (stellt sicher, dass die Nachricht nicht im Leeren landet).

JSON-Payload: Umwandlung der Rechnungsdaten in ein JSON-Format (für maximale Kompatibilität mit dem Worker).

Dispatch: Veröffentlichung der Nachricht und Schließen der Verbindungen.











##Starten des Clients##

Voraussetzung: Der Docker-Stack (PostgreSQL & RabbitMQ) sowie der invoice_metadata.server müssen aktiv sein.