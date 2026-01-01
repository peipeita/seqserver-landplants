# SequenceServer for Land Plants

Dockerized SequenceServer setup for BLAST searches against land plant protein sequences.

## Project Structure

```
sequenceserver-landplants/
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Multi-architecture Docker image
├── scripts/
│   └── setup_databases.py     # Setup script - creates & organizes databases
├── config/
│   └── sequenceserver.conf    # SequenceServer configuration
├── blast_dbs/                 # BLAST databases organized by taxonomy
│   ├── Algae/                 # 7 databases
│   ├── Basal_Angiosperm/      # 2 databases
│   ├── Eudicots/              # 1 database
│   ├── Fern/                  # 11 databases
│   ├── Gymnosperm/            # 5 databases
│   ├── Hornwort/              # 12 databases
│   ├── Liverwort/             # 8 databases
│   ├── Lycophyte/             # 4 databases
│   ├── Monocots/              # 1 database
│   └── Mosses/                # 5 databases
└── README.md                  # This file
```

**Total: 56 BLAST databases**

## Requirements

- Docker Desktop (with Docker Compose)
- FASTA files in `/Users/user/landplants-fastas/clean/pep`

## Setup

### 1. Build the Docker Image

```bash
docker-compose build
```

### 2. Create BLAST Databases

Run the setup script to automatically create and organize databases:

```bash
docker-compose run --rm sequenceserver python3 /app/scripts/setup_databases.py
```

**What this does:**
- Recursively searches for all FASTA files (`.fasta`, `.fa`, `.faa`, `.pep`) in the source directory
- Creates BLAST databases for each file
- **Automatically organizes databases into taxonomic subdirectories** based on filename prefixes
- Prepares the tree widget structure for easy navigation

The script will show you a summary of databases organized by taxonomic group when complete.

### 3. Start SequenceServer

```bash
docker-compose up -d
```

SequenceServer will be available at: http://localhost:4567

## Usage

### Start the Service
```bash
docker-compose up -d
```

### Stop the Service
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f sequenceserver
```

### Rebuild Databases
If you add new FASTA files or update existing ones:

```bash
# Stop the service
docker-compose down

