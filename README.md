###DVG-2 - Digitalisierung eines Geschäftsprozesses###
Projekt im Rahmen des Moduls "Digitalisierung von Geschäftsprozessen" – Hochschule Karlsruhe







##Projektbeschreibung##

Dieses Projekt demonstriert die Digitalisierung der Eingangsrechnungsverarbeitung eines mittelständischen Unternehmens. Ziel ist der Aufbau einer stabilen Microservice-Architektur, die Rechnungen sicher speichert und asynchron bezahlt.

In Sprint 2 wurde das System von einer flüchtigen In-Memory-Lösung auf eine persistente PostgreSQL-Datenbank umgestellt.





##Projektstruktur##

DVG-2/
├── extras/
│   └── backend/             # Docker Compose: Infrastruktur (Postgres & RabbitMQ)
├── src/
│   ├── client/              # Orchestrator: Initiiert gRPC-Call & RabbitMQ-Nachricht
│   ├── invoice_metadata/    # gRPC Server: Speichert Metadaten in PostgreSQL
│   ├── payment_system/      # Worker: Verarbeitet Zahlungen & aktualisiert DB-Status
│   └── proto/            # Docker Compose: Infrastruktur (Postgres & RabbitMQ)
├── .gitignore               # Git Ausnahmen
├── requirements.txt         # Python Abhängigkeiten (inkl. psycopg2)
└── README.md                # Diese Projektdokumentation








##Technologien##

gRPC: Performante, synchrone Kommunikation zwischen Client und Metadaten-Service.

PostgreSQL: Relationale Datenbank zur dauerhaften Speicherung der Rechnungsdaten.

RabbitMQ: Message Broker für die entkoppelte, asynchrone Zahlungsabwicklung.

Protobuf: Typsichere Serialisierung der Nachrichten.

Docker: Containerisierung der Infrastruktur (Datenbank & Broker).






##Voraussetzungen##

Python 3.13

Docker & Docker Compose






##Der Prozess-Flow in Sprint 2##

Client sendet Metadaten via gRPC an den Server.

Server speichert die Rechnung mit Status OFFEN in PostgreSQL.

Client erhält "OK" und sendet Zahlungsauftrag an RabbitMQ.

Payment-Worker empfängt Nachricht, wartet 1 Sekunde und setzt den Status in PostgreSQL auf BEZAHLT.






##Monitoring & Debugging##

Datenbank prüfen:
docker exec -it postgres_db psql -U admin -d invoice_db -c "SELECT * FROM invoices;"

RabbitMQ Management UI:
http://localhost:15672 | Login: user / password