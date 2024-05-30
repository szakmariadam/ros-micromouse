[image1]: ./assets/maze.jpg "maze"
[image2]: ./assets/robot_model.jpg "robot_model"

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
### Az elkészült labirintus:
![image1]
# Micromouse robot
## Modell
A mobilrobot modelljének a alapja (base_footprint) 10x20x5 cm-es téglatest. Ennek a két oldalán egy-egy kerék (5 cm sugarú és 5 cm magas henger). Ahhoz, hogy a robot ne billenjen előre vagy hátra, az alap téglatest alján két gömb támasztja azt. A robot tetején egy 3x3x3 cm-es doboz modellezi a lidar szenzort.
### A robot modellje:
![image2]
## Irányítás
A mobilrobot mozgatása és irányítása differenciál hajtással van megoldva. Ehhez a ROS "differential_drive_controller" plugin-ját implementáltuk. Ebből következik, hogy a robotot a cmd_vel topic-ba küldött twist típusú üzenettel lehet irányítani.
## Szenzorok
A feladat megvalósításához a robotba 2 dimenziós Lidar és IMU szenzorokat raktunk. A lidar cálja a közelben lévő falak figyelése. Az IMU a robot orientációjának meghatározására szolgál.
# Labirintus feltérképezése
Ahhoz, hogy a meg lehessen oldani a labirintust, azt először fel kellett térképezni. Ehhez a micromouse robot körbe megy a labirintusban és egy mátrixba lejegyzi a falak és utak helyét.
## Körbevezetés
Ha a robot a bal oldali falat követi végig, akkor egyszer körbe fog érni a labirintuson úgy, hogy mindenhol járt. Ez volt az alap ötlet a körbevezetés megvalósításakor. Ezt a folyamatot egy python script kezeli. A mozgatáshoz koordináták (waypointok) vannak megadva, amik az adott célpontot jelzik. Ezek a célok az éppen soron következő cella koordinátái lesznek. Ahhoz, hogy elérjük ezeket a waypointokat a robot orientációja és pozíciója folyamatosan monitororzva van. A cél waypoint és a robot állása közötti szöghibát kiszámolja a program és twist üzenettel addig van forgatva ameddig ez a hiba egy elfogadható tartományon belülre nem kerül. Hasonló a helyzet a waypointtól vett távolsággal is. Miután irányban van a robot, addig megy előre amíg el nem éri kellően kis hibával a kívánt koordinátákat. A cellában a lidar felméri a körülötte lévő falakat és ez alapján a ki lehet számolni a következő waypointot. Ezt addig ismétli a program ameddig vissza nem ért a kiinduló pontra.
## Térkép készítés
A térkép egy mátrix amiben fel vannak tüntetve a cellák és a cellák közötti falak. Amikor a robot egy új cellába lép megnézi a lidar segítségével a körülötte lévő cellákat és ha falat lát akkor a mátrix megfelelő helyére feljegyzi azt. Ha nem falat lát hanem utat azt is feljegyzi. Külön szimbólum jelzi a mátrixban a falat a cellát és a cellák közötti szabad utat. 
### Az így elkészített térképmátrix:
# Labirintus megoldása
A labirintus megoldása hasonlóan működik mint a körbevezetés, csak itt előre ki vannak számolva a waypointok, amik kijelölik az optimális útvonalat.
## Útvonal kiszámítása
A korábban elkészült térképmátrix segítségével számoltuk ki a leggyorsabb útvonalat. Ezen a mátrixon flood fill algoritmust alkalmazva megkaptuk, hogy az egyes cellák hány lépésnyire vannak a céltól. Ezek alapján a mindegyik pozícióból el lehet dönteni, hogy melyik a leggyorsabb irány. Ezt az irányt követve kijött az optimális útvonal, amiből ki lettek számolva a waypointok és azok koordinátái.
### A flood fill algoritmus eredménye:
# Eredmények