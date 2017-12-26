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


from semlm.kaldi import read_nbest_entry_lines

# These aren't working yet...

def read_nbest_file(f):
    "Read a Kaldi n-best file."
    while True:
        entry = read_nbest_entry_lines(f)
        entry = split_nbest_lines(entry)
        print(list(entry))
        entry = process_line_data(entry)
        print(list(entry))
        exit()
        if not entry:
            break
        s = entry_lines_to_sentence(entry)
        print(s)

def split_nbest_lines(lines):
    line_data = map(str.split, lines)
    line_data = map(lambda x: x if len(x) != 4 else (x[:3] + x[3].split(',')), line_data)
    return line_data

def process_line_data(line_data):
    processed = []
    print(line_data)
    for i, line in enumerate(list(line_data)):
        print(i)
        if '' in line: line.remove('')
        if i == 0:
            processed.append(line)
            continue
        line[0] = int(line[0])
        if len(line) > 1:
            line[1] = int(line[1])
        if len(line) >= 5:
            line[3] = float(line[3])
            line[4] = float(line[4])

        processed.append(line)
    print(processed)
    return processed

def validate_line_data(line_data):
    line_data = list(line_data)
    assert(len(line_data[0]) == 1)
    for i, data in enumerate(line_data[1:]):
        assert(data[0] == i)
        assert(data[1] == i + 1)
