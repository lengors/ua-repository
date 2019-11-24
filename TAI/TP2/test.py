import sys, os, subprocess

def sys_call(*args):
    print(' '.join(args))
    subprocess.run(args)

input_path = sys.argv[1] if len(sys.argv) > 1 else 'songs'
output_path = sys.argv[2] if len(sys.argv) > 2 else 'database'
vector_size = sys.argv[3] if len(sys.argv) > 3 else '8820'
overlap_factor = sys.argv[4] if len(sys.argv) > 4 else '4410'
cluster_size = sys.argv[5] if len(sys.argv) > 5 else '100'
max_iterations = sys.argv[6] if len(sys.argv) > 6 else '100'

sys_call('time', './run.sh', 'wavcb', vector_size, overlap_factor, cluster_size, input_path, output_path, max_iterations)

for song in os.listdir(input_path):
    sys_call('./run.sh', 'wavcp', os.path.join(input_path, song), song, '88200', '264600')
    if any([ a in song for a in [ '02', '05', '07' ] ]):
        sys_call('./run.sh', 'wavcp', os.path.join(input_path, song), 's01_{}'.format(song), '176400', '44100')

waves = [ file for file in os.listdir('.') if file.endswith('.wav') ]
for bits in [ '8', '4', '3' ]:
    for wave in waves:
        sys_call('./run.sh', 'wavquant', bits, wave, 'quant{}_{}'.format(bits, wave))

waves = [ file for file in os.listdir('.') if file.endswith('.wav') ]
for wave in waves:
    sys_call('./run.sh', 'wavfind', vector_size, overlap_factor, wave, output_path)