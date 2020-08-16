from flask import Flask, render_template
import altair as alt
from sportplot import gpx_parser, analysis, postprocess
from sportplot import fit
import os
import json

app = Flask(__name__)

DEFAULT_GPX = 'data/4132209152_activity.gpx'
gpx = gpx_parser.GPXFile(DEFAULT_GPX)
act_data = postprocess.ActData(gpx.points)
BASE_DIR = '/srv/storage/mucho/esport/garmin/'


def get_ele_chart(df):
    base = alt.Chart(act_data.df).encode(
        alt.X('hoursminutesseconds(time_from_start)', title='Time')
    )

    ele = base.mark_line().encode(
        alt.Y(
            'ele',
            axis=alt.Axis(title='Elevation'),
            scale=alt.Scale(zero=False)
        ),
    ).interactive()

    hr = base.mark_line().encode(
        alt.Y(
            'hr',
            axis=alt.Axis(title='Heart Rate')
        ),
    ).interactive()

    multi = alt.vconcat(
        ele,
        hr,
        )
    return multi.to_json()

@app.route('/')
def index():
    return render_template('index.html',
                           summary=act_data.get_summary_text())


@app.route('/activity/<act_id>')
def activity(act_id):
    fit_fn = '{}.fit'.format(act_id)
    fit_path = os.path.join(BASE_DIR, fit_fn)
    fit_file = fit.CyclingFitFile(fit_path)
    ele_chart = get_ele_chart(fit_file.records_to_df())
    print(ele_chart)
    return render_template('activity.html',
                           act_id=act_id,
                           ele_chart=json.loads(ele_chart))

@app.route('/charts/ele')
def chart_ele():
    base = alt.Chart(act_data.df).encode(
        alt.X('hoursminutesseconds(time_from_start)', title='Time')
    )

    ele = base.mark_line().encode(
        alt.Y(
            'ele',
            axis=alt.Axis(title='Elevation'),
            scale=alt.Scale(zero=False)
        ),
    ).interactive()

    hr = base.mark_line().encode(
        alt.Y(
            'hr',
            axis=alt.Axis(title='Heart Rate')
        ),
    ).interactive()

    multi = alt.vconcat(
        ele,
        hr,
        )
    return multi.to_json()


@app.route('/charts/zones')
def chart_zones():
    time_in_zone = analysis.get_time_in_zone(act_data.df, 160)
    zones = alt.Chart(
        data=time_in_zone,
        # height=700,
        # width=600
    ).mark_bar().encode(
        x='zone',
        y='time'
    ).interactive()
    return zones.to_json()


if __name__ == '__main__':
    app.run(debug=True)
