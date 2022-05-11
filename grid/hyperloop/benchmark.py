import matplotlib.pyplot as plt
import array as arr

production = ['LHC15o_test', 'LHC18_pp_test', 'LHC18_pp_benchmark']

# Derived data tables
reduction_factor_fwd = arr.array('d', [2333, 299, 812])
pss_memory_fwd = arr.array('d', [2.2, 2.3, 2.3]) # GB
timing_fwd = arr.array('d', [2.62, 2.62, 2.6]) # min
throughtput_fwd = arr.array('d', [34.5, 17.5, 32.2]) # MB/s
procData_fwd = arr.array('d', [0 ,0 ,0])

reduction_factor_barrel = arr.array('d', [805, 272, 621])
pss_memory_barrel = arr.array('d', [3.3, 3.9, 3.6]) # GB
timing_barrel = arr.array('d', [2.6, 2.96, 2.6]) # min
throughtput_barrel = arr.array('d', [4.2, 3.9, 4.6]) # MB/s
procData_barrel = arr.array('d', [0 ,0 ,0])

print("Processed data")
for iIndex in range(0, len(production)) :
    print("----> %s" % production[iIndex])
    procData_fwd[iIndex] = 3. *  throughtput_fwd[iIndex]
    print("fwd = %f" % procData_fwd[iIndex])
    procData_barrel[iIndex] = 3. *  throughtput_barrel[iIndex]
    print("barrel = %f" % procData_barrel[iIndex])


figure, axis = plt.subplots(2, 2, figsize=(20, 8))

axis[0, 0].plot(production, reduction_factor_fwd, 'r', marker = "o", label = "fwd")
axis[0, 0].plot(production, reduction_factor_barrel, 'b', marker = "o", label = "barrel")
axis[0, 0].set_title("Reduction factor")
axis[0, 0].legend()

axis[1, 0].plot(production, pss_memory_fwd, 'r', marker = "o", label = "fwd")
axis[1, 0].plot(production, pss_memory_barrel, 'b', marker = "o", label = "barrel")
axis[1, 0].set_title("PSS memory (GB)")
axis[1, 0].legend()

axis[0, 1].plot(production, procData_fwd, 'r', marker = "o", label = "fwd")
axis[0, 1].plot(production, procData_barrel, 'b', marker = "o", label = "barrel")
axis[0, 1].set_title("Processed data in 3 min (MB)")
axis[0, 1].legend()

axis[1, 1].plot(production, throughtput_fwd, 'r', marker = "o", label = "fwd")
axis[1, 1].plot(production, throughtput_barrel, 'b', marker = "o", label = "barrel")
axis[1, 1].set_title("Throughtput")
axis[1, 1].legend()

plt.show()