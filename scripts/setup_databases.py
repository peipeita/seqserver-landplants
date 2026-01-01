#!/usr/bin/env python3
"""
Setup script for creating BLAST databases from FASTA files
Automatically organizes databases into taxonomic subdirectories for Tree Widget
"""

import os
import subprocess
import glob
from pathlib import Path

FASTA_DIR = "/data/fasta"
BLAST_DB_DIR = "/app/blast_dbs"

# Taxonomic directory mapping based on filename prefixes
TAXONOMIC_DIRS = {
    "algae-": "Algae",
    "basal_angiosperm-": "Basal_Angiosperm",
    "eudicots-": "Eudicots",
    "fern-": "Fern",
    "fr-": "Fern",  # Alternative fern prefix
    "gymnosperm-": "Gymnosperm",
    "hornwort-": "Hornwort",
    "liverwort-": "Liverwort",
    "lycophyte-": "Lycophyte",
    "monocots-": "Monocots",
    "mosses-": "Mosses",
}

def get_taxonomic_dir(filename):
    """Determine taxonomic directory based on filename prefix"""
    for prefix, directory in TAXONOMIC_DIRS.items():
        if filename.startswith(prefix):
            return directory
    return None

def create_blast_db(fasta_file, output_base_dir):
    """Create BLAST database from FASTA file in appropriate taxonomic subdirectory"""
    basename = os.path.basename(fasta_file)
    db_name = os.path.splitext(basename)[0]

    # Determine taxonomic directory
    taxonomic_dir = get_taxonomic_dir(basename)

    if taxonomic_dir:
        output_dir = os.path.join(output_base_dir, taxonomic_dir)
        os.makedirs(output_dir, exist_ok=True)
        print(f"Processing: {basename} -> {taxonomic_dir}/{db_name}")
    else:
        output_dir = output_base_dir
        print(f"Processing: {basename} -> {db_name} (no taxonomic group detected)")

    cmd = [
        "makeblastdb",
        "-in", fasta_file,
        "-dbtype", "prot",
        "-out", os.path.join(output_dir, db_name),
        "-parse_seqids",
        "-hash_index",
        "-title", db_name
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✓ Created database: {taxonomic_dir}/{db_name}" if taxonomic_dir else f"✓ Created database: {db_name}")
        return True, taxonomic_dir
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create database for {basename}")
        print(f"Error: {e.stderr}")
        return False, None

def main():
    """Main setup function"""
    print("=" * 70)
    print("SequenceServer BLAST Database Setup with Tree Widget Organization")
    print("=" * 70)
    print(f"Source directory: {FASTA_DIR}")
    print(f"Target directory: {BLAST_DB_DIR}")
    print()

    # Create output directory if it doesn't exist
    os.makedirs(BLAST_DB_DIR, exist_ok=True)

    # Find all FASTA files (recursively)
    fasta_patterns = ["*.fasta", "*.fa", "*.faa", "*.pep"]
    fasta_files = []

    for pattern in fasta_patterns:
        fasta_files.extend(glob.glob(os.path.join(FASTA_DIR, "**", pattern), recursive=True))

    if not fasta_files:
        print(f"No FASTA files found in {FASTA_DIR}")
        return 1

    print(f"Found {len(fasta_files)} FASTA file(s)")
    print()

    # Create BLAST databases
    success_count = 0
    taxonomic_counts = {}

    for fasta_file in sorted(fasta_files):
        success, tax_dir = create_blast_db(fasta_file, BLAST_DB_DIR)
        if success:
            success_count += 1
            if tax_dir:
                taxonomic_counts[tax_dir] = taxonomic_counts.get(tax_dir, 0) + 1

    print()
    print("=" * 70)
    print(f"Setup complete: {success_count}/{len(fasta_files)} databases created")
    print("=" * 70)

    # Show taxonomic organization
    if taxonomic_counts:
        print("\nDatabases organized by taxonomic group:")
        for tax_dir in sorted(taxonomic_counts.keys()):
            count = taxonomic_counts[tax_dir]
            print(f"  {tax_dir + ':':<20} {count:>2} database(s)")
        print(f"\n  {'Total:':<20} {sum(taxonomic_counts.values()):>2} database(s)")

        print("\nTree Widget is now ready!")
        print("Access SequenceServer to see databases organized by taxonomy.")

    return 0 if success_count == len(fasta_files) else 1

if __name__ == "__main__":
    exit(main())
