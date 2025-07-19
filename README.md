# Python-Data-Plotly-Predictive-Analytics-Dashboard

## Find and Analyze the Dashboard/Graph
Python &amp; Plotly Data Visualization and storytelling: given a type of plot (dashboard, Sankey diagram, etc.), Recreate a similar visual that tells the same story using a dummy dataset, Python scripts for data generation and visualization that would naturally produce the visual you created.

The data row begins with searching the web for a reference image of a business-related dashboard or graph that matches the chart description you are given. For example, it may search for something such as “dashboard for business software”.

Obtaining a reference image, Carefully inspect.
The main objective is to creatively expand on this reference image, capturing the core features while developing datasets and visualizations that reflect real-world situations.

## Generate a Prompt for it
This reference image might Write a simple user-style question or instruction that the reference image would answer. So, this should prompt frames the data story and helps guide your synthetic data generation:
 - The prompt should not be very specific and can be open-ended.
 - The prompt should not specify a lot of formatting requirements.
 - The prompt must be natural and practical, reflecting the kind of questions a user might realistically ask in a real-world scenario.

## Generate Data To Tell the Business Story
Write a data creation script within the scripts folder (../scripts/data_gen.py) that:
 - Uses only pandas and numpy.
 - Generates at least two datasets (as DataFrames or Numpy arrays) into the data folder, such as (../data/sales_data.csv and ../data/local_sales_data.csv)
 - Tells a similar story based on your reference image, reflects real-world situations, and contains enough detail to fully recreate the image.

## Recreate the Visualization
Write a visualization script within the scripts folder (../scripts/viz.py) that:
 - Uses only pandas, numpy, and plotly (library is known as dash)
   - You can use the pip install dash command to install Plotly Dash.
 - Reads the generated files from your data creation script.
 - Generates one HTML file of an interactive dashboard into the outputs folder (../outputs/dashboard.html) using Plotly's HTML export method. It may be helpful to also reference the “Inserting Plotly Output into HTML” section on that page.
 - Works and can be interacted with properly.
 - Contains visuals that adhere to the following style guidelines:
Typography: Titles MUST be bold, and properly formatted legends and labels.
Aesthetics: Organize layout using visual containers (e.g., cards, sections). Use depth thoughtfully via shadows or gradients to create visual hierarchy. We do not want flat images.
Storytelling: Establish a clear narrative flow: start with high-level KPIs, then drill into details. Data elements should feel connected and purposeful, not isolated or random.
Complexity: Dashboards must follow the level of complexity found here. Dashboard complexity should match the visual density and insight variety shown in the provided reference. Avoid oversimplification.
Layout: No overlapping elements or cut-off text. Ensure consistent padding, margin, and spacing between plots.
Legends: If a legend is present, ensure it is clearly displayed and boxed if appropriate. Use well-organized legend placement with appropriate spacing.
Color Palette: Use a professional and aesthetically pleasing color scheme. The color palette should complement the data and enhance readability.
Overall Quality: The final plot should be polished and suitable for a presentation or publication.

## Upload Files
This step is very important to save your work. On the left side panel on the Labelbox platform, you will be copy pasting the contents of the data generation script, visualization script, and generated HTML file. Note that you may want to open the HTML file in your code editor in order to be able to copy paste the actual contents of the file. You will not need to upload the generated .csv/.npy files, as these can be generated from your data generation script.
Folder Structure Overview
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
