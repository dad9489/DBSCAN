print(__doc__)

import numpy as np

from sklearn.cluster import DBSCAN, KMeans
from sklearn import metrics


# #############################################################################
# Generate sample data
# centers = [[1, 1], [-1, -1], [1, -1]]
# X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,
#                             random_state=0)
#
# X = StandardScaler().fit_transform(X)

# "normal" dataset
# X = [[0.1129032258064516, 0.511904761904762], [0.13306451612903228, 0.5335497835497836], [0.14919354838709678, 0.5227272727272727], [0.1592741935483871, 0.49296536796536794], [0.1532258064516129, 0.4496753246753247], [0.12298387096774191, 0.4550865800865801], [0.11088709677419353, 0.49296536796536794], [0.1290322580645161, 0.4902597402597403], [0.18145161290322578, 0.45779220779220786], [0.17741935483870966, 0.5227272727272727], [0.7943548387096774, 0.45779220779220786], [0.8508064516129031, 0.4496753246753247], [0.8487903225806451, 0.3874458874458875], [0.8064516129032259, 0.3847402597402597], [0.7963709677419355, 0.4253246753246753], [0.8185483870967742, 0.4334415584415585], [0.8286290322580645, 0.39015151515151514], [0.8729838709677419, 0.41720779220779225], [0.8205645161290323, 0.4686147186147186], [0.5060483870967742, 0.7932900432900434], [0.5342741935483871, 0.7635281385281386], [0.5100806451612904, 0.7283549783549784], [0.4798387096774194, 0.7445887445887447], [0.48991935483870974, 0.7716450216450217], [0.5201612903225806, 0.7472943722943723], [0.5362903225806451, 0.7175324675324676], [0.47580645161290325, 0.7012987012987013], [0.5685483870967742, 0.7581168831168832], [0.46370967741935487, 0.23322510822510825], [0.5161290322580645, 0.17911255411255414], [0.47379032258064513, 0.14935064935064937], [0.4536290322580645, 0.16287878787878787], [0.45967741935483875, 0.21428571428571433], [0.49193548387096775, 0.2061688311688312], [0.4798387096774194, 0.17911255411255414], [0.44354838709677424, 0.20075757575757577], [0.5040322580645161, 0.24134199134199139], [0.5362903225806451, 0.18722943722943727], [0.19758064516129034, 0.8419913419913421], [0.4576612903225806, 0.5281385281385281], [0.21370967741935484, 0.2196969696969697], [0.7721774193548387, 0.18452380952380956], [0.7721774193548387, 0.7797619047619049], [0.5423387096774194, 0.21158008658008662], [0.8366935483870968, 0.4117965367965368], [0.497983870967742, 0.6850649350649352], [0.5705645161290323, 0.7256493506493507], [0.18346774193548385, 0.49837662337662336], [0.14919354838709678, 0.5714285714285715], [0.33467741935483875, 0.9312770562770564]]