# Clear old databases (optional, if you want a fresh start)
rm -rf blast_dbs/*

# Rebuild databases (automatically organized into taxonomic subdirectories)
docker-compose run --rm sequenceserver python3 /app/scripts/setup_databases.py

# Start the service
docker-compose up -d
```

**Note:** The setup script automatically detects taxonomic groups from filename prefixes and organizes databases accordingly. Make sure your FASTA files follow the naming convention: `<group>-<species>.pep.fa`

### Adding New Protein Files

To add new protein FASTA files to your SequenceServer database:

#### 1. Add Your FASTA Files
Place your new protein FASTA files in the source directory:
```
/Users/user/landplants-fastas/clean/pep/
```

The script will automatically detect files with these extensions: `.fasta`, `.fa`, `.faa`, `.pep`

#### 2. Name Files with Taxonomic Prefixes
For automatic organization into taxonomic groups, use these naming conventions:

- `algae-yourspecies.pep.fa` → Algae folder
- `basal_angiosperm-yourspecies.pep.fa` → Basal_Angiosperm folder
- `eudicots-yourspecies.pep.fa` → Eudicots folder
- `fern-yourspecies.pep.fa` or `fr-yourspecies.pep.fa` → Fern folder
- `gymnosperm-yourspecies.pep.fa` → Gymnosperm folder
- `hornwort-yourspecies.pep.fa` → Hornwort folder
- `liverwort-yourspecies.pep.fa` → Liverwort folder
- `lycophyte-yourspecies.pep.fa` → Lycophyte folder
- `monocots-yourspecies.pep.fa` → Monocots folder
- `mosses-yourspecies.pep.fa` → Mosses folder

**Note:** Files without these prefixes will still be processed and added to the database, but won't be organized into a specific taxonomic folder.

#### 3. Rebuild BLAST Databases
After adding new files, rebuild the databases:

```bash
# Stop the service
docker-compose down

# Run the setup script (processes all FASTA files including new ones)
docker-compose run --rm sequenceserver python3 /app/scripts/setup_databases.py

# Restart the service
docker-compose up -d
```

The setup script will show you a summary of all databases organized by taxonomic group.

#### 4. Adding New Taxonomic Groups
If you need a taxonomic category not listed above, you can modify the `TAXONOMIC_DIRS` dictionary in `scripts/setup_databases.py` to add custom prefixes and folder names.

## Features

### Tree Widget for Database Organization

This setup uses SequenceServer's **Tree Widget** feature to organize databases hierarchically by taxonomic groups. The setup scripts **automatically organize databases** based on filename prefixes, so you don't need to manually create subdirectories.

**Taxonomic Groups:**
- **Algae**: Green algae and streptophyte algae (`algae-*.pep.fa`)
- **Basal Angiosperm**: Early-diverging flowering plants (`basal_angiosperm-*.pep.fa`)
- **Eudicots**: Dicotyledonous flowering plants (`eudicots-*.pep.fa`)
- **Fern**: Ferns and fern allies (`fern-*.pep.fa`, `fr-*.pep.fa`)
- **Gymnosperm**: Conifers and related plants (`gymnosperm-*.pep.fa`)
- **Hornwort**: Hornworts (`hornwort-*.pep.fa`)
- **Liverwort**: Liverworts (`liverwort-*.pep.fa`)
- **Lycophyte**: Clubmosses and relatives (`lycophyte-*.pep.fa`)
- **Monocots**: Monocotyledonous flowering plants (`monocots-*.pep.fa`)
- **Mosses**: Mosses (`mosses-*.pep.fa`)

**Benefits:**
- ✓ Automatic organization - no manual file moving required
- ✓ Select specific taxonomic groups for targeted BLAST searches
- ✓ Compare results across evolutionary lineages
- ✓ Navigate large numbers of databases efficiently

**Configuration:**
The tree widget is enabled in `config/sequenceserver.conf`:
```yaml
:databases_widget: tree
```

The database organization is handled automatically by `scripts/setup_databases.py` based on filename prefixes.

## Configuration

### Port Configuration
The service is exposed on port 4567. To change the port, edit `docker-compose.yml`:

```yaml
ports:
  - "YOUR_PORT:4567"
```

### BLAST Parameters
Edit `config/sequenceserver.conf` to modify:
- E-value thresholds
- Number of threads
- Job lifetime (result caching)
- Other BLAST options

### Data Directory
The FASTA files are mounted from `/Users/user/landplants-fastas/clean/pep`. To change the source directory, edit `docker-compose.yml`:

```yaml
volumes:
  - /path/to/your/fasta/files:/data/fasta:ro
```

## Platform Information

This Docker image is configured to run on `linux/amd64` platform, which works on both:
- Intel/AMD (x86_64) Macs and PCs
- Apple Silicon (ARM64) Macs via Rosetta 2 emulation

## Troubleshooting

### Database not found
Make sure you've created the BLAST databases using one of the setup scripts before starting SequenceServer.

### Permission issues
Ensure the `./blast_dbs` directory has appropriate write permissions:
```bash
chmod -R 755 blast_dbs
```

### Port already in use
If port 4567 is already in use, change the port mapping in `docker-compose.yml`.

### Container won't start
Check the logs:
```bash
docker-compose logs sequenceserver
```

## Accessing SequenceServer

Once running, open your web browser and navigate to:
```
http://localhost:4567
```

You should see the SequenceServer interface with your BLAST databases organized in a tree structure by taxonomic group, making it easy to select databases for your searches.

## Data Persistence

- BLAST databases are stored in `./blast_dbs` (persistent)
- Source FASTA files are mounted read-only from `/Users/user/landplants-fastas/clean/pep`
- BLAST search results are cached according to the `job_lifetime` setting

## Maintenance

### Updating SequenceServer
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Cleaning Up
```bash
# Stop and remove containers
docker-compose down

# Remove BLAST databases (will need to rebuild)
rm -rf blast_dbs/*
```

## License

Please refer to SequenceServer's license at https://sequenceserver.com/
