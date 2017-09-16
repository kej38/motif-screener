import sys


def process_motif(back_ground_file_path, cont_file_path, motif):
    genome_1 = 0
    genome_2 = 0
    with open(back_ground_file_path) as f:
       genomes = f.readline()


def main():
    if len(sys.argv) != 4:
        print("-Usage [background_genome_file_path] [contaminating_genome_file_path] [motif]")
    else:
        back_ground_file_path = sys.argv[1]
        contaminating_genome_file_path = sys.argv[2]
        motif = sys.argv[3]
        process_motif(back_ground_file_path, contaminating_genome_file_path, motif)


main()
