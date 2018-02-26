import matplotlib.pyplot as plt
plt.plot([0.2,0.4,0.6,0.8,1], [0.761176470588235,0.716470588235294,0.687647058823529, 0.665294117647059,0.655882352941176], 'ro')
plt.axis([0, 1.2, 0.6, 0.8])
plt.ylabel('error rate by sentence')
plt.show()
