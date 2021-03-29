import subprocess
import matplotlib.pyplot as plt
from tqdm import tqdm
from mining.util.formatters.JsonFormatter import JsonFormatter
import os.path

# modify these value for different run configurations
N = 29
start = 10
end = 300

# initialization
step = (end - start) / N
parameters = list(map(lambda x: round(start + x * step), range(N + 1)))
formatter = JsonFormatter()

total_couplings = []

# execute the tool for each parameter
for parameter in tqdm(parameters, unit=' run', desc="Performaing analysis"):
  # output file name for the analyzer
  filename = f"ensemble-output/{parameter}.json"

  # if the file exist, use it as a cache, execute the analyzer on command line otherwise
  if not os.path.isfile(filename):
    subprocess.run([
        "python3",
        "mining",
        "analysis",
        "-r", "cache/flowengine-go",
        "-al", "urc",
        "-nm",
        "-nw",
        "-nl",
        "-df", "reuse",
        "-cc", f"{parameter}m",
        "-o", f"{filename}"
    ], capture_output=True)

  # import the ouput data from the analysis
  data = formatter.import_file({'input': filename})

  # perform some kind of data collection, in this case sum up all couplings
  total_couplings.append(sum(edge['weight'] for edge in data['edges']))

# show the data on a graph, that plots the input paramters against the output data
plt.figure()
plt.xlabel("Combine Consecutive [Minutes]")
plt.ylabel("Total Couplings")
plt.plot(parameters, total_couplings)
plt.savefig("results.pdf")
plt.show()
