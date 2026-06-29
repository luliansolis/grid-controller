import socket 
import os
import matplotlib.pyplot as plt, mpld3
from scipy.io import loadmat
import webbrowser
import json
class OscClient:
    def __init__(self, filename, path):
        self.fs = filename
        self.path = path
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("localhost", 5555))
        print("Connected Oscilloscope")
    def get_data(self, xpos, ypos, orpos, att, display_data = False):
        self.sock.sendall("CAPTURE\n".encode())
        ack = self.sock.recv(4096)
        print("Did I go through this?")
        out_filename = f"out_data_{int(xpos)}_{int(ypos)}_{orpos}_att_{att}.mat"
        filename = self.fs
        out_filename = os.path.join(self.path, out_filename)
        os.rename(filename, out_filename)
        filename_two = "/mnt/c/PhD_Code_and_Data/2DSPAO/output_matrix_res.mat"
        out_filename = f"out_data_res_{int(xpos)}_{int(ypos)}_{orpos}_att_{att}.mat"
        out_filename = os.path.join(self.path, out_filename)
        os.rename(filename_two, out_filename)
        if display_data:
            self.display_data(xpos, ypos, orpos, att)
    def display_data(self, xpos, ypos, orpos, att):
        out_filename = f"out_data_{int(xpos)}_{int(ypos)}_{orpos}_att_{att}.mat"
        out_filename = os.path.join(self.path, out_filename)
        mat = loadmat(out_filename)["out_signal_complete"]
        colors = ['#2196F3', '#F44336', '#4CAF50', '#FF9800']
        labels = [f'CH{i+1}' for i in range(4)]
        fig, ax = plt.subplots(figsize=(10,10))
        for i, row in enumerate(mat):
            ax.plot(row, color=colors[i], linewidth=0.8, label=labels[i])
        ax.legend()
        ax.set_xlabel("Samples")
        ax.set_ylabel("Voltage [V]")
        self.show_plot(fig)
    def show_plot(self, fig):
        fig_dict = mpld3.fig_to_dict(fig)
        # inject auto-refresh every 2 seconds
        #html = html.replace('<head>', '<head><meta http-equiv="refresh" content="2">')
        with open("plot.json", "w") as f:
            json.dump(fig_dict, f)
        with open("plot.html", "w") as f:
            fig_json = json.dumps(fig_dict)
            print(fig_dict["width"])
            f.write("""
        <!DOCTYPE html>
        <html>
        <body>
            <h1>SLICER Dashboard</h1>
            <div id="plot"></div>
            <script src="https://d3js.org/d3.v5.min.js"></script>

            <script src="https://mpld3.github.io/js/mpld3.v0.5.9.min.js"></script>
            <script>
                fetch('plot.json')
                    .then(r => r.json())
                    .then(fig => mpld3.draw_figure('plot', fig));
            </script>
        </body>
        </html>
        """)
    def close(self):
        print("Enters here?")
        self.sock.close()