# Copyright 2012-2018 Ben Lambert

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



#~/bin/sh -x

# /home/bel/software/kaldi-trunk/src/latbin/lattice-rmali 'ark,t:gunzip -c /home/bel/kaldi-recipes/librispeech/s5/exp/tri5b/test_dev/decode_fglarge_dev_other/lat.1.gz|' 'ark,t:|gzip -c > /home/bel/kaldi-recipes/librispeech/s5/exp/tri5b/test_dev/decode_fglarge_dev_other_noali/lat.1.no_ali' 


# Size of n-bests
n=100

# This is 1/14
acoustic_scale=0.07

# This is 1/18
# acoustic_scale=0.055555

# folder=/home/bel/kaldi-recipes/librispeech/s5/exp/tri5b/decode_fglarge_train_other_500


# folder=/home/bel/kaldi-recipes/librispeech/s5/exp/tri5b/test_dev/decode_fglarge_dev_other
# folder=/home/bel/kaldi-recipes/librispeech/s5/exp/tri5b/test_dev/decode_fglarge_dev_clean
# folder=/home/bel/kaldi-recipes/librispeech/s5/exp/tri5b/test_dev/decode_fglarge_test_other
folder=/home/bel/kaldi-recipes/librispeech/s5/exp/tri5b/test_dev/decode_fglarge_test_clean

tasks=80
priority=0


# TODO: The file naming could be improved.  The final files have names like lat.1.nbest.txt
# TODO: gzip the files

# Remove alignments, they take up a huge amount of space
# qsub -o logs -N rmali -p $priority -t 1-$tasks -j y -cwd -l mem_free=2G -b y /home/bel/software/kaldi-trunk/src/latbin/lattice-rmali  \"ark,t\:gunzip -c $folder/lat.\$SGE_TASK_ID.gz\|\" ark\:$folder/lat.\$SGE_TASK_ID.no_ali
mkdir -p ${folder}_noali
mkdir -p ${folder}_nbest.ids
mkdir -p ${folder}_nbest.txt

# TODO: gzip the files...

# Remove alignments, they take up a huge amount of space
# qsub -o logs -N rmali -p $priority -t 1-$tasks -j y -cwd -l mem_free=2G -b y /home/bel/software/kaldi-trunk/src/latbin/lattice-rmali  \"ark,t\:gunzip -c $folder/lat.\$SGE_TASK_ID.gz\|\" ark:${folder}_noali/lat.\$SGE_TASK_ID.no_ali

# Convert to n-bests
# qsub -o logs -N lattice-to-nbest -p $priority -t 1-$tasks -j y -cwd -l mem_free=2G -b y /home/bel/software/kaldi-trunk/src/latbin/lattice-to-nbest --n=$n --acoustic-scale=$acoustic_scale ark\:${folder}_noali/lat.\$SGE_TASK_ID.no_ali ark,t\:${folder}_nbest.ids/nbest.\$SGE_TASK_ID.ids

# Convert the symbol IDs into symbols
qsub -o logs -N int2syms -hold_jid nbest-to-lin -p $priority -t 1-$tasks -j y -cwd -l mem_free=2G -b y /home/bel/software/kaldi-trunk/egs/wsj/s5/utils/int2sym.pl -f 3 /home/bel/kaldi-recipes/librispeech/s5/data/lang/words.txt ${folder}_nbest.ids/nbest.\$SGE_TASK_ID.ids \> ${folder}_nbest.txt/nbest.\$SGE_TASK_ID.txt
