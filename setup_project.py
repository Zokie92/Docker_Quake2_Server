import os

# Projektmappens namn
base = "Docker_Quake2_Server"

# Vilka mappar vi ska skapa
dirs = [
    "baseq2",
    "configs",
]

# Vilka filer vi ska skapa + innehåll
files = {
    "docker-compose.yml": """version: '3'
services:
  quake2:
    image: q2pro/q2pro:latest
    ports:
      - "27910:27910/udp"
    volumes:
      - ./baseq2:/q2pro/baseq2
""",

    "Dockerfile": """FROM q2pro/q2pro:latest
COPY baseq2 /q2pro/baseq2
COPY configs/server.cfg /q2pro/baseq2/server.cfg
""",

    "configs/server.cfg": """// Quake 2 Server Config
hostname "Docker Q2 Server"
maxclients 8
fraglimit 30
timelimit 20
map base1
""",

    "baseq2/README.txt": "Place your pak0.pak and pak1.pak here.\n"
}

# Skapar projektmappen
os.makedirs(base, exist_ok=True)

# Skapar submappar
for d in dirs:
    os.makedirs(os.path.join(base, d), exist_ok=True)

# Skapar filer
for path, content in files.items():
    full_path = os.path.join(base, path)
    with open(full_path, "w") as f:
        f.write(content)

print("Projektet är skapat!")
