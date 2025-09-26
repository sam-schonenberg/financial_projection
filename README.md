# Financial Projection System

Dieses Projekt dient zur **Finanzplanung und Szenarioanalyse** für mein Unternehmen *Schonenberg Developments*.  
Die Software unterstützt bei der Prognose von Umsätzen, Kosten und Liquidität für ein hybrides Geschäftsmodell (**SaaS + individuelle Webprojekte**).

---

## 🎯 Ziel des Projekts
- **Transparenz**: Alle Finanzprognosen basieren auf einem reproduzierbaren Modell.  
- **Flexibilität**: Annahmen (z. B. Kundenzahlen, Marketingkosten, Churn-Rate) können angepasst werden, wodurch sofort neue Szenarien entstehen.  
- **Planungssicherheit**: Darstellung, wie das Unternehmen sich in verschiedenen Situationen entwickeln würde (z. B. konservativ, realistisch, optimistisch).  
- **Investoren- & Bankenrelevanz**: Zeigt, dass die Finanzplanung nicht „Pi mal Daumen“ ist, sondern systematisch und datenbasiert.  

---

## 🛠️ Hauptfunktionen
- **Kundenakquise-Modellierung**  
  Berechnung der Kundenzahlen pro Monat, basierend auf Marketingbudget, CAC (Customer Acquisition Cost) und Churn-Rate.  

- **Umsatzprojektionen**  
  Abbildung der Einnahmen aus SaaS-Abos (Basic, Pro, Enterprise) sowie zusätzlichen Projekten (z. B. Webseiten).  

- **Kostenplanung**  
  Enthält Marketingkosten, Infrastruktur (Server, Domains, Tools), Personalkosten (Freelancer, spätere Mitarbeiter) und weitere Fixkosten.  

- **Liquiditäts- und Rentabilitätsplanung**  
  Monatliche Projektion von Einnahmen, Ausgaben und Cashflow.  

- **Szenarienvergleich**  
  Unterschiedliche Varianten können durchgespielt werden:  
  - **Optimistisch** (schnelles Wachstum, niedriger Churn)  
  - **Realistisch** (konservativere Kundenzahlen, steigende CAC)  
  - **Worst Case** (nur 50 % der geplanten Kunden, trotzdem tragfähig)  

---

## 📂 Projektstruktur
- `src/` → Kernfunktionen (Berechnung von Umsatz, Kosten, Cashflow)  
- `config/` → Parameterdateien (z. B. Preise, Marketingbudgets, Churn-Raten)  
- `main.py` → Startpunkt für Simulationen  
- `realistic_projection.py` → Beispielrechnung mit realistischen Annahmen  
- `requirements.txt` → Abhängigkeiten (Python-Bibliotheken)  

---

## 📊 Beispielergebnisse

Hier eine Projektion der Kundenzahlen im realistischen Szenario:

![Customer Growth Projection](images/customer_projection_chart.png)

- **Blaue Linie** = Gesamtkunden  
- **Orange Linie** = Neue Kunden pro Monat  
- **Grüne Linie** = Kündigungen pro Monat  

Diese Darstellung zeigt anschaulich, dass das Wachstum nicht nur geplant, sondern auf konkreten Annahmen basiert.

---

## 🚀 Warum dieses Projekt wichtig ist
Dieses Tool zeigt, dass meine Finanzplanung:  
- **klar nachvollziehbar** ist,  
- auf **realistischen und flexiblen Annahmen** basiert,  
- und jederzeit **transparent überprüft** werden kann.  

Damit können Berater:innen und Banken nachvollziehen, dass das Geschäftsmodell nicht nur auf Annahmen, sondern auf **dynamischen Berechnungen** aufgebaut ist.

---

## 📎 Hinweis für IHK / Bank
Dieses Repository dient **nicht** dazu, dass Sie den Code im Detail prüfen müssen.  
Wichtig ist: Alle Prognosen wurden **systematisch** erstellt und können bei Bedarf **beliebig angepasst** und neu berechnet werden.  
Die Finanzzahlen im Businessplan stammen direkt aus diesem Modell.
