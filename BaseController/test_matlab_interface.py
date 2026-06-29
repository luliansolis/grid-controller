from matlab_interface import OscClient
import matplotlib.pyplot as plt, mpld3
from scipy.io import loadmat


x = 0
y = 0
ori = 0
att = 1
os_client = OscClient("/mnt/c/PhD_Code_and_Data/2DSPAO/output_matrix.mat", "/mnt/c/PhD_Code_and_Data/2DSPAO")
filename = "/mnt/c/PhD_Code_and_Data/2DSPAO/out_data_0_0_0_att_1"
os_client.get_data(x,y,ori,att)
os_client.close()
data = loadmat(filename)["out_signal_complete"]