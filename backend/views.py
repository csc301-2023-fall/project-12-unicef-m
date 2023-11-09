from flask import Blueprint, render_template, request, jsonify
from api_helpers import get_access_token, get_dashboards, get_datasets, get_charts, export_one_dashboard, get_charts_with_ID, get_dataset_uuid, set_chart_dataset 

views = Blueprint('views', __name__)


@views.route('/')
def index():
    html_data = get_dataset_to_chart_mapping()
    return render_template("index.html", html_data=html_data)


def get_dataset_to_chart_mapping():
    token = get_access_token()
    dashboards = get_dashboards(token)
    datasets = get_datasets(token)

    dataset_to_chart_map = {}
    all_charts = []
    for d1, d1Name in dashboards:
        charts = get_charts(token, d1)
        all_charts.append(charts)

        dataset_to_chart_map[d1] = {
            "charts": charts,
            "datasets": datasets
        }

    html_data = {
        "dashboards": dashboards,
        "charts": all_charts,
        "datasets": datasets,
        "datasetChartMapping": dataset_to_chart_map
    }
    return html_data


@views.route('/clone', methods=['POST'])
def clone():
    dashboard_source = request.form.get('dashboard_source')
    destination_name = request.form.get('destination_name')

    chart_names = []
    chart_tables = []

    index = 0
    while True:
        chart_name = request.form.get(f'chart{index}')
        dataset = request.form.get(f'dataset{index}')

        if chart_name is None or dataset is None:
            break

        chart_names.append(chart_name)
        chart_tables.append(dataset)
        index += 1

    token = get_access_token()

    # hard coded to 6 for now, change to inputting the dashboard id of the dashboard picked
    extracted_folder_name = export_one_dashboard(token, 6)
    charts = get_charts_with_ID(token, dashboard_source)

    # iterating through all the charts
    for i in range(0, index):
        # getting the uuid for the database that was specified for chart i
        dataset_uuid = get_dataset_uuid(extracted_folder_name + '/datasets/examples/' + chart_tables[i] + '.yaml')

        # building the name of the chart file in the format chart_name_id.yaml
        chart_filename = charts[i][0].replace(" ", "_") + '_' + str(charts[i][1]) + '.yaml'

        # setting the new database uuid in the chart's yaml file
        # chart_names[i] is the new name of chart i
        set_chart_dataset(extracted_folder_name + '/charts/' + chart_filename, dataset_uuid, chart_names[i])

    return render_template("clone.html")


@views.route('/get_dataset_chart_mapping', methods=['GET'])
def get_dataset_chart_mapping():
    return jsonify(get_dataset_to_chart_mapping()["datasetChartMapping"])