# SupermarktConnector
Een Python project voor het ophalen van data vanuit de Albert Heijn en Jumbo

## Albert Heijn
Voor de AH word gebruikt gemaakt van een achterliggende REST-API die ik gevonden heb tijdens het analyzeren van de android app. Deze REST-API heeft wel verschillende veiligheidsmechanisme's ingebouwd om gebruik van derde te voorkomen.

```ms.ah.nl/rest/ah/```

### Basic authentication
Voor gebruik moet er eerst een wachtwoord aangevraagd worden, dit wachtwoord kan dan gebruikt worden om gegevens zoals gebruikersnaam te verkrijgen. Bij alle requests moet dit wachtwoord en gebruikersnaam meegestuurd worden. 
Ook moet er een gehashte Base64 authenticatie meegestuurd worden.

### X-digest
De X-digest is een gehashte waarde door middel van SHA1 die gebruikt word om te controleren of de gegenereerde X-Digest ook daadwerkelijk bij de gevraagde url met parameters hoort. Deze word gemaakt met de data:

URL MET PARAMETERS, Gebruikersnaam, de gegeven body (maximaal 1000 bytes), de geheime digest code die in de android app verwerkt is.

Dit mechanisme heb ik nagemaakt waardoor er exact dezelfde hash uitkomt.

## Jumbo Supermarkten
Voor de Jumbo maak ik ook gebruik van de achterliggende REST-API die uit de android app komt. Er word niet gebruikt gemaakt van een speciale veiligheidsmechanisme. Wel word er een X-jumbo-token gebruikt, dit is alleen van toepassing als je de prijs van een speciale winkel wil zien of een winkelmandje wil samenstellen.

Deze X-jumbo-token heb ik geimplementeerd zodat je kan switchen tussen lokale winkels. Tijdens het experimenteren kwam ik er namelijk achter dat alle jumbo winkels een bepaalde categorie bezitten van J1-J5

```mobileapi.jumbo.com```
