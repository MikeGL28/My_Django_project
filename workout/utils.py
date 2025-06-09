import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns


def generate_chart_image(data, x_key, y_key, title, xlabel, ylabel):
    plt.figure(figsize=(6, 3))
    sns.set(style="whitegrid")

    x = [item[x_key] for item in data]
    y = [item[y_key] for item in data]

    sns.lineplot(x=x, y=y, marker='o', color='blue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return image_base64