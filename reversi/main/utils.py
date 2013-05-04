
import random


def random_game_name():
    return "Schlacht um " + STAR_TREK_PLANETS[random.randint(0, len(STAR_TREK_PLANETS))]


STAR_TREK_PLANETS = """
Alpha III
Alpha Carinae II
Alpha Carinae V
Alpha Cygnus IX
Alpha Eridani II
Alpha Laputa IV
Alpha Leonis system
Alpha Majoris I
Alpha Omicron VII
Alpha Onias III
Alpha Proxima II
Alpha V
Alpha-441
Alsaurian
Altair III
Altair IV
Altair VI
Althos IV
Alture VII
Amargosa
Amerind
Amleth Prime
Andevian II
Andoria
Andros III
Angel I
Angosia III
Antede III
Antica
Antos IV
AR-558
Archanis IV
Archer IV
Archer's Comet
Archer's Planet
Arcturus IV
Ardana
Argana II
Argelius II
Argratha
Argus X
Ariannus
Arkaria
Arloff IX
Armus IX
Arret
Arvada III
Aschelan V
Astral V
Atalia VII
Atbar Prime
Athos IV
Atifs IV
Atlec
Atrea IV
'Aucdet IX
Aurelia
Avenal VII
Avery III
Axanar
B'Saari II
Ba'ku
Babel
Bajor
Bajor VIII
Balancar
Balosnee VI
Banean
Barisa Prime
Barkon IV
Barradas III
Barson II
Barzan
Beltane IX
Benecia Colony
Benthos
Benzar
Berengaria VII
Bersallis III
Beta III
Beta VI
Beta XII-A
Beta Agni II
Beta Antares IV
Beta Aurigae
Beta Aquilae II
Beta Cassius
Beta Kupsic
Beta Niobe I
Beta Stromgren
Beta Ursae Minoris II
Betazed
Betelgeuse II
Beth Delta I
Bilana III
Bilaren
Blue Horizon
Bolarus IX
Bopak III
Boraal II
Boradis III
Boreal III
Boreth
Borg Prime
Borka VI
Boslic
Bracas V
Braslota
Brax
Brechtian cluster
Bre'el IV
Breen
Brekka
Brentalia
Brinda V
Bringloid V
Browder IV
Brunali
Bryma
Bynaus
Caere
Cairn
Cait
Calder II
Caldik Prime
Caldonia
Caldos II
Caleb IV
Callinon VII
Calondia IV
Camor V
Campor III
Camus II
Capella IV
Cardassia III
Cardassia IV
Cardassia V
Cardassia Prime
Carema III
Carnel
Carraya IV
Casperia Prime
Castal I
Catulla
Celtris III
Centauri VII
Cerberus II
Cestus III
Ceti Alpha V
Ceti Alpha VI
Chalna
Chaltok IV
Chandra V
Chaya VII
Cheron
Chrysalian
Cirrus IV
Coltar IV
Cor Caroli V
Coridan
Corinth IV
Corvan II
Cravic
Cygnet XIV
Cygnia Minor
Dakala
Daled IV
Danula II
Daran V
Davlos Prime
Dayos IV
Decos Prime
Dedestris
Deinonychus VII
Dekendi III
Delb II
Delinia II
Delios VII
Delos III
Delos IV
Delphi Ardu IV
Delta IV
Delta Vega
Delvos Prime
Deneb II
Deneb IV
Deneb V
Deneva
Denobula
Deriben V
Dessica II
Detria
Devidia II
Devos II
Dimorus
Dinaal
Donatu V
Doraf I
Dorvan V
Dosi
Dozaria
Draken IV
Drayan II
Draygo IV
Draylax
Draylon II
Drema IV
Dreon VII
Dulisian IV
Durenia IV
Duronom
Dytallix B
Earth
Earth Colony 2
Eden
Efros
Ekos
Elas
El-Adrel IV
El-Auria
Elanu IV
Elaysian
Elba II
Ellora
Emila II
Eminiar VII
Enara Prime
Endicor
Epsilon 119
Epsilon IV
Epsilon Canaris III
Epsilon Eridani
Epsilon Indi II
Epsilon West IV
Erabus Prime
Errikang VII
Evadne IV
Evora
Excalbia
Exo III
Fabrina
Fahleena III
Farius Prime
Faynos
Felton Prime
Fendaus V
Ferenginar
Fina Prime
Finnea Prime
Feris VI
Flaxian
Folnar III
Forcas III
Forlat III
Fornax
Founders'
Freehaven
Gagarin IV
Gaia
Galador II
Galdonterre
Galen IV
Gallos II
Galor IV
Galorda Prime
Galorndon Core
Galvin V
Gamelan V
Gamma 400
Gamma II
Gamma VII-A
Gamma Canaris IV
Gamma Canaris N
Gamma Hromi II
Gamma Hydra II
Gamma Hydra IV
Gamma Tauri IV
Gamma Trianguli VI
Gamma Vertis IV
Ganalda IV
Garadius IV
Garenor
Garon II
Gaspar VII
Gault
Gedi Prime
Gema IV
Gemaris V
Gemulon V
Genesis Planet
Ghorusda
Gideon
Golana
Gonal IV
Gorlan
Gorn
Gothos
Gramilia
Gravesworld
Grazer
H'atoria
Ha'Dara
Hakton VII
Haakon
Halana
Halee
Halii
Halka
Hanoli
Hanon IV
Hanoran II
Hansen's Planet
Harrakis V
Harrod IV
Haven
Hayashi
Hekaras II
Hell
Hemikek IV
Heva VII
Hoek IV
Holberg 917-G
Holna IV
Hottar II
Hupyria
Hurada III
Hurkos III
Iadora Colony
Icarus Prime
Iconia
Icor IX
Idran
Ilari
Ilecom system
Ilidaria
Illyria
Inavar Prime
Indri VIII
Inferna Prime
Ingraham B
Invernia II
Iota Geminorum IV
Iraatan V
Irtok
Isis III
Itamish III
Ivor Prime
Iyaar
Izar
Janus VI
Japori II
Jaros II
Jerido
Jouret IV
Juhraya
Jupiter
Kabrel I
Kabrel II
Kaelon II
Kaldra IV
Kalla III
Kanda IV
Kantare
Kar-telos
Karemma
Kataan
Katarrea VII
Kavaria
Kavis Alpha IV
Kazlati
Kelemane's Planet
Kelis'
Kelton IV
Kelva
Kelvas V
Kenda II
Kentanna
Kesat
Kesprytt III
Kessik IV
Keto-Enol
Khitomer (QI'tomer in Klingon)
Khosla II
Kiberia
Klaestron IV
Klavdia III
Klendeth
Koinonian
Kolandra
Kolarus III
Koltair IV
Kora II
Koralis III
Korat
Korma
Korridon
Korris I
Kostolain
Kotara Barath
Kotati
Kraus IV
Kronos
Kreetassa
Kressari
Krios
Ktaria VII
Ktaris
Kurill Prime
Kurl
Kyana Prime
Kylata II
Kyria
L374
L-S VI
Landris II
Lappa IV
Largo V
Laurentian System
Lazon II
Ledonia III
Ledos
Legara IV
Lemma II
Lerishi IV
Levinius V
Ligillium
Ligobis X
Ligon II
Ligos VII
Lima-Sierra III
Lissepia
Loque'eque
Loracus Prime
Loren III
Lorillian
Loval
Luria
Lya III
Lya IV
Lyshan
Lysia
M-113
M'kemas III
M-S-1
M-Zed V
Mab-Bu VI
Machine planet
Magna Roma
Magus III
Makus III
Malaya IV
Malcor III
Malindi VII
Malkus IX
Malon Prime
Malona IV
Malur
Manu III
Manzar colony
Maranga IV
Marcos XII
Marcus II
Marejaretus VI
Mari
Mariah IV
Marijne VII
Mariposa
Marlonia
Mars (Sol IV)
Marva IV
Matalas
Mataline II
Mavala IV
Maxia Zeta
Mazar
Meezan IV
Meldrar I
Meles II
Melina II
Melnos IV
Memory Alpha
Memory Delta
Memory Gamma
Merak II
Merik III
Mercury
Meridian
Midos V
Milika III
Minara II
Minnobia
Minos
Minos Korva
Minshara
Mintaka III
Miri
Miridian VI
Mislen
Mithren
Mizar II
Moab IV
Modean
Monac IV
Monea
Mordan IV
Morikin VII
Morska
Moselina system
Mudd
Mudor V
Mundahla
Myrmidon
Nagor
Nahmi IV
Nanibia Prime
Napinne
Narendra III
Nasreldine
Nausicaa
Nechani
Nehru colony
Nel III
Nel Bato
Nelvana III
Nervala IV
Nessik
Neubilia Prime
Neural
New Bajor
New Berlin
New Brooklyn IX
New Earth
New France colony
New Gaul
New Halana
New Sydney
Nibia
Nigala IV
Nimbus III
Ninipia Prime
Nivoch
Norcadia Prime
Norellus
Norkan
Norpin V
Nova Kron
Nyria III
O'Ryan's Planet
Oby VI
Ocampa
Oceanus IV
Ogat
Ogus II
Ohniaka III
Omega Cygni
Omega IV
Omekla III
Omicron IV
Omicron Ceti III
Omicron Delta
Omicron Pascal
Omicron Theta
Ophiuchus III
Oran'taku
Orelious IX
Orendal V
Organia
Orias III
Orion
Orion I
Orion III
Ornara
Oshionion Prime
Otar II
Paan Mokar
Pacifica
Palamar
Panora
Paraagan
Parada II
Parada IV
Parliament
Parsion III
Parvenium system
Paxsor III
Pegos Minor
Peliar Zel
Pellius V
Pendari
Pentarus
Pentath III
Penthara IV
Pernaia Prime
Persephone V
P'Jem
Planet Q
Planet X
Platonius
Pluto
Polaric Ion Planet
Pollux IV
Porakas IV
Portas V
Prakal II
Pralor
Praxillus
Praxis
Preenos
Prema II
Procyon V
Prometheus
Prophet's Landing
Psi Upsilon III and IV
Psi 2000
Pullock V
Purser's Planet
Pyris VII
Pythro V
Qo'noS
Qomar
Quadra Sigma III
Qualor II
Quarra
Quatal Prime
Quazulu VIII
Quinor VII
Rachelis
Rahm-Izad
Rakal
Rakella Prime
Rakhar
Rakosa V
Ramatis III
Ram Izad
Ramura
Rana IV
Ranza V
Regula
Regulak IV
Regulus
Reina VI
Rekag-Seronia
Relva VII
Remmil VI
Remus
Rha'darus
Rhaandaran
Rhymus Major
Rigel II
Rigel III
Rigel IV
Rigel V
Rigel VII
Rigel X
Rigel XII
Rinax
Risa
Rivos V
Rochanie III
Romulus
Ronara Prime
Rondac III
Rousseau V
Ruah IV
Rubicun III
Runara IV
Rura Penthe
Rutia IV
Sakari
Sakura Prime
Saltok IV
Salva II
Samrin's Planet
Sarona VIII
Sarpeidon
Sarpedion V
Sarthong V
Saturn
Sauria
Scalos
Secarus IV
Sefalla Prime
Selay
Selek IV
Selenia Prime
Sentinel Minor IV
Septimis Minor
Septimus III
Seros
Setlik III
Sha Ka Ree
Shantil III
Shelia
Sherman's Planet
Sheva II
Shiralea VI
Sigma Draconis
Sigma Erani
Sigma Iota II
Sikaris
Simperia
Sirrie IV
Skagaran colony
Sobras
Solais V
Solarion IV
Solosos III
Son'a Prime
Sothis III
Soukara
Spica
Stameris
Starbase 6
Starbase 11
Starbase 12
Starbase 73
Starbase 123
Starbase 133
Starbase 152
Starbase 153
Starbase 234
Starbase 515
Starbase Earhart
Starbase Montgomery
Star Station India
Straleb
Styris IV
Suliban
Sulvin IV
Sumiko IV
Surata IV
T'Khasi
T'Khut
T'Lani III
T'Lani Prime
T'lli Beta
T-Rogoran
Tagra IV
Tagus III
Takar II
Takara
Talarian
Talax
Tallonian
Talos IV
Tamar
Tandar Prime
Tantalus
Tanuga IV
Taranko colony
Taresia
Tarakis
Tarchannen III
Tarellia
Taresia
Tarkalea
Tarlac
Tarod IX
Tarok
Tarquin's Planet
Tarsus III
Tarsus IV
Tartarus V
Tau Alpha C
Tau Ceti Prime
Tau Ceti III
Tau Ceti IV
Tau Cygna V
Taurus II
Taurus III
Taurus Ceti IV
Tavela Minor
Teerza Prime
Telemarius IV
Tellar Prime
Telsius
Teluridian IV
Tendara colony
Teplan system
Terlina III
Terosa Prime
Terra Nova
Terrellian
Tessen III
Tessik Prime
Tethys III
Thalos IV
Thalos VII
Thanatos VII
Thasus
Thelka IV
Thera
Theta 116 VIII
Theta VII
Theta Cygni XII
Theta Kiokis II
Theta Omicron IV
Tholia
Thurasia
Ti'Acor
Tiburon
Tilonus IV
Time Planet
Timor II
Titan
Titus IV
Tohvun III
Torad V
Toranius Prime
Torga IV
Torman V
Torna IV
Torona IV
Toroth
Torros III
Tracken II
Tranome Sar
Trebus
Trelka V
Trelkis III
Triacus
Trialas IV
Triannon
Trill
Triona
Triskelion
Troyius
Turkana IV
Tycho IV
Tyree
Tyrellia
Tyrus VII-A
Tzenketh
Udala Prime
Ufandi III
Ullian
Ultima Thule
Umoth VIII
Unefra III
Uxal
Vaadwaur
Vacca VI
Vadris III
Vagra II
Valo II
Valo III
Valt Minor
Vanden Prime
Vandor IV
Vandros IV
Varala
Vega IX
Vega Reticuli
Velara III
Velos VII
Veloz Prime
Vendikar
Ventani II
Ventax II
Venus
Verex III
Veridian III
Veridian IV
Vico V
Vilmoran II
Vissia
Volan II
Volan III
Volchok Prime
Vulcan
Wadi
Wolf 359
Wolf 424
Wrigley's Pleasure Planet
Wysanti
Xanthan
Xanthras III
Xantoras
Xendi Sabu
Xendi Starbase 9
Xerxes VII
Xindi Council Planet
Xindus
Yadalla Prime
Yadera Prime
Yadera II
Yalidian
Yalosian
Yonada
Yridian
Zadar IV
Zahl
Zakdorn
Zalkon
Zaran II
Zayra IV
Zed Lapis
Zeon
Zeta Alpha II
Zeta Boetis III
Zetar
Zibalia
Zytchin III
""".split("\n")
