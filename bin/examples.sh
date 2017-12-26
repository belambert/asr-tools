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


echo "Compute WER:"
python compute-wer.py ~/data/librispeech1/dev_clean.ref ~/data/librispeech1/dev_clean.14_0.5.tra.txt 

echo "Compute oracle WER:"
python oracle-wer.py ~/data/librispeech1/nbests/lat.1.nbest.txt ~/data/librispeech1/dev_clean.ref

echo "Display n-best improvements:"
python show-nbest-improvements.py ~/data/librispeech1/nbests/lat.1.nbest.txt ~/data/librispeech1/dev_clean.ref

# I'm not sure if this is right
echo "Display n-bests?"
python show-nbests.py ~/data/librispeech1/nbests/lat.1.nbest.txt ~/data/librispeech1/dev_clean.ref
