echo "Compute WER:"
python compute-wer.py ~/data/librispeech1/dev_clean.ref ~/data/librispeech1/dev_clean.14_0.5.tra.txt 

echo "Compute oracle WER:"
python oracle-wer.py ~/data/librispeech1/nbests/lat.1.nbest.txt ~/data/librispeech1/dev_clean.ref

echo "Display n-best improvements:"
python show-nbest-improvements.py ~/data/librispeech1/nbests/lat.1.nbest.txt ~/data/librispeech1/dev_clean.ref

# I'm not sure if this is right
echo "Display n-bests?"
python show-nbests.py ~/data/librispeech1/nbests/lat.1.nbest.txt ~/data/librispeech1/dev_clean.ref
