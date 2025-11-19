Quake 1 Multiplayer Setup på Mac (M1) med Docker

Översikt

Denna guide dokumenterar hela processen för att få Quake 1 multiplayer att fungera på en Mac M1 med Docker. Den innehåller alla steg, felsökningar och lösningar vi gick igenom. Guiden täcker både server och klient.

⸻

1. Miljö och krav
	•	OS: macOS (M1)
	•	Docker & Docker Compose installerat
	•	Quake 1 pak-filer: pak0.pak och pak1.pak
	•	Klient: DarkPlaces 3504 (Mac build)
	•	Server image: moisesber/quaken:latest (Docker)
	•	Ports: 26000 UDP (Quake), 51820 UDP (WireGuard om VPN används)

2. Problem och felsökning

2.1 Klientproblem med Host_Error
	•	Symptom:
Klienten (VkQuake) fick felmeddelande:
Host_Error: Server returned version 3504, not 15 or 666 or 999.
Unknown command "cl_serverextension_download"

	•	Lösning:
Klienten och servern måste ha samma version. Vi bytte klient till DarkPlaces desktop build för Mac (version 3504).

⸻

2.2 DarkPlaces kunde inte hitta filer
	•	Symptom:
W_LoadWadFile: couldn't load gfx.wad
Check that this has an id1 subdirectory containing pak0.pak and pak1.pak
	•	Åtgärder:
	1.	Skapa en mappstruktur:
    ~/Documents/Quake/id1/pak0.pak
    ~/Documents/Quake/id1/pak1.pak

2.	Starta DarkPlaces med basdir:
~/Documents/DarkPlaces.app/Contents/MacOS/darkplaces-sdl -basedir ~/Documents/Quake

2.3 Docker-compose problem på M1
	•	Symptom:
    The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8)

	•	Lösning:
Lägg till platform: linux/amd64 i serversektionen i docker-compose.yml för kompatibilitet med M1.

2.4 Inga konfigurationsfiler hittades
	•	Symptom:
no configuration file provided: not found

	•	Åtgärd:
Navigera till rätt katalog där docker-compose.yml finns och kör:
docker-compose -f ./docker-compose.yml up -d

3. Server Setup

3.1 Docker-compose fil
services:
  quake_server:
    image: moisesber/quaken:latest
    container_name: quake_server
    platform: linux/amd64
    ports:
      - "26000:26000/udp"
    volumes:
      - ./quake_data:/nquakesv/id1
      - ./quake_data/maps:/nquakesv/modules
    environment:
      - GAME_DIR=id1
      - CONFIG_FILE=server.cfg
    restart: unless-stopped

networks:
  default:
    driver: bridge

3.2 Server konfiguration (server.cfg)
hostname "Mattias Quake Server"
deathmatch 1
fraglimit 20
timelimit 15
map e1m1
sv_maxclients 8

3.3 Starta server