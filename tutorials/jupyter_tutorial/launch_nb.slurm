#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --mem=2G               # 2Gb memory
#SBATCH --time=0-04:00:00      # 4 hours
#SBATCH --output=notebook.out

# Once this job launches, check the node it landed on with:
#      squeue --user=userid
# Then open tunnel from local machine with something like:
#      ssh -L 9999:vmpXXX:7777 vunetid@login.accre.vanderbilt.edu
# This binds port 9999 on localhost to port 7777 on vmpXXX
# Finally, point your local browser to localhost:9999

PORT=7777
echo To open a tunnel from local machine, 
echo Execute in a new terminal window:
echo "ssh -L 9999:$HOSTNAME:$PORT $(whoami)@login.accre.vanderbilt.edu"
printf '=%.0s' {1..80}
echo

module load Anaconda3      # load python 
source activate capra_py3  # load virtual environment

jt -t solarizedd -f anonymous -fs 15 -nfs 15 -ofs 15 -cellw 90%  # optionally set theme

jupyter notebook --no-browser --ip='*' --port=${PORT}

