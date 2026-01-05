import matplotlib.pyplot as plt
import numpy as np

import matplotlib
import matplotlib as mpl

ratesL = [0.33, 0.30, 0.25]
ratesA = [0.25, 0.30, 0.33]

experiments = ["random"]
#experiments = ["0.15", "0.30", "0.45"]

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw=None, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current Axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    kwargs["cmap"] =  mpl.colormaps.get_cmap(kwargs["cmap"] )
    kwargs["cmap"].set_bad(color='grey')
    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(range(data.shape[1]), labels=col_labels,
                  rotation=-30, ha="right", rotation_mode="anchor")
    ax.set_yticks(range(data.shape[0]), labels=row_labels)

    ax.set_xlabel("adv rate")
    ax.set_ylabel("lazy rate")
    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data[i, j] != np.nan:
                kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
                text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            else:
                kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
                text = im.axes.text(j, i, "fail", **kw)
            texts.append(text)

    return texts


def readfile(path):
    with open(path, "r") as f:
        data = f.readlines()
        retval = []
        for d in data:
            try:
                retval.append(int(d))
            except ValueError:
                if d == "fail\n":
                    retval.append("fail")
        return retval



path = None

for experiment in experiments:
        data = []
        for rateL in ratesL:
            l_data = []
            for rateA in ratesA:
                if experiment == "random":
                    path = f"{experiment}/10000_lazy_{rateL:.2f}_adv_{rateA:.2f}.txt"
                else:
                    path = f"{experiment}/0.60/weighted_{experiment}:10000_lazy_{rateL:.2f}_adv_{rateA:.2f}.txt"
                dt = readfile(path)
                if "fail" in dt:
                    l_data.append(np.nan)
                else:
                    l_data.append(np.mean(dt) * 5)
            data.append(l_data)
        print(experiment, data)
        d = np.array(data)
        plt.rcParams.update({'font.size': 22})
        fig, ax = plt.subplots()

        im, cbar = heatmap(d, ratesL, ratesA, ax=ax,
                   cmap="YlGn", cbarlabel="recovery time, min")
        texts = annotate_heatmap(im, valfmt="{x:.2f}")

        fig.tight_layout()
        plt.show()

        name = f"{experiment}.png"
        fig.savefig(name, bbox_inches='tight')