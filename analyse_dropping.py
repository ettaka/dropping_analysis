import matplotlib.pyplot as plt
import numpy as np
import argparse


colors = ['b','g','r','c','m','y','k']
markers = ['o', '^', 'v', '<', '>', '1', '2', '3', '4', 's', 'p', '*', 'h', '+', 'x']

data_list = []

def drop_fit(data):
    data['name'] = data['filename'].split('.')[0].replace('_', ' ')
    filename = data['filename']
    data_drop = np.loadtxt(filename, skiprows=3)
    name = data['name']
    
    data['t'] = data_drop[:,0]
    data['x'] = data_drop[:,1]
    data['v'] = data_drop[:,2]
    
    data_fit = data_drop

    if data['t0'] != None:
        data_fit = data_drop[data_drop[:,0]>data['t0']]

    if data['t1'] != None:
        data_fit = data_drop[data_drop[:,0]<data['t1']]
    
    data['fit'] = {}
    fit = np.polyfit(data_fit[:,0], data_fit[:,1], deg=2)
    data['fit']['function'] = fit
    data['fit']['a'] = 2 * fit[0]
    data['fit']['poly1d'] = np.poly1d(data['fit']['function'])

    data['fit']['t_0'] = -fit[1]/data['fit']['a']
    data['fit']['x_0'] = data['fit']['poly1d'](data['fit']['t_0'])

    return fit, name

def plot_fit(data):
    i = data['id']
    tol = data['plot_tol']

    plot_data = np.array([data['t'],data['x'],data['fit']['poly1d'](data['t'])]).T
    plot_data = plot_data[np.abs(plot_data[:,1]-plot_data[:,2])/plot_data[:,2]<tol]

    if True:
        data_t = plot_data[:,0]-data['fit']['t_0']
        data_x = plot_data[:,1]-data['fit']['x_0']
        data_x_fit = plot_data[:,2]-data['fit']['x_0']
    else:
        data_t = data['t']
        data_x = data['x']
        data_x_fit = data['fit']['poly1d'](data['t'])
    
    plt.plot(data_t, data_x,'--'+colors[i]+markers[i], label=data['name'])
    plt.plot(data_t, data_x_fit, '-b', label=data['name']+' fit')

def add_data(filename, t0=None, t1=None, plot_tol=1e-2):
    data_list.append({}) 
    data = data_list[-1]

    data['filename'] = filename
    data['t0'] = t0
    data['t1'] = t1
    data['id'] = len(data_list)
    data['plot_tol'] = plot_tol

parser = argparse.ArgumentParser(description='Analyse a dropping object')
#parser.add_argument('filenames', nargs='+', type=str)
parser.add_argument('-sp', '--show-plot', action='store_true', default=False) 
args = parser.parse_args()

add_data('marble.txt', plot_tol=1e-1)
add_data('lego_ball.txt', t0=0.8, t1=1.129, plot_tol=1)
add_data('foil_ball.txt', t0=0.7, t1=1.06)
add_data('ping_pong_ball.txt', t0=0.32, t1=0.78, plot_tol=1)

results=[]
plotname='fig'
print "name\tacceleration[m/s**2]"
for data in data_list:
    drop_fit(data)
    plot_fit(data)
    print data['name']+"\t{:2.2f}".format(data['fit']['a'])
    plotname+='_'+data['filename'].split('.')[0]

plt.legend(loc='best')
plt.grid()
if args.show_plot:
    plt.show()
else:
    plt.savefig(plotname)