# non-convex
# X = [[0.7520161290322581, 0.6255411255411256], [0.75, 0.6471861471861472], [0.7358870967741935, 0.6742424242424243], [0.7258064516129032, 0.6931818181818182], [0.7056451612903226, 0.7148268398268399], [0.6834677419354839, 0.7283549783549784], [0.6491935483870968, 0.7445887445887447], [0.6088709677419355, 0.7527056277056278], [0.5705645161290323, 0.7527056277056278], [0.5362903225806451, 0.7527056277056278], [0.497983870967742, 0.7445887445887447], [0.4556451612903226, 0.7310606060606061], [0.41532258064516125, 0.7067099567099567], [0.38508064516129037, 0.6823593073593074], [0.3568548387096775, 0.649891774891775], [0.33467741935483875, 0.5957792207792209], [0.32056451612903225, 0.538961038961039], [0.3084677419354839, 0.48484848484848486], [0.3084677419354839, 0.4253246753246753], [0.3165322580645161, 0.35497835497835506], [0.33467741935483875, 0.31980519480519487], [0.36491935483870974, 0.2846320346320347], [0.3911290322580645, 0.24675324675324675], [0.4193548387096774, 0.2224025974025974], [0.4375, 0.2088744588744589], [0.469758064516129, 0.19805194805194806], [0.497983870967742, 0.19264069264069264], [0.5342741935483871, 0.18722943722943727], [0.5725806451612904, 0.18452380952380956], [0.6129032258064516, 0.18722943722943727], [0.5826612903225806, 0.18452380952380956], [0.3004032258064516, 0.5362554112554113], [0.3104838709677419, 0.47132034632034636], [0.32056451612903225, 0.3847402597402597], [0.342741935483871, 0.6228354978354979], [0.38306451612903225, 0.676948051948052], [0.44758064516129037, 0.7175324675324676], [0.5181451612903226, 0.7364718614718615], [0.5705645161290323, 0.7472943722943723], [0.6209677419354839, 0.7472943722943723], [0.6754032258064516, 0.7391774891774893], [0.5423387096774194, 0.5281385281385281], [0.560483870967742, 0.5227272727272727], [0.5725806451612904, 0.48484848484848486], [0.5504032258064516, 0.4496753246753247], [0.5201612903225806, 0.4632034632034633], [0.5100806451612904, 0.49837662337662336], [0.5362903225806451, 0.5091991341991342], [0.5645161290322581, 0.48484848484848486], [0.5362903225806451, 0.47132034632034636], [0.5362903225806451, 0.48484848484848486], [0.5725806451612904, 0.48755411255411263], [0.5887096774193549, 0.5227272727272727], [0.560483870967742, 0.5443722943722944], [0.5282258064516129, 0.5362554112554113], [0.5282258064516129, 0.49296536796536794], [0.5766129032258065, 0.4604978354978355], [0.5866935483870968, 0.45779220779220786], [0.5846774193548387, 0.5146103896103896], [0.7237903225806451, 0.4145021645021645], [0.7459677419354839, 0.4145021645021645], [0.7661290322580645, 0.3982683982683983], [0.7883064516129032, 0.3847402597402597], [0.8225806451612904, 0.3712121212121212], [0.8487903225806451, 0.36038961038961037], [0.8830645161290324, 0.33333333333333337], [0.9072580645161291, 0.3252164502164503], [0.8790322580645161, 0.336038961038961], [0.8024193548387096, 0.36309523809523814], [0.7439516129032259, 0.39015151515151514], [0.7883064516129032, 0.37662337662337664], [0.8306451612903226, 0.3576839826839827], [0.8508064516129031, 0.3387445887445888], [0.8790322580645161, 0.3170995670995671], [0.8084677419354839, 0.34686147186147187]]


# noisy
# X = [[0.17137096774193547, 0.3793290043290043], [0.18145161290322578, 0.39015151515151514], [0.20161290322580647, 0.43885281385281383], [0.22782258064516128, 0.5064935064935066], [0.252016129032258, 0.5524891774891775], [0.27620967741935487, 0.5876623376623377], [0.2782258064516129, 0.5470779220779222], [0.29032258064516125, 0.4902597402597403], [0.30241935483870963, 0.43885281385281383], [0.314516129032258, 0.3874458874458875], [0.30645161290322576, 0.37662337662337664], [0.27217741935483875, 0.40909090909090906], [0.2479838709677419, 0.4334415584415585], [0.22983870967741934, 0.45238095238095244], [0.19758064516129034, 0.49296536796536794], [0.17137096774193547, 0.5254329004329005], [0.18749999999999997, 0.5281385281385281], [0.24596774193548385, 0.5173160173160174], [0.28629032258064513, 0.5146103896103896], [0.3266129032258065, 0.5091991341991342], [0.36895161290322587, 0.5010822510822511], [0.314516129032258, 0.47132034632034636], [0.2641129032258065, 0.4496753246753247], [0.252016129032258, 0.43885281385281383], [0.1995967741935484, 0.4117965367965368], [0.7076612903225806, 0.3874458874458875], [0.7217741935483871, 0.4117965367965368], [0.7459677419354839, 0.4686147186147186], [0.7600806451612904, 0.511904761904762], [0.7741935483870968, 0.5416666666666667], [0.7903225806451613, 0.4902597402597403], [0.8024193548387096, 0.4280303030303031], [0.8125, 0.373917748917749], [0.7862903225806451, 0.3874458874458875], [0.7520161290322581, 0.42261904761904767], [0.7258064516129032, 0.45779220779220786], [0.7036290322580645, 0.48755411255411263], [0.75, 0.48755411255411263], [0.7903225806451613, 0.47943722943722944], [0.8286290322580645, 0.47132034632034636], [0.8548387096774194, 0.4632034632034633], [0.8145161290322581, 0.446969696969697], [0.7661290322580645, 0.4280303030303031], [0.7096774193548387, 0.39556277056277056], [0.7681451612903226, 0.45238095238095244], [0.25806451612903225, 0.47943722943722944], [0.13508064516129034, 0.9448051948051949], [0.4092741935483871, 0.8014069264069265], [0.6411290322580645, 0.933982683982684], [0.9112903225806451, 0.8690476190476192], [0.5181451612903226, 0.6201298701298702], [0.41532258064516125, 0.11417748917748918], [0.10483870967741934, 0.13041125541125545], [0.4576612903225806, 0.2711038961038962], [0.7338709677419355, 0.1547619047619048], [0.9475806451612904, 0.12770562770562774], [0.9475806451612904, 0.6336580086580087], [0.7137096774193549, 0.6634199134199135], [0.09274193548387097, 0.6985930735930737], [0.31854838709677413, 0.9096320346320347], [0.08467741935483872, 0.446969696969697], [0.5987903225806451, 0.4280303030303031], [0.5544354838709677, 0.7770562770562771], [0.7862903225806451, 0.787878787878788], [0.9596774193548386, 0.3035714285714286], [0.2641129032258065, 0.25757575757575757], [0.25604838709677413, 0.7445887445887447], [0.47379032258064513, 0.9502164502164504], [0.8306451612903226, 0.9556277056277057], [0.5806451612903226, 0.2224025974025974], [0.7600806451612904, 0.014069264069264065], [0.22580645161290322, 0.016774891774891776], [0.23588709677419353, 0.4821428571428572], [0.2620967741935484, 0.49837662337662336], [0.2681451612903226, 0.520021645021645]]

