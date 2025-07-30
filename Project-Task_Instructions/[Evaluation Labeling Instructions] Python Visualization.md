## ![][image1]

## **EVALUATION ONLY \- Labeling Instructions**

**(DO NOT USE THIS INSTRUCTION DOCUMENT FOR PRODUCTION PROJECT)**

## Objective

**IMPORTANT UPDATE AS OF JULY 12TH:**  
**We are no longer using an upload script. You will be copy pasting the contents of the scripts and HTML file into the Labelbox editor.**

This is a Python evaluation focused on data visualization and storytelling: given a type of plot (dashboard, Sankey diagram, etc.), your task is to recreate a similar visual that tells the same story using a dummy dataset and Python scripts for data generation and visualization. You will also write an input prompt that would naturally produce the visual you created.

**Walkthrough Video**: [\[Evaluation Labeling Walkthrough\] Advanced Capabilities v2](https://www.loom.com/share/97050425732f4d7c81f40c8071df1cd3?sid=ed772ae9-0bf2-46d9-91c1-d2f8f12c0415)

---

## Labeling Steps

## 1\. Find and Analyze the Dashboard/Graph

The data row begins with searching the web for a **reference image** of a business-related dashboard or graph that matches the chart description you are given. For example, you may search for something such as “dashboard for business software”.

When you find a reference image, you will need to obtain the direct URL to the image itself. You can do this by right-clicking on the image and selecting “Copy Image Address”.

Carefully inspect your reference image. Your objective is to creatively expand on this reference image, capturing the core features while developing datasets and visualizations that reflect real-world situations.

---

## 2\. Generate a Prompt

Write a simple user-style question or instruction that the reference image would answer. This prompt frames the data story and helps guide your synthetic data generation:

* The prompt should not be very specific and can be open-ended.  
* The prompt should not specify a lot of formatting requirements.  
* The prompt must be natural and practical, reflecting the kind of questions a user might realistically ask in a real-world scenario.

### Prompt Examples

Below are some examples of good prompts along with the story and visuals related to them. These are for inspiration only and you should not directly use them:

|  | Prompt Topic | Story & Visuals |  |
| ----- | ----- | ----- | ----- |
|  | “Show how global electric-vehicle (EV) adoption has evolved since 2015 and predict the next five years.” | • Multi-line time-series of unit sales by region • Stacked area of battery chemistries • Sankey of supply-chain flows • Heat-map of EV market-share by country |  |
|  | “Analyze hospital network capacity vs. infectious-disease outbreaks during winter seasons.” | • Dual-axis line (ICU beds vs. cases) • Correlation heat-map of symptoms & test positivity • Box-whisker of LOS by diagnosis group |  |
|  | “Contrast same-day vs. two-day e-commerce delivery performance during holiday peaks.” | • Violin plot of delivery times • Pareto of top delay causes • Time-series forecast of warehouse backlog |  |
|  | “Track sustainable-aviation-fuel (SAF) usage across the airline industry and project carbon savings.” | • Waterfall of CO₂ reductions • Treemap of SAF feedstocks • Monte Carlo projection of carbon offset targets |  |
|  | “Visualise smart-city energy flows between residential, commercial, and EV charging nodes.” | • Chord diagram of kWh transfers • Area chart of renewables vs. grid demand • Animated map of substation loads by hour |  |
|  | “Evaluate multi-modal public-transport punctuality and rider sentiment in megacities.” | • Box-plot of lateness by mode (bus, metro, rail) • Word-cloud & sentiment drill-down • Gantt of headways over 24 h |  |
|  | “Benchmark fintech fraud-detection algorithms across geographies and transaction types.” | • ROC curves for each model • Confusion-matrix heat-maps • KPI bullet charts for latency & cost |  |
|  | “Map food-delivery fleet efficiency vs. weather impacts in dense urban zones.” | • Scatter of drop-offs vs. travel km • Histogram of idle minutes per driver • Isochrone map overlaying rainfall intensity |  |
|  | “Identify semiconductor-fab yield losses and correlate with equipment maintenance logs.” | • Stacked bar of defect classes • Control chart of daily yields • Network graph of tool dependencies |  |
|  | “Forecast coastal-city real-estate risk under sea-level-rise scenarios to 2100.” | • Scenario fan-chart of property values • Choropleth of flood exposure zones • Animated slider of shoreline retreat |  |

---

## 3\. Generate Data To Tell the Business Story

Write a data creation script within the scripts folder (`../scripts/data_gen.py`) that:

* Uses **only** `pandas` and `numpy`.  
* Generates **at least two** datasets (as DataFrames or Numpy arrays) into the data folder, such as (`../data/sales_data.csv` and `../data/local_sales_data.csv`)  
* Tells a similar story based on your reference image, reflects real-world situations, and contains enough detail to fully recreate the image.

---

## 4\. Recreate the Visualization

Write a visualization script within the scripts folder (`../scripts/viz.py`) that:

* Uses **only** `pandas`, `numpy`, and `plotly` (library is known as dash)  
  * You can use the `pip install dash` command to install Plotly Dash.  
* Reads the generated files from your data creation script.  
* Generates **one** HTML file of an interactive dashboard into the outputs folder (`../outputs/dashboard.html`) using Plotly's [HTML export](https://plotly.com/python/interactive-html-export/) method. It may be helpful to also reference the “Inserting Plotly Output into HTML” section on that page.  
* Works and can be interacted with properly.  
* Contains visuals that adhere to the following style guidelines:  
  * **Typography**: Titles MUST be bold, and properly formatted legends and labels.  
  * **Aesthetics**: Organize layout using visual containers (e.g., cards, sections). Use depth thoughtfully via shadows or gradients to create visual hierarchy. We do not want flat images.  
  * **Storytelling**: Establish a clear narrative flow: start with high-level KPIs, then drill into details. Data elements should feel connected and purposeful, not isolated or random.  
  * **Complexity**: Dashboards must follow the level of complexity found [here](?tab=t.g10z3iduj1fv). Dashboard complexity should match the visual density and insight variety shown in the provided reference. Avoid oversimplification.  
  * **Layout**: No overlapping elements or [cut-off text](https://github.com/plotly/plotly.js/issues/2001#issuecomment-981888072). Ensure consistent padding, margin, and spacing between plots.  
  * **Legends**: If a legend is present, ensure it is clearly displayed and boxed if appropriate. Use well-organized legend placement with appropriate spacing.  
  * **Color Palette**: Use a professional and aesthetically pleasing color scheme. The color palette should complement the data and enhance readability.  
  * **Overall Quality**: The final plot should be polished and suitable for a presentation or publication.


---

## 5\. Upload Files

This step is **very important** to save your work. On the left side panel on the Labelbox platform, you will be copy pasting the contents of the data generation script, visualization script, and generated HTML file. Note that you may want to open the HTML file in your code editor in order to be able to copy paste the actual contents of the file. You will not need to upload the generated .csv/.npy files, as these can be generated from your data generation script.

### Folder Structure Overview

```
<data_row_id>/
├── data/
│   ├── sample.npy
│   ├── dataframe2.csv
│   └── dataframe.csv          # Generated .csv and/or npy files
│
├── scripts/
│   ├── data_gen.py            # Data generation script
│   └── viz.py                 # Visualization script
│
├── outputs/
│   └── dashboard.html         # Interactive html generated using viz.py
```

## Best Practices

Please refer to [this](?tab=t.1kvo3yk0hu3d) section to see examples of the level of complexity that is required for dashboards.

Refer to [this](https://docs.google.com/document/d/1TTrcVLIeuBkZAN_7LmIoubn2xhoDGSIOE_lUNAJNS6o/edit?tab=t.a0cdlqid3z09) section for examples of the charts that you may encounter.

While searching for a reference image, here are some examples of charts you should be pursuing versus not:

✅[Positive examples](https://docs.google.com/document/d/1TTrcVLIeuBkZAN_7LmIoubn2xhoDGSIOE_lUNAJNS6o/edit?tab=t.g10z3iduj1fv)  
❌[Negative examples](https://docs.google.com/document/d/1TTrcVLIeuBkZAN_7LmIoubn2xhoDGSIOE_lUNAJNS6o/edit?tab=t.24c353l6whvd)

A full example is available [here](?tab=t.nabf08jm9e0j).  


[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKYAAAAmCAYAAABOOOCvAAAHgklEQVR4Xu2cTYgcRRTHN/Fb8VuMbBYyu870x8zsGllR/EAXBMGLFxEkKOJByM2zoiKCwbMHwaMHPYggCCYg5KIH9RAxORiCCoJCgoKKRuNHEn1vumvm9b/rVXXNzvRkd/oHj92t/6tXr6rfdld3z+7CwiaJ4+5/PsM+DQ1ThYruBBahZti3oWFquIoujuPFeSrMKIpumpe5XtBE0bDo3kaNMQdpdXX1ev7K/ugzC/BMHlJIrn4uraE+drgOQBQlz0jdfL+83N+FvnWDBaTNwYarn0trqIk4TgeLnyTJjagxloPjLOQ6wQLK5tH9Av1sYD9dS2c+z7nEdmAMUZQ+yRqdNb+U7abPysrKtbK9Tii3b7C4XHNBfH0WF9evbLfbl2F7Qw2Yg7J3797rUGO0g8a4tDqQRUVF6iwyG77CbJgRa2trV7kOCl3CfsoOevc71Bhq/ycvirdQq4HhdsLkD4V2GjsgTWFeoPgOiE9nqvhMA1tR2dpcuPyjqPeRNKkhnU56fzFW+pvUqe19soO5HQLNtB+kX3TQ0jPFuPGi1KsgryT8JKXT6T6NPojMqdheuCrtR1/a7j1lfDudZJ/MfRTFQ5L0Hs062Tf2YjIHUJPEce9Y7nsStWkiJz2a+GMXldt07DH8moHa96OfNFq7f3O/P0ZtxfXGPrY2NHLZIWMgUbSaYB+bYT8D+lCN2F68mMIcttF8X8U231glPB2C7rpDfCeFNmnZTkVwXmqIa/FcWqbH96KP3dJP4oDChLOSajKGhIrjOPq6DPszqGOf3KyFafFTxylBi3MqC5R8jxpjgvEeFDUb7Xb39qAENgnlf1abtHhRUNIQ1+K5NJvOZp5Q8N08Fdhg/53ZKF9/YQ79jvL6c0zqPyxsEfOojJOzE/34qYoRs7xKcSrNLY/1VzzYlqQ/x5bCjMUvYG5H4jg5xGuBY1gxHbHd4NNtjNNnXGDyv7t01CQQx1kwLo1+Gd6UuiFJkrvLvv7ClLqh1Wpd7vPz6Ya8sFQ/jGMrXkPZtxyvErwxzwc7hhpjgq+vr1+CGkPae9jGjC5t+iQmAb8E8C2C1F2vTl0LOq6GkF64gfEVptQQ0n/RfKMoWtE0G8WcNjW/gu/GxsbF6FMJ12DtdvtWl05F92euH0GNMfujXq93KWqTAhcCdabqM01XLE2jAtgN7c4bEUb6b6YwGc03PE76q+ZfjNV7RGpI6LhWTGdt7+gJXnpuaCHopmkcZA54kA38Wwu5WotH+mDOmqa1u5D+mHMxnn0+Em1sGOM1qWlUiSXbbRTz9/tbcXWmRXkhn5SiDwf/IPuankEfxvjRWbON2iSQi+A6M0s/vFQZpA9bFU1rd2GuJFkuemFqeUq0sTGvUNNiyXYb0rdK/iVMZ+1gehIZ3u3xDx5frz4u8gBnC5G+oxn6YixG6uijaVq7i6YwFWjvuOQaiBbudBY4/Rg1RvTdyT+3Wr1b3PG6g3hk1njjIhch1Fqt8mcB0KeKprW7kP5NYQp8g1TRtQWVbRKfHkoU9e6TixBqtkVDnyqa1u6imId9HTPNH08bW7YnSf8hqYWijWEjNP8hdOnuZh21vWN2maGgn0XRbbvRtATjAXaNoXj8MJb1iZw15QKMa76YVTT6/rCt3YX0r6MwKc4pqYWijWEjNP8hvgFkYN20os70JEnuQY3xjR1ClXwQfNPBWxCp4zzH1I5LDcHnrnUUJmqhhMQJzX8AOecP07ufo2ZYW1u7OUm6L2vmS9Cly2d+qIXQbpuzfmZ0FbgBfTRkP8xjGhqCvtMqTFwjqdkgn3fFuA+CFhInKP8BVYO7oBuna/I451BjxFbgYdSYSeQgJx8ay3V37orr1npvoE574DulT+ZX9Mn8plOYqNl0ictXa7chfavkzx3OZx2Sw6iF4kvSpdNZM/8IVrXLr43i5MPiyA9D5/2HH2qQ7Zi/S2P4IKCPzThf6Yv5F33L4yDSH7UFeAmSj1f4wHRc/qAFxym8gPCMUaA4lt/fWSyh8N+9uOLR2eLHfBF+QI0ZJR9fjZoPKuhXQhbKhuwvY2jtPs2AZ2ObsV+NhcljfYo5uIzOG69jDN8YkmIsjz9Pnh2Xl9M9qI2LL1GPPvarSjnxcfozWgyt3adJeL+Lvmx0kIZvxuosTAavEppRLo9jX6bKGIZiPI9/1aAhmH90oMWNR38f9DVqjOg7eEhfFboBe04a6lXgpwYyxtLS0hXcTmf6l6TJPrSPfFGa1EJxFWbo/GidnzWGGhLH/Ttk4Qh7An0lIflA/s+jPsSSxMQt4O/PC/j07QquH+pzARXNA6NF4Ev6pE1fWN5DaotPZ518H9r9CrWtSqz8Ox2kWJjpCdTnBq046kAbW2vfitA8/pbFhrqEbi6C3xRtW7rd7l2zWoh+v78Lx6azxEn+mc6W30rfrQrtE8/JYmNL07SDfugzi+NxwSEWIuhmYxKMDkT2d9Db8aBgwVUxjDG3zHBBSg96k6S/gU5bHZyjy7DvXGNuVugyswe1aTNPB4a2KAdwvrl9iL4NOZbFmoGFv/Fp2ObQWfNouVDqtPQs5tQwf/wPa0cuOjc7BTcAAAAASUVORK5CYII=>