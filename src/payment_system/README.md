###Payment System (RabbitMQ Consumer)###

Dieses Modul ist für die asynchrone Zahlungsabwicklung verantwortlich. Es entkoppelt den Bezahlvorgang vom Hauptprozess. In Sprint 2 wurde der Worker um eine Datenbank-Anbindung erweitert, um den Zahlungsstatus dauerhaft zu speichern.








##Funktionsweise##

Der Dienst fungiert als "Consumer" für die RabbitMQ-Warteschlange:

Verbindung: Stellt eine Verbindung zum RabbitMQ-Broker her (Port 5672) und gleichzeitig eine Verbindung zur PostgreSQL-Datenbank (Port 5432).

Subscription: Abonniert die Queue zahlungs_auftraege.





##Nachrichtenverarbeitung (Callback)##

Sobald eine Nachricht eintrifft, führt der Worker folgende Schritte aus:

Dekodierung: Empfängt den JSON-String und extrahiert rechnungs_nummer und betrag.

Zahlungssimulation: Simuliert die Kommunikation mit einer Bank/Schnittstelle (time.sleep(1)).

Datenbank-Update (Neu in Sprint 2):

Führt ein SQL-Kommando aus: UPDATE invoices SET status = 'BEZAHLT' WHERE rechnungs_nummer = %s.

Damit wird die Vorarbeit des gRPC-Servers finalisiert.

Logging: Gibt den Erfolg des Datenbank-Updates im Terminal aus.








##Bestätigung (Acknowledgement)##

Success: Bei erfolgreichem DB-Update wird die Nachricht mit basic_ack aus der Queue gelöscht.

Error: Bei Fehlern (z. B. DB nicht erreichbar) sorgt die Fehlerbehandlung dafür, dass die Nachricht nicht verloren geht oder das System blockiert.







##Technische Highlights im Code##

Durable Queue: Die Warteschlange ist als durable=True deklariert. Aufträge überstehen einen Neustart des RabbitMQ-Containers.

Fair Dispatch: prefetch_count=1 sorgt dafür, dass ein Worker nicht überlastet wird, wenn mehrere Zahlungen anstehen.

SQL-Integrität: Nutzt parametrisierte Abfragen, um SQL-Injection zu verhindern und die Konsistenz in der invoice_db zu wahren.