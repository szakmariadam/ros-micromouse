# Bevezetés
## Feladat

A feladat egy micromouse jellegű labirintus megoldása Ros noetic segítségével gazeebo szimulációban.

## A feladat részei
- Egy labirintus elkészítése
- Mobil robot elkészítése
- A labirintus feltérképezése
- A labirintus megoldása az optimális útvonallal

# Tartalomjegyzék
1. [Labirintus](#labirintus)
2. [Micromouse robot](#micromouse-robot)
3. [Labirintus feltérképezése](#labirintus-feltérképezése)
4. [Labirintus megoldása](#labirintus-megoldása)
5. [Összefoglalás](#összefoglalás)

# Labirintus
## Felépítés
A labirintus közelítőleg a micromouse szabályai szerint készült el. A felépítése egy cella struktúra, ahol a cellákat falak választhatják el. A cellák mérete és a falak magassága nem követi a verseny szabványát azonban később a robot dimenziói ezekkel arányosan lettek beállítva. A kezdő és végpontok a neégyzet alapterületű labirintus két szemközti sarkában lett elhelyezve. A kész világ továbbá tartalmaz átlós mozgást megengedő szakaszt.
## A gazeebo világ generálása
A szimulációhoz alkalmazott world fájlt egy Python script generálta. A cellák 31 cm oldalhosszú négyzetek, a falak pedig 20 cm magasak.
# Micromouse robot
## Modell
A mobilrobot modelljének a alapja (base_footprint) 10x20x5 cm-es téglatest. Ennek a két oldalán egy-egy kerék (5 cm sugarú és 5 cm magas henger). Ahhoz, hogy a robot ne billenjen előre vagy hátra, az alap téglatest alján két gömb támasztja azt. A robot tetején egy 3x3x3 cm-es doboz modellezi a lidar szenzort.
## Irányítás
A mobilrobot mozgatása és irányítása differenciál hajtással van megoldva. Ehhez a ROS "differential_drive_controller" plugin-ját implementáltuk. Ebből következik, hogy a robotot a cmd_vel topic-ba küldött twist típusú üzenettel lehet irányítani.
## Szenzorok
A feladat megvalósításához a robotba 2 dimenziós Lidar és IMU szenzorokat raktunk. A lidar cálja a közelben lévő falak figyelése. Az IMU a robot orientációjának meghatározására szolgál.
# Labirintus feltérképezése
# Labirintus megoldása
# Összefoglalás