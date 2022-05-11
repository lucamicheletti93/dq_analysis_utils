import matplotlib.pyplot as plt

time = [0, 1, 2]
position = [0, 100, 200]

production = ['LHC15o_test', 'LHC18_pp_test', 'LHC18_pp_benchmark']

# Derived data tables
reduction_factor_fwd = [2333, 299, 812]
pss_memory_fwd = [2.2, 2.3, 2.3] # GB
timing_fwd = [2.62, 2.62, 2.6] # min
throughtput_fwd = [34.5, 17.5, 32.2] # MB/s

reduction_factor_barrel = [805, 272, 621]
pss_memory_barrel = [3.3, 3.9, 3.6] # GB
timing_barrel = [2.6, 2.96, 2.6] # min
throughtput_barrel = [4.2, 3.9, 4.6] # MB/s


figure, axis = plt.subplots(2, 2, figsize=(20, 8))

axis[0, 0].plot(production, reduction_factor_fwd, 'r', marker = "o", label = "fwd")
axis[0, 0].plot(production, reduction_factor_barrel, 'b', marker = "o", label = "barrel")
axis[0, 0].set_title("Reduction factor")
axis[0, 0].legend()

axis[1, 0].plot(production, pss_memory_fwd, 'r', marker = "o", label = "fwd")
axis[1, 0].plot(production, pss_memory_barrel, 'b', marker = "o", label = "barrel")
axis[1, 0].set_title("PSS memory")

axis[0, 1].plot(production, timing_fwd, 'r', marker = "o", label = "fwd")
axis[0, 1].plot(production, timing_barrel, 'b', marker = "o", label = "barrel")
axis[0, 1].set_title("Timing")

axis[1, 1].plot(production, throughtput_fwd, 'r', marker = "o", label = "fwd")
axis[1, 1].plot(production, throughtput_barrel, 'b', marker = "o", label = "barrel")
axis[1, 1].set_title("Throughtput")

plt.show()