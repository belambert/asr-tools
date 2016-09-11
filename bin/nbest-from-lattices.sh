#~/bin/sh -x

n=100

# This is 1/14
acoustic_scale=0.07
# folder=/home/bel/kaldi-run/librispeech/s5/exp/tri5b/decode_fglarge_dev_other
folder=/home/bel/kaldi-run/librispeech/s5/exp/tri5b/decode_fglarge_dev_clean
tasks=80
priority=1024


# TODO: The file naming could be improved.  The final files have names like lat.1.nbest.txt
# TODO: gzip the files

# Remove alignments, they take up a huge amount of space
# qsub -o logs -N rmali -p $priority -t 1-$tasks -j y -cwd -l mem_free=2G -b y /home/bel/software/kaldi-trunk/src/latbin/lattice-rmali  \"ark,t\:gunzip -c $folder/lat.\$SGE_TASK_ID.gz\|\" ark\:$folder/lat.\$SGE_TASK_ID.no_ali

# Convert to text N-bests
# qsub -o logs -N lattice-to-nbest -p $priority -t 1-$tasks -j y -cwd -l mem_free=2G -b y /home/bel/software/kaldi-trunk/src/latbin/lattice-to-nbest --n=$n --acoustic-scale=$acoustic_scale ark\:$folder/lat.\$SGE_TASK_ID.no_ali ark,t\:$folder/lat.\$SGE_TASK_ID.nbest.ids

# Convert the symbol IDs into symbols
qsub -o logs -N int2syms -hold_jid nbest-to-lin -p $priority -t 1-$tasks -j y -cwd -l mem_free=2G -b y /home/bel/software/kaldi-trunk/egs/wsj/s5/utils/int2sym.pl -f 3 /home/bel/kaldi-recipes/librispeech/s5/data/lang/words.txt $folder/lat.\$SGE_TASK_ID.nbest.ids \> $folder/lat.\$SGE_TASK_ID.nbest.txt


