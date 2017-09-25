import sys
import re
from datetime import datetime

# allows seeing cmd line args.


def print_and_save_counts(chromosome, counter, positions, output_file, fasta_length):
    if len(positions) > 200:
        output_file.write("{},{},{},{}\n".format(chromosome, counter, fasta_length, chromosome + ".txt"))
        temp_file = open("./Results/" + chromosome + ".txt", "w")
        temp_file.write(" ".join(str(position) for position in positions))
        temp_file.close()
        print("Count: {}\nFasta Length: {}\nPositions: {}".format(counter, fasta_length, "More than 200"))
    else:
        output_file.write("{},{},{},{}\n".format(chromosome, counter, fasta_length, " ".join(str(position) for position in positions)))
        print("Count: {}\nFasta Length: {}\nPositions: {}".format(counter, fasta_length, positions))


def read_bases(open_file_path, output_file, motif):
    frequency_ratios = {}
    regex = re.compile("[>]")
    time_started = str(datetime.now())
    total_read = 0
    total_matches = 0
    position = 0
    positions = []
    motif_l = len(motif)
    chromosome = ""
    previous = ""
    counter = 0
    output_file.write("chromosome,count,fasta_length,position\n")
    print("Searching For Motif: {}".format(motif))
    f = open(open_file_path, 'r')
    for line in f:
        line = line.replace("\n", "")
        if regex.match(line):
            line = line.replace(">", "")
            if chromosome != "":
                print("\n" + chromosome)
                print_and_save_counts(chromosome, counter, positions, output_file, position)
                frequency_ratios[chromosome] = counter
            chromosome = line
            total_read += position
            total_matches += counter
            previous = ""
            positions = []
            position = 0
            counter = 0
        else:
            with_old = previous + line
            for i in range(0, len(with_old) - motif_l):
                position += 1
                match = with_old[i:i+motif_l]
                if match == motif:
                    positions.append(position)
                    counter += 1
            previous = with_old[-motif_l:]
    print_and_save_counts(chromosome, counter, positions, output_file, position)
    frequency_ratios[chromosome] = counter
    for chromosome in frequency_ratios:
        if frequency_ratios[chromosome] != 0:
            frequency_ratios[chromosome] = float(float(total_read)/float(frequency_ratios[chromosome]))
    time_ended = str(datetime.now())
    print("\nStarted: " + time_started)
    print("Ended: " + time_ended)
    print("Motif: {}".format(motif))
    return frequency_ratios


def process_motif(file_paths, motif, out_put_file):
    out_f = open("./Results/" + out_put_file, 'w')
    frequency_ratios = []
    for path in file_paths:
        frequency_ratios.append(read_bases(path, out_f, motif))
    out_f.close()
    print(frequency_ratios)


def main():
    if len(sys.argv) != 4:
        print("-Usage [file_path,file_path_2,...] [motif] [out_put_file]")
        print("Compare fasta with only 2 files.")
    else:
        back_ground_file_path = sys.argv[1].split(",")
        output_file = sys.argv[3]
        motif = sys.argv[2].upper()
        process_motif(back_ground_file_path, motif, output_file)


main()
