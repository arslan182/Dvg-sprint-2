#!/usr/bin/env python3
r"""
Event Log Generator - STANDALONE VERSION
Funktioniert auch wenn Python PATH kaputt ist!

Einfach mit dem funktionierenden venv ausführen:
C:\Users\aliar\workspace\python\fastapi\.venv\Scripts\python.exe .\generate_event_log_standalone.py
"""

import csv
import os
from datetime import datetime, timedelta
import random

# ============ KONFIGURATION ============
NUM_INVOICES = 50
OUTPUT_DIR = r"C:\Users\aliar\workspace\Dvg\Dvg-sprint-2\analysis\data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "event_log.csv")

ACTIVITIES = [
    "Rechnung empfangen (Client → gRPC)",
    "Validierung durchgeführt",
    "Metadaten gespeichert (gRPC → DB)",
    "Payment Request in Queue (gRPC → RabbitMQ)",
    "Payment Request enqueued",
    "Payment Worker startet",
    "Zahlung verarbeitet",
    "Zahlung abgeschlossen",
    "Log geschrieben",
    "Fehler: Validierung fehlgeschlagen",
    "Fehler: Payment fehlgeschlagen",
    "Retry: Payment versuchen",
    "Notification gesendet"
]

# ============ FUNKTIONEN ============

def generate_events_for_invoice(case_id, start_time):
    """Generiert Events für eine Rechnung"""
    events = []
    current_time = start_time
    variant = random.choices(['normal', 'error_retry', 'slow'], weights=[60, 20, 20], k=1)[0]
    
    # Event 1
    events.append({
        'Case_ID': case_id,
        'Activity': ACTIVITIES[0],
        'Timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'Variant': variant,
        'Status': 'completed'
    })
    current_time += timedelta(milliseconds=random.randint(10, 100))
    
    # Event 2
    events.append({
        'Case_ID': case_id,
        'Activity': ACTIVITIES[1],
        'Timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'Variant': variant,
        'Status': 'completed'
    })
    
    # Fehler-Variante
    if variant == 'error_retry' and random.random() < 0.5:
        current_time += timedelta(milliseconds=random.randint(50, 150))
        events.append({
            'Case_ID': case_id,
            'Activity': ACTIVITIES[9],
            'Timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
            'Variant': variant,
            'Status': 'error'
        })
        current_time += timedelta(milliseconds=random.randint(100, 500))
        events.append({
            'Case_ID': case_id,
            'Activity': ACTIVITIES[1],
            'Timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
            'Variant': variant,
            'Status': 'retry'
        })
    
    current_time += timedelta(milliseconds=random.randint(50, 150))
    
    # Event 3
    events.append({
        'Case_ID': case_id,
        'Activity': ACTIVITIES[2],
        'Timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'Variant': variant,
        'Status': 'completed'
    })
    current_time += timedelta(milliseconds=random.randint(50, 200))
    
    # Event 4
    events.append({
        'Case_ID': case_id,
        'Activity': ACTIVITIES[3],
        'Timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'Variant': variant,
        'Status': 'completed'
    })
    current_time += timedelta(milliseconds=random.randint(10, 50))
    
    # Event 5
    events.append({
        'Case_ID': case_id,
        'Activity': ACTIVITIES[4],
        'Timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'Variant': variant,
        'Status': 'completed'
    })
    
    # Queue wait
    if variant == 'slow':
        queue_wait = random.randint(3000, 8000)
    else:
        queue_wait = random.randint(200, 1000)
    
    current_time += timedelta(milliseconds=queue_wait)
    
    # Event 6
    events.append({
        'Case_ID': case_id,
        'Activity': ACTIVITIES[5],
        'Timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'Variant': variant,
        'Status': 'started'
    })
    current_time += timedelta(milliseconds=random.randint(100, 500))
    
    # Event 7
    events.append({
        'Case_ID': case_id,
        'Activity': ACTIVITIES[6],
        'Timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'Variant': variant,
        'Status': 'processing'
    })
    current_time += timedelta(seconds=random.randint(4, 6))
    
    # Fehler bei Payment
    if variant == 'error_retry' and random.random() < 0.5:
        events.append({
            'Case_ID': case_id,
            'Activity': ACTIVITIES[10],
            'Timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
            'Variant': variant,
            'Status': 'error'
        })
        current_time += timedelta(seconds=random.randint(2, 5))
        events.append({
            'Case_ID': case_id,
            'Activity': ACTIVITIES[11],
            'Timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
            'Variant': variant,
            'Status': 'retry'
        })
        current_time += timedelta(seconds=random.randint(4, 6))
    
    # Event 8
    events.append({
        'Case_ID': case_id,
        'Activity': ACTIVITIES[7],
        'Timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'Variant': variant,
        'Status': 'completed'
    })
    current_time += timedelta(milliseconds=random.randint(50, 200))
    
    # Event 9
    events.append({
        'Case_ID': case_id,
        'Activity': ACTIVITIES[8],
        'Timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'Variant': variant,
        'Status': 'completed'
    })
    current_time += timedelta(milliseconds=random.randint(10, 100))
    
    # Event 10
    events.append({
        'Case_ID': case_id,
        'Activity': ACTIVITIES[12],
        'Timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'Variant': variant,
        'Status': 'completed'
    })
    
    return events


def main():
    """Hauptfunktion"""
    
    # Check Ordner
    if not os.path.exists(OUTPUT_DIR):
        print(f"❌ Ordner existiert nicht: {OUTPUT_DIR}")
        return False
    
    print(f"📊 Generiere Event Log mit {NUM_INVOICES} Rechnungen...")
    print(f"📁 Output-Ordner: {OUTPUT_DIR}")
    
    all_events = []
    start_date = datetime(2026, 4, 20, 8, 0, 0)
    
    # Generiere alle Events
    for i in range(NUM_INVOICES):
        case_id = f"R-{100 + i}"
        time_offset = random.randint(0, 3600)
        invoice_start_time = start_date + timedelta(seconds=time_offset)
        
        invoice_events = generate_events_for_invoice(case_id, invoice_start_time)
        all_events.extend(invoice_events)
    
    # Schreibe CSV
    print(f"✍️  Schreibe {len(all_events)} Events...")
    
    try:
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['Case_ID', 'Activity', 'Timestamp', 'Variant', 'Status']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_events)
        
        print(f"\n✅ Event Log erfolgreich erstellt!")
        print(f"\n📈 Statistik:")
        print(f"  - Gesamtanzahl Events: {len(all_events)}")
        print(f"  - Gesamtanzahl Fälle: {NUM_INVOICES}")
        print(f"  - Events pro Fall: {len(all_events) // NUM_INVOICES}")
        print(f"  - Dateiname: event_log.csv")
        print(f"  - Vollständiger Pfad: {OUTPUT_FILE}")
        print(f"\n🎯 Nächster Schritt:")
        print(f"  1. Überprüfe: {OUTPUT_FILE}")
        print(f"  2. Lade in Celonis hoch")
        print(f"  3. Process Mining durchführen")
        return True
    
    except Exception as e:
        print(f"\n❌ Fehler beim Schreiben: {e}")
        return False


if __name__ == "__main__":
    main()