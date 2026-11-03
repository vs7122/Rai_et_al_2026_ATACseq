
import sys
import gzip

if len(sys.argv) != 3:
    sys.stderr.write("Usage:  count.py Sample_R1.fastq.gz Sample_R2.fastq.gz\n")
    sys.exit(-1)

# Open the two files, using either the standard file open, or the gzip.open if they are gzipped files.

fp1 = open(sys.argv[1]) if not sys.argv[1].endswith(".gz") else gzip.open(sys.argv[1], "rt")
fp2 = open(sys.argv[2]) if not sys.argv[2].endswith(".gz") else gzip.open(sys.argv[2], "rt")

# Loop through the reads to the ends of both files.

readcnt = 0
telocnt = 0
while True:
    # Read four lines from each of the files (to get the fastq lines for the next read from each file).
    
    (l11, l12, l13, l14) = (fp1.readline(), fp1.readline(), fp1.readline(), fp1.readline())
    (l21, l22, l23, l24) = (fp2.readline(), fp2.readline(), fp2.readline(), fp2.readline())

    # If we hit the end of the file for both files, stop.
    
    if not l11 and not l21:
        break

    # Perform some checks to make sure both files have the same number of lines, both files
    # are in the fastq format, and the order of the reads match (i.e., the same order of read
    # accessions appear in the two files).
    
    if not l11:
        sys.stderr.write("Error:  File '%s' is shorter than file '%s'.\n" % (sys.argv[1], sys.argv[2]))
        sys.exit(-1)

    if not l21:
        sys.stderr.write("Error:  File '%s' is shorter than file '%s'.\n" % (sys.argv[2], sys.argv[1]))
        sys.exit(-1)

    if not l14 or not l24 or l11[0] != "@" or l21[0] != "@" or l13[0] != "+" or l23[0] != "+":
        sys.stderr.write("Error:  Invalid fastq file format.\n")
        sys.exit(-1)

    acc1 = l11[1:].split()[0]
    acc2 = l21[1:].split()[0]

    if acc1 != acc2:
        sys.stderr.write("Error:  R1 and R2 files contain different read orders.\n")
        sys.exit(-1)

    # Check the reads to see if they contain the telomere signature.

    readcnt += 1
    
    #Change these lines to change number of reads you are searching for. Currently set at 2
    if l12.find("TTAGGGTTAGGG") != -1 or \
       l12.find("CCCTAACCCTAA") != -1 or \
       l22.find("TTAGGGTTAGGG") != -1 or \
       l22.find("CCCTAACCCTAA") != -1:
        telocnt += 1

fp1.close()
fp2.close()

sys.stdout.write("%d of %d reads (%.3f%%) found as telomere.\n" % (telocnt, readcnt, telocnt * 100.0 / readcnt))