# one cluster
# X = [[0.4334677419354839, 0.5443722943722944], [0.42741935483870974, 0.5633116883116883], [0.44758064516129037, 0.5768398268398269], [0.45967741935483875, 0.5579004329004329], [0.467741935483871, 0.520021645021645], [0.4536290322580645, 0.511904761904762], [0.44354838709677424, 0.5443722943722944], [0.4536290322580645, 0.5524891774891775], [0.4879032258064516, 0.5524891774891775], [0.497983870967742, 0.5903679653679654], [0.4717741935483871, 0.6147186147186148], [0.4395161290322581, 0.6174242424242424], [0.39717741935483875, 0.6011904761904763], [0.3870967741935484, 0.5551948051948052], [0.43145161290322587, 0.5010822510822511], [0.5100806451612904, 0.47943722943722944], [0.5141129032258065, 0.5443722943722944], [0.5100806451612904, 0.5524891774891775], [0.4959677419354839, 0.5146103896103896], [0.4495967741935484, 0.474025974025974], [0.4092741935483871, 0.5091991341991342], [0.3931451612903226, 0.5470779220779222], [0.4193548387096774, 0.58495670995671], [0.44556451612903225, 0.5984848484848485], [0.4657258064516129, 0.58495670995671], [0.469758064516129, 0.538961038961039], [0.4858870967741936, 0.4821428571428572], [0.4334677419354839, 0.45779220779220786], [0.3911290322580645, 0.48755411255411263], [0.3629032258064516, 0.5551948051948052], [0.36693548387096775, 0.612012987012987], [0.4213709677419355, 0.630952380952381], [0.4717741935483871, 0.630952380952381], [0.5141129032258065, 0.5984848484848485], [0.5423387096774194, 0.520021645021645], [0.497983870967742, 0.44426406926406925], [0.44354838709677424, 0.43614718614718617], [0.5060483870967742, 0.48755411255411263], [0.5221774193548387, 0.5660173160173161], [0.4959677419354839, 0.6147186147186148], [0.4375, 0.6363636363636364], [0.3568548387096775, 0.5714285714285715], [0.10282258064516128, 0.8690476190476192], [0.07459677419354838, 0.5524891774891775], [0.09475806451612903, 0.28733766233766234], [0.5483870967741936, 0.10335497835497837], [0.780241935483871, 0.6444805194805195], [0.4193548387096774, 0.860930735930736], [0.8145161290322581, 0.36038961038961037], [0.8991935483870969, 0.8041125541125542]]

# small
X = [[0.5020161290322581, 0.336038961038961], [0.44556451612903225, 0.400974025974026], [0.4536290322580645, 0.5497835497835498], [0.33870967741935487, 0.9204545454545455], [0.13508064516129034, 0.8203463203463204], [0.08870967741935484, 0.34956709956709964], [0.7580645161290323, 0.8419913419913421], [0.9092741935483871, 0.5660173160173161], [0.6270161290322581, 0.05194805194805194]]

X = np.array(X)
# #############################################################################
# Compute DBSCAN
db = DBSCAN(eps=0.195, min_samples=2).fit(X)
# db = KMeans(n_clusters=2).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)

print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, labels))

# #############################################################################
# Plot result
import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()